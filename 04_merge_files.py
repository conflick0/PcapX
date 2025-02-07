import pathlib
import os
from src.utils import exec_tshark_command

def merge_pcap(inp_dir, out_dir):
    inp_path = os.path.join(inp_dir,'*.pcap')
    out_file = os.path.join(out_dir, f'tftp_all.pcap')
    exec_tshark_command(f'mergecap {inp_path} -w {out_file}')


if __name__ == '__main__':
    pcap_dir = r'D:\workspace\PcapX\report\x11\x11'
    out_merge_pcap_dir = r'D:\workspace\PcapX\report\x11'

    merge_pcap(pcap_dir,out_merge_pcap_dir)