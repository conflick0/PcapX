import os
import glob
import pandas as pd
from src.utils import EXTRACT_TYPE, extract_ip


def get_match_blacklist_ip_by_dir(report_endpoint_dir, black_list_pth):
    # get target files
    f_pths = glob.glob(os.path.join(report_endpoint_dir, '*.csv'))

    # extract ips from target files
    out_df = extract_ip(EXTRACT_TYPE.ENDPOINT, f_pths)

    # get match ip
    ips = out_df['ip'].values.tolist()

    # export black list ip
    export_match_blacklist_ip(ips, black_list_pth)

    # save endpoint ip
    out_df.to_csv(out_endpoint_csv, index=False)


def get_match_blacklist_ip_by_file(csv_pth, black_list_pth):
    df = pd.read_csv(csv_pth)
    ips = df['ip'].values.tolist()
    export_match_blacklist_ip(ips, black_list_pth)



def export_match_blacklist_ip(ips, black_list_pth):
    # read blk ips
    blk_ips = pd.read_csv(black_list_pth, header=None).to_numpy().flatten().tolist()

    match_ips = list(set(blk_ips) & set(ips))

    # show info
    print('num of black list ip:', len(blk_ips))
    print('num of ip:', len(ips))
    print('num of match ip:', len(match_ips))
    print('match ip:', match_ips)

    # save match ip
    match_ips = list(map(lambda x: [x], match_ips))
    pd.DataFrame(match_ips, columns=['ip']).to_csv(out_blk_csv, index=False)



if __name__ == '__main__':
    black_list_pth = r'D:\blacklist-2025.01.22.csv.csv'
    report_dir = r'D:\workspace\PcapX\report\tmp'

    is_dir = False # mode use dir or file as inp
    inp_endpoint_dir = os.path.join(report_dir, 'endpoint') # use dir as inp
    inp_csv = r'D:\ip_list.csv' # or use file as inp

    out_blk_csv = os.path.join(report_dir, f'blk_ip.csv')
    out_endpoint_csv = os.path.join(report_dir, f'endpoint_ip.csv')

    if is_dir:
        get_match_blacklist_ip_by_dir(inp_endpoint_dir, black_list_pth)
    else:
        get_match_blacklist_ip_by_file(inp_csv, black_list_pth)

