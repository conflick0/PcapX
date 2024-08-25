import glob
import os
import platform
import subprocess

import geoip2.database
import pandas as pd

WIRE_SHARK_PATH = 'C:\Program Files\Wireshark'


def get_ip_info(file_path, with_protocol):
    protocol_cmd = '-e _ws.col.Protocol' if with_protocol else ''
    base_command = (f'tshark -r {file_path} -Y ip -T fields -e ip.src -e ip.dst {protocol_cmd} '
                    f' -e ip.geoip.src_country -e ip.geoip.src_city -e ip.geoip.src_lat -e ip.geoip.src_lon '
                    f'-e ip.geoip.dst_country -e ip.geoip.dst_city -e ip.geoip.dst_lat -e ip.geoip.dst_lon '
                    f'-E separator=","')

    if platform.system() == 'Windows':
        command = f'$env:path += ";{WIRE_SHARK_PATH}"; {base_command} | Sort-Object | Get-Unique  | Out-File -encoding utf8 "data/tmp.csv"'
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    else:
        command = f'{base_command} | sort | uniq > data/tmp.csv'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        return pd.read_csv('data/tmp.csv', header=None, names=[
            'src.ip', 'dst.ip', 'protocol',
            'src.country', 'src.city', 'src.lat', 'src.lon',
            'dst.country', 'dst.city', 'dst.lat', 'dst.lon'
        ])
    else:
        print("tshark command failed with return code:", result.returncode)
        print("Error:")
        print(result.stderr)
        raise Exception("tshark command failed")


def creat_endpoint_csv(workspace_dir, with_protocol):
    pcap_files = glob.glob(os.path.join(workspace_dir, '*.pcap'))

    out_df = pd.DataFrame()
    for pcap_file in pcap_files:
        print(f'processing {pcap_file} ...')
        df = get_ip_info(pcap_file, with_protocol)
        print(f'{pcap_file} done')
        if df is None: continue
        df = df.fillna('')
        out_df = pd.concat([out_df, df], axis=0)
        out_df = out_df.drop_duplicates()

    out_df.insert(0, 'id', out_df.index + 1)

    out_df.to_csv('endpoint.csv', index=False)

    print('done')


if __name__ == '__main__':
    workspace_dir = 'workspace'
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs('data', exist_ok=True)
    creat_endpoint_csv(workspace_dir, with_protocol=True)
