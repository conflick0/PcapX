import os
import glob
import pandas as pd

from src.utils import EXTRACT_TYPE, extract_ip, get_geo_info


if __name__ == '__main__':
    report_dir = r'D:\workspace\PcapX\report\door'
    extract_type = EXTRACT_TYPE.CONV_UDP
    report_conv_dir = os.path.join(report_dir, extract_type)
    out_csv = os.path.join(report_dir, f'{extract_type}.csv')

    # read file paths
    f_pths = glob.glob(os.path.join(report_conv_dir, '*.csv'))

    # extract ip
    df = extract_ip(extract_type, f_pths)

    dicts = []
    for _, d in df.iterrows():
        src_city, src_country, src_lat, src_lon  = get_geo_info(d['src_ip'])
        dst_city, dst_country, dst_lat, dst_lon = get_geo_info(d['dst_ip'])

        if extract_type == EXTRACT_TYPE.CONV_TCP or extract_type == EXTRACT_TYPE.CONV_UDP:
            dicts.append({
                'src_ip': d['src_ip'],
                'src_port': d['src_port'],
                'dst_ip': d['dst_ip'],
                'dst_port': d['dst_port'],
                'src_city': src_city,
                'dst_city': dst_city,
                'src_country': src_country,
                'dst_country': dst_country,
                'src_lat': src_lat,
                'src_lon': src_lon,
                'dst_lat': dst_lat,
                'dst_lon': dst_lon
            })
        else:
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


