import os
import glob
import pandas as pd

from src.utils import EXTRACT_TYPE, extract_ip, get_geo_info


if __name__ == '__main__':
    report_dir = r'D:\workspace\PcapX\report\test'
    report_conv_dir = os.path.join(report_dir, 'conv')
    out_csv = os.path.join(report_dir, 'conv_ip.csv')

    # read file paths
    f_pths = glob.glob(os.path.join(report_conv_dir, '*.csv'))

    # extract ip
    df = extract_ip(EXTRACT_TYPE.CONV, f_pths)

    dicts = []
    for _, d in df.iterrows():
        src_city, src_country, src_lat, src_lon  = get_geo_info(d['src_ip'])
        dst_city, dst_country, dst_lat, dst_lon = get_geo_info(d['dst_ip'])
        dicts.append({
            'src_ip': d['src_ip'],
            'dst_ip': d['dst_ip'],
            'src_city': src_city,
            'dst_city': dst_city,
            'src_country': src_country,
            'dst_country': dst_country,
            'src_lat': src_lat,
            'src_lon': src_lon,
            'dst_lat': dst_lat,
            'dst_lon': dst_lon
        })


    df = pd.DataFrame().from_records(dicts).fillna('')
    df.to_csv(out_csv, index=False)

    print('num conv ip:', len(df))
    print('done')

