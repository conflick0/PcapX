import os
import glob
import pandas as pd
from src.utils import EXTRACT_TYPE, extract_ip


def get_match_blacklist_ip(report_endpoint_dir, black_list_pth):
    # read blk ips
    blk_ips = pd.read_csv(black_list_pth, header=None).to_numpy().flatten().tolist()

    # get target files
    f_pths = glob.glob(os.path.join(report_endpoint_dir, '*.csv'))

    # extract ips from target files
    out_df = extract_ip(EXTRACT_TYPE.ENDPOINT, f_pths)

    # get match ip
    ips = out_df['ip'].values.tolist()
    match_ips = list(set(blk_ips) & set(ips))

    # show info
    print('num of black list ip:', len(blk_ips))
    print('num of ip:', len(ips))
    print('num of match ip:', len(match_ips))
    print('match ip:', match_ips)

    # save match ip
    match_ips = list(map(lambda x: [x], match_ips))
    pd.DataFrame(match_ips, columns=['ip']).to_csv(out_blk_csv, index=False)

    # save endpoint ip
    out_df.to_csv(out_endpoint_csv, index=False)


if __name__ == '__main__':
    black_list_pth = r'D:\Users\11user\Desktop\blacklist-2024.08.14\1.csv'
    report_dir = r'D:\workspace\PcapX\report\test'
    report_endpoint_dir = os.path.join(report_dir, 'endpoint')
    out_blk_csv = os.path.join(report_dir, f'blk_ip.csv')
    out_endpoint_csv = os.path.join(report_dir, f'endpoint_ip.csv')

    get_match_blacklist_ip(report_endpoint_dir, black_list_pth)

