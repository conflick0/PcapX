# PcapX
- extract ip and compare with blacklist
- extract conv ip
- extract endpoints ip
## Installation
* install package
```
pip install -r requirements.txt
```
* set wireshark path in `src/utils.py`. (for windows)
```
WIRE_SHARK_PATH ='C:\Program Files\Wireshark'
```
* put `GeoLite2-City.mmdb` into `src`
```
src/GeoLite2-City.mmdb
```
## Usage
### Extract Blacklist IP
* run `01_extract_ip.py` to extract ip (read pcap, output ip csv)
```
python 01_extract_ip.py
```
* run `02_extract_blacklist_ip.py` to compare blacklist, write black ip csv
```
python 02_extract_blacklist_ip.py
```
### Extract Conv IP
* run `01_extract_ip.py` to extract ip (read pcap, output ip csv)
```
python 01_extract_ip.py
```
* run `02_extract_conv_ip.py` to extract conv ip, write conv ip csv
```
python 02_extract_conv_ip.py
```