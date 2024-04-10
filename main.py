import os
import platform
import subprocess

import geoip2.database
import pandas as pd


WIRE_SHARK_PATH ='C:\Program Files\Wireshark'


def get_ip_info():
    print('get ip info...')
    base_command = 'tshark -r *.pcap -Y ip -T fields -e ip.src -e ip.dst -e _ws.col.Protocol -E separator=","'

    if platform.system() == 'Windows':
        command = f'$env:path += ";{WIRE_SHARK_PATH}"; {base_command} | Sort-Object | Get-Unique  | Export-Csv -Path "data.csv" -NoTypeInformation'
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    else:
        command = f'{base_command} | sort | uniq > data.csv'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        print("get ip info successfully.")
        return pd.read_csv('data.csv', header=None, names=['src.ip', 'dst.ip', 'protocol'])
    else:
        print("tshark command failed with return code:", result.returncode)
        print("Error:")
        print(result.stderr)
        return None


def get_geo_info(ip):
    with geoip2.database.Reader('data/GeoLite2-City.mmdb') as reader:
        try:
            r = reader.city(ip)
            return [r.city.name, r.country.name, r.location.latitude, r.location.longitude]
        except:
            return [None, None, None, None]


def creat_report_csv():
    # get ip info
    df = get_ip_info()
    if df is None: return

    # get geo info
    print('get geo info...')
    s_df = pd.DataFrame(
        df['src.ip'].apply(lambda x: get_geo_info(x)).tolist(),
        columns=['src.city', 'src.country', 'src.lat', 'src.lon']
    )
    d_df = pd.DataFrame(
        df['dst.ip'].apply(lambda x: get_geo_info(x)).tolist(),
        columns=['dst.city', 'dst.country', 'dst.lat', 'dst.lon']
    )

    df = pd.concat([df, s_df, d_df], axis=1)

    df.to_csv('report.csv', index=False)

    print('done')


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    creat_report_csv()
