#!/usr/bin/env python3
# Author: Human beings feat. ChatGPT with GitHub Copilot
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import urllib3
urllib3.disable_warnings()

class DefectDojo():
    def __init__(self, api_key, base_url=None):
        if api_key == None:
            raise ValueError("api_key is required")
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'http://localhost:8080/api/v2/'
        self.headers = {
            'Authorization': f'Token {api_key}',
            'Accept': 'application/json'
        }

    def list_products(self):
        url = f"{self.base_url}products/"
        res = requests.get(url, headers=self.headers, verify=False)
        if res.status_code == 200:
            return res.json()
        else:
            return None

    def import_scan(self, product_name, file_path, scan_type="Tenable Scan"):
        url = f"{self.base_url}import-scan/"
        files = {
            'file': open(file_path, 'rb')
        }
        data = {
            'product_name': product_name,
            'scan_type': scan_type,
            'engagement_name': datetime.now().strftime("%a, %d %b %Y %H:%M:%S"),
            'auto_create_context': True
            #'minimum_severity': 'Info', # option
            #'active': active, # option
            #'verified': verified, # option
        }
        res = requests.post(url, headers=self.headers, files=files, data=data, verify=False)
        if res.status_code == 201:
            return res.json()
        else:
            return None

if __name__ == "__main__":
    load_dotenv()
    DEFECTDOJO_BASE_URL = os.getenv('DEFECTDOJO_BASE_URL')
    DEFECTDOJO_API_KEY = os.getenv('DEFECTDOJO_API_KEY')
    file_path = "scan_results.nessus"
    dd = DefectDojo(DEFECTDOJO_API_KEY, base_url=DEFECTDOJO_BASE_URL)
    res = dd.import_scan('test', file_path, 'Tenable Scan')
    if res:
        print(res)
    else:
        print("Failed to import scan")