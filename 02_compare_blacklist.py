import csv
import os
import glob
import pandas as pd
from functools import reduce

from tqdm import tqdm

if __name__ == '__main__':
    data_dir = r'D:\workspace\PcapX\output'
    black_list_pth = r'D:\Users\11user\Desktop\blacklist-2024.08.14\1.csv'

    # output csv
    file_name = data_dir.split('\\')[-1]
    report_dir = os.path.join('report')
    os.makedirs(report_dir, exist_ok=True)
    out_csv = os.path.join(report_dir, f'{file_name}_blk_ip.csv')

    # get target files
    f_pths = glob.glob(os.path.join(data_dir, '*.csv'))

    # read blk ips
    blk_ips = pd.read_csv(black_list_pth, header=None).to_numpy().flatten().tolist()

    out_ips = []
    for f_pth in tqdm(f_pths):
        # read target src ip and dst ip
        df = pd.read_csv(f_pth, sep=' ', names=['src_ip', 'dst_ip'], header=None)

        # merge src ip and dst ip to one list, and unique ip
        ips = list(set(df['src_ip'].values.tolist() + df['dst_ip'].values.tolist()))

        # filter ip like ["ip1,ip2", "ip3,ip4,ip5"], and covert to [ip1, ip2, ip3, ip4, ip5]
        ips_1 = list(map(lambda x: x.split(','), filter(lambda x: ',' in x, ips)))
        if len(ips_1) != 0:
            ips_1 = list(reduce(lambda x, y: x + y, ips_1))

        # filter ip like this ["ip1", "ip2"]
        ips_2 = list(filter(lambda x: ',' not in x, ips))

        # merge and unique ip
        ips = list(set(ips_1 + ips_2))

        # filter blk ips
        match_blk_ips = list(set(ips) & set(blk_ips))

        # append to out list
        if len(match_blk_ips) != 0:
            out_ips.extend(match_blk_ips)
            out_ips = list(set(out_ips))

    # show info
    print('num of black list ip:', len(blk_ips))
    print('num of match ip:', len(out_ips))
    print('match ip:', out_ips)

    # save into csv
    out_ips = list(map(lambda x: [x], out_ips))
    pd.DataFrame(out_ips, columns=['ip']).to_csv(out_csv, index=False)


