# Lost Ark Server Status Checker

A Python script to check the status of Lost Ark game servers and receive notifications when a specific server comes online.

## Overview

This script utilizes web scraping to fetch the server status information from the official [Lost Ark server status page](https://www.playlostark.com/en-us/support/server-status). It can be used to monitor the status of different regions' game servers and get notifications when a specific server becomes online.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `beautifulsoup4`
  - `plyer`
  - `requests`

You can install these packages using the following command:
```
pip install beautifulsoup4 plyer requests
```

## Usage
Run the script using the command line with the following options:
- `-w` or `--watchserver`: Specify the server name to monitor.

### Example Usages
1. To check the status of all servers:
```
python loaserverstatus.py
```

2. To watch a specific server and receive a notification when it comes online:
```
python loaserverstatus.py -w SERVER_NAME
```
Replace **SERVER_NAME** with the name of the server you want to watch.

## Notes
The server status information is scraped from the official website, which might be subject to change. If the structure of the website changes, the script might need adjustments.