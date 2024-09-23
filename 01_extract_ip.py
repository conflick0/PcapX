import glob
import os
import platform
import queue
import subprocess
import threading
import time

WIRE_SHARK_PATH = 'C:\Program Files\Wireshark'

my_queue = queue.Queue()


def get_ip_info(file_path):
    fn = file_path.split('\\')[-1].split('.')[0]

    base_command = f'tshark -B 256 -r {file_path} -Y ip -T fields -e ip.src -e ip.dst -E separator=" "'

    if platform.system() == 'Windows':
        command = f'$env:path += ";{WIRE_SHARK_PATH}"; {base_command} | Sort-Object | Get-Unique  | Out-File -encoding utf8 "output/{fn}.csv"'
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    else:
        command = f'{base_command} | sort | uniq > data/tmp.csv'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check the result
    if result.returncode != 0:
        print("tshark command failed with return code:", result.returncode)
        print("Error:")
        print(result.stderr)
        raise Exception("tshark command failed")


class Worker(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    def run(self):
        while self.queue.qsize() > 0:
            # 取得新的資料
            data = self.queue.get()

            # self.lock.acquire()
            print(f"Worker {self.num}: {data}")

            # 處理資料
            get_ip_info(data)

            time.sleep(1)
            # self.lock.release()


def creat_endpoint_csv(workspace_dir):
    pcap_files = glob.glob(os.path.join(workspace_dir, '*.pcap'))

    # print(pcap_files)

    # input queue
    for pcap_file in pcap_files:
        my_queue.put(pcap_file)

    num_workers = 5
    workers = []
    for i in range(num_workers):
        workers.append(Worker(my_queue, i))

    for i in range(num_workers):
        workers[i].start()

    for i in range(num_workers):
        workers[i].join()

    print('done')


if __name__ == '__main__':
    workspace_dir = r'E:\20240723'
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs('output', exist_ok=True)
    b = time.time()
    for sub_dir in os.listdir(workspace_dir):
        creat_endpoint_csv(os.path.join(workspace_dir, sub_dir))
    e = time.time()
    print(e - b)
    print('done')
