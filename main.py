import glob
import os
import platform
import subprocess

import geoip2.database
import pandas as pd

WIRE_SHARK_PATH = 'C:\Program Files\Wireshark'


def get_ip_info(file_path):
    base_command = f'tshark -r {file_path} -Y ip -T fields -e ip.src -e ip.dst -e _ws.col.Protocol -E separator=","'

    if platform.system() == 'Windows':
        command = f'$env:path += ";{WIRE_SHARK_PATH}"; {base_command} | Sort-Object | Get-Unique  | Out-File -encoding utf8 "data/tmp.csv"'
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    else:
        command = f'{base_command} | sort | uniq > data/tmp.csv'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        return pd.read_csv('data/tmp.csv', header=None, names=['src.ip', 'dst.ip', 'protocol'])
    else:
        print("tshark command failed with return code:", result.returncode)
        print("Error:")
        print(result.stderr)
        raise Exception("tshark command failed")


def get_geo_info(ip):
    with geoip2.database.Reader('data/GeoLite2-City.mmdb') as reader:
        try:
            r = reader.city(ip)
            return [r.city.name, r.country.name, r.location.latitude, r.location.longitude]
        except:
            return [None, None, None, None]


def get_ip_geo_dict(df):
    ips = set(df['src.ip'].values.tolist() + df['dst.ip'].values.tolist())
    return {ip: get_geo_info(ip) for ip in ips}


def get_endpoint_info(file_path):
    # get ip info
    df = get_ip_info(file_path)

    # check empty
    if len(df) == 0: return None

    # get geo info
    ip_geo_dict = get_ip_geo_dict(df)

    # map ip to geo
    geo_col = ['src.city', 'src.country', 'src.lat', 'src.lon', 'dst.city', 'dst.country', 'dst.lat', 'dst.lon']
    geo_df = df.apply(lambda x: pd.Series(ip_geo_dict[x.iloc[0]]+ip_geo_dict[x.iloc[1]], index=geo_col), axis=1)

    # concat ip and geo df
    df = pd.concat([df, geo_df], axis=1)
    return df


def creat_endpoint_csv(workspace_dir):
    pcap_files = glob.glob(os.path.join(workspace_dir, '*.pcap'))

    out_df = pd.DataFrame()
    for pcap_file in pcap_files:
        print(f'processing {pcap_file} ...')
        df = get_endpoint_info(pcap_file)
        print(f'{pcap_file} done')
        if df is None: continue
        out_df = pd.concat([out_df, df], axis=0)
        out_df = out_df.drop_duplicates()


    out_df = out_df.fillna('')
    out_df.insert(0, 'id', out_df.index + 1)

    out_df.to_csv('endpoint.csv', index=False)

    print('done')


if __name__ == '__main__':
    workspace_dir = 'workspace'
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs('data', exist_ok=True)
    creat_endpoint_csv(workspace_dir)
