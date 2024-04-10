# PcapX
Get ip and geo information from pcap.
## Installation
### Download wireshark (tshark)
* Download from [here](https://www.wireshark.org/download.html).
### Download GeoLite2-City.mmdb
* Download `GeoLite2-City.mmdb` from [here](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data).
* Put `GeoLite2-City.mmdb` into `data` dir.
### Install package
```
pip install -r requirements.txt
```
### Download test pcap (optional)
* Download `Aleta_29072017.pcap` from [here](http://dataset.tlm.unavarra.es/ransomware/).
## Usage
* set wireshark path in `main.py`. (for windows)
```
WIRE_SHARK_PATH ='C:\Program Files\Wireshark'
```
* run `main.py` to get ip geo report.
```
python main.py
```
```
src.ip,dst.ip,protocol,src.city,src.country,src.lat,src.lon,dst.city,dst.country,dst.lat,dst.lon
192.168.1.5,192.168.1.4,TCP,,,,,,,,
192.168.1.5,192.168.1.4,UDP,,,,,,,,
8.8.8.8,192.168.1.4,DNS,,United States,37.751,-97.822,,,,
```
