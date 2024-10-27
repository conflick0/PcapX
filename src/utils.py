import os
import threading
import time
import queue
import platform
import subprocess
from dataclasses import dataclass
import pandas as pd
import geoip2.database


WIRESHARK_PATH = 'C:\Program Files\Wireshark'


@dataclass
class EXTRACT_TYPE:
    ENDPOINT='endpoint'
    CONV='conv'


class Worker(threading.Thread):
    def __init__(self, queue, num, fn):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num
        self.fn = fn

    def run(self):
        while self.queue.qsize() > 0:
            # 取得新的資料
            data = self.queue.get()

            # self.lock.acquire()
            print(f"Worker {self.num}: {data}")

            # 處理資料
            self.fn(data)

            time.sleep(1)
            # self.lock.release()


def exec_workers(data, fn, num_workers):
    my_queue = queue.Queue()

    # input queue
    for d in data:
        my_queue.put(d)

    workers = []
    for i in range(num_workers):
        workers.append(Worker(my_queue, i, fn))

    for i in range(num_workers):
        workers[i].start()

    for i in range(num_workers):
        workers[i].join()


def exec_tshark_command(command):
    if platform.system() == 'Windows':
        result = subprocess.run(
            ["powershell", "-Command", f'$env:path += ";{WIRESHARK_PATH}"; {command}'],
            capture_output=True,
            text=True
        )
    else:
        raise Exception('not supported linux platform')

    # Check the result
    if result.returncode != 0:
        print("tshark command failed with return code:", result.returncode)
        print("Error:")
        print(result.stderr)
        raise Exception("tshark command failed")


def extract_ip(extract_type, csv_files):
    """
    extract ip from csv files
    :param extract_type: 'endpoint' or 'conv'
    :param csv_files:
    :return: df
    """
    if extract_type == EXTRACT_TYPE.CONV:
        names = ['src_ip', 'dst_ip']
    elif extract_type == EXTRACT_TYPE.ENDPOINT:
        names = ['ip']
    else:
        raise ValueError(f'invalid extract_type: {extract_type}')

    out_df = pd.DataFrame()
    for f_pth in csv_files:
        # read target src ip and dst ip
        df = pd.read_csv(f_pth, names=names, header=None)

        # concat df
        out_df = pd.concat([out_df, df])

        # drop duplicates
        out_df = out_df.drop_duplicates()

    return out_df


def get_geo_info(ip):
    with geoip2.database.Reader('src/GeoLite2-City.mmdb') as reader:
        try:
            r = reader.city(ip)
            return [r.city.name, r.country.name, r.location.latitude, r.location.longitude]
        except:
            return [None, None, None, None]