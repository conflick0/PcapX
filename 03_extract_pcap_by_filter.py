import glob
import os
import pathlib
import time

from src.utils import exec_workers
from src.utils import exec_tshark_command


def get_pcap_files(workspace_dir, ext_name):
    pcap_files = glob.glob(os.path.join(workspace_dir, '**', f'*.{ext_name}'), recursive=True)
    return pcap_files

def get_cmd(file_path, out_dir):
    fn = file_path.split('\\')[-1].split('.')[0]
    out_file = os.path.join(out_dir, f'{fn}.pcap')
    command = f'tshark -n -r {file_path} -Y "udp.port == 177" -w "{out_file}"'
    return command

def export_tftp_pcap(
        pcap_files,
        num_workers,
        out_csv_dir,
    ):

    # get tshark commands
    cmds = list(map(lambda pcap_file: get_cmd(pcap_file, out_csv_dir), pcap_files))

    # exec workers
    exec_workers(cmds, exec_tshark_command, num_workers)




if __name__ == '__main__':
    workspace_dir = r'E:\x11' # pcap 的資料夾
    num_workers = 8                                    # thread 的數量
    ext_name = 'pcap'                                  # pcap副檔名 (pcapng 或 pcap)

    # 輸出目錄位置
    report_dir = os.path.join('report')
    out_pcap_dir = os.path.join(report_dir, pathlib.PurePath(workspace_dir).parts[-1], 'x11')

    # 建立資料夾
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(out_pcap_dir, exist_ok=True)

    # 讀取所有 pcap 檔案
    pcap_files = get_pcap_files(workspace_dir, ext_name)

    print('[info]')
    print('extract_type:', 'tftp')
    print('workspace_dir:', workspace_dir)
    print('num_workers:', num_workers)
    print('ext_name:', ext_name)
    print('num_pcap:', len(pcap_files))
    print('')

    print('[process]')
    b = time.time()
    export_tftp_pcap(pcap_files, num_workers, out_pcap_dir)
    e = time.time()
    print('time:', e - b, 'secs')
    print('done')

