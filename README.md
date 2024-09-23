# PcapX
extract ip and compare with blacklist
## Install package
```
pip install -r requirements.txt
```
## Usage
* set wireshark path in `01_extract_ip.py`. (for windows)
```
WIRE_SHARK_PATH ='C:\Program Files\Wireshark'
```
* run `01_extract_ip.py` to extract ip, write ip list csv to `output`
```
python 01_extract_ip.py
```
* run `02_compare_blacklist.py` to compare blacklist, write black ip csv to `report`
```
python 02_compare_blacklist.py
```