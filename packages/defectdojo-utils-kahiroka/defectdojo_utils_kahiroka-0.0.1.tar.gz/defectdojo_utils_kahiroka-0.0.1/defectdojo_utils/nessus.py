#!/usr/bin/env python3
# Author: Human beings feat. ChatGPT with GitHub Copilot
import os
import requests
import time
import json
import sys
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings()

class Nessus():
    def __init__(self, access_key, secret_key, base_url=None):
        if access_key == None or secret_key == None:
            raise ValueError("access_key and secret_key are required")
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'https://localhost:8834'
        self.headers = {
            'X-ApiKeys': f'accessKey={access_key}; secretKey={secret_key}',
            'Content-Type': 'application/json'
        }

    def get_session(self):
        url = f"{self.base_url}/session"
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            return True
        else:
            return False

    def list_scans(self):
        url = f"{self.base_url}/scans"
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            scans = response.json()['scans']
            return scans
        else:
            return None

    def export_request(self, scan_id):
        url = f"{self.base_url}/scans/{scan_id}/export"
        data = {
            "format": "nessus"
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data), verify=False)
        if response.status_code == 200:
            file_id = response.json()['file']
            return file_id
        else:
            return None

    def export_status(self, scan_id, file_id):
        url = f"{self.base_url}/scans/{scan_id}/export/{file_id}/status"
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            status = response.json()['status']
            return status
        else:
            return None

    def export_download(self, scan_id, file_id, file_name):
        url = f"{self.base_url}/scans/{scan_id}/export/{file_id}/download"
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)
            return True
        else:
            return None

if __name__ == "__main__":
    load_dotenv()
    NESSUS_BASE_URL = os.getenv('NESSUS_BASE_URL')
    NESSUS_ACCESS_KEY = os.getenv('NESSUS_ACCESS_KEY')
    NESSUS_SECRET_KEY = os.getenv('NESSUS_SECRET_KEY')
    nessus = Nessus(NESSUS_ACCESS_KEY, NESSUS_SECRET_KEY, base_url=NESSUS_BASE_URL)
    ret = nessus.get_session()
    print(f"session: {ret}")
    if not ret:
        sys.exit(1)
    scans = nessus.list_scans()
    for scan in scans:
        print(f"{scan['id']}: {scan['name']}")

    scan_id = 44
    file_id = nessus.export_request(scan_id)
    if file_id == None:
        sys.exit(1)

    while True:
        status = nessus.export_status(scan_id, file_id)
        if status == "ready":
            print(f"status: {status}  ")
            break
        else:
            print(f"status: {status}", end="\r")
        time.sleep(5)

    file_name = "scan_results.nessus"
    ret = nessus.export_download(scan_id, file_id, file_name)
    if ret:
        print(f"Downloaded {file_name}")