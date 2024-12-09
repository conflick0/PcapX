import glob
import os
import pathlib
import time


from src.utils import exec_workers
from src.utils import exec_tshark_command
from src.utils import EXTRACT_TYPE


def get_conv_cmd(file_path, out_dir):
    fn = file_path.split('\\')[-1].split('.')[0]
    out_file = os.path.join(out_dir, f'{fn}.csv')
    command = f'tshark -n -r {file_path} -q -z conv,ip | Select-String "<->" | ForEach-Object {{ $fields = $_ -split \'\s+\'; "$($fields[0]),$($fields[2])" }} | Out-File -encoding utf8 "{out_file}"'
    return command

def get_conv_tcp_cmd(file_path, out_dir):
    fn = file_path.split('\\')[-1].split('.')[0]
    out_file = os.path.join(out_dir, f'{fn}.csv')
    command = f'tshark -n -r {file_path} -q -z conv,tcp | Select-String "<->" | ForEach-Object {{ $fields = $_ -split \'\s+\'; "$($fields[0]),$($fields[2])" }} | Out-File -encoding utf8 "{out_file}"'
    return command


def get_conv_udp_cmd(file_path, out_dir):
    fn = file_path.split('\\')[-1].split('.')[0]
    out_file = os.path.join(out_dir, f'{fn}.csv')
    command = f'tshark -n -r {file_path} -q -z conv,udp | Select-String "<->" | ForEach-Object {{ $fields = $_ -split \'\s+\'; "$($fields[0]),$($fields[2])" }} | Out-File -encoding utf8 "{out_file}"'
    return command


def get_endpoint_cmd(file_path, out_dir):
    fn = file_path.split('\\')[-1].split('.')[0]
    out_file = os.path.join(out_dir, f'{fn}.csv')
    command = f'tshark -n -r {file_path} -q -z endpoints,ip | Select-String -Pattern "(\d+\.\d+\.\d+\.\d+)" | ForEach-Object {{ $fields = $_ -split \'\s+\'; "$($fields[0])" }} | Out-File -encoding utf8 "{out_file}"'
    return command


def get_pcap_files(workspace_dir, ext_name):
    pcap_files = glob.glob(os.path.join(workspace_dir, '**', f'*.{ext_name}'), recursive=True)
    return pcap_files


def creat_ip_csv(
        extract_type,
        pcap_files,
        num_workers,
        out_csv_dir,
    ):

    if extract_type == EXTRACT_TYPE.CONV:
        get_cmd = get_conv_cmd
    elif extract_type == EXTRACT_TYPE.ENDPOINT:
        get_cmd = get_endpoint_cmd
    elif extract_type == EXTRACT_TYPE.CONV_TCP:
        get_cmd = get_conv_tcp_cmd
    elif extract_type == EXTRACT_TYPE.CONV_UDP:
        get_cmd = get_conv_udp_cmd
    else:
        raise ValueError(f'invalid extract_type: {extract_type}')

    # get tshark commands
    cmds = list(map(lambda pcap_file: get_cmd(pcap_file, out_csv_dir), pcap_files))

    # exec workers
    exec_workers(cmds, exec_tshark_command, num_workers)


if __name__ == '__main__':
    workspace_dir = r'D:\workspace\PcapX\workspace\door' # pcap 的資料夾
    num_workers = 2                                      # thread 的數量
    ext_name = 'pcapng'                                  # pcap副檔名 (pcapng 或 pcap)
    extract_type = EXTRACT_TYPE.CONV_UDP                 # 讀取類型 (conv 或 endpoint)

    # 輸出目錄位置
    report_dir = os.path.join('report')
    out_csv_dir = os.path.join(report_dir, pathlib.PurePath(workspace_dir).parts[-1], extract_type)

    # 建立資料夾
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(out_csv_dir, exist_ok=True)

    # 讀取所有 pcap 檔案
    pcap_files = get_pcap_files(workspace_dir, ext_name)

    print('[info]')
    print('extract_type:', extract_type)
    print('workspace_dir:', workspace_dir)
    print('num_workers:', num_workers)
    print('ext_name:', ext_name)
    print('num_pcap:', len(pcap_files))
    print('')

    print('[process]')
    b = time.time()
    creat_ip_csv(extract_type, pcap_files, num_workers, out_csv_dir)
    e = time.time()
    print('time:', e - b, 'secs')
    print('done')




