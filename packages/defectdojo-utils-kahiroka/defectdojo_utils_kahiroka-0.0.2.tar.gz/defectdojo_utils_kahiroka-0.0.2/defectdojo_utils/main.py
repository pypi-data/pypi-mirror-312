#!/usr/bin/env python3
# Author: Human beings feat. ChatGPT with GitHub Copilot
import os
import sys
import time
import argparse
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from defectdojo_utils.nessus import Nessus
from defectdojo_utils.defectdojo import DefectDojo

def getArgs():
    usage = 'python3 {}'.format(__file__)
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-i', '--input', dest='input', default=None, help='INPUT filename')
    parser.add_argument('-o', '--output', dest='output', default=None, help='OUTPUT filename')
    parser.add_argument('--list-nessus', dest='list_nessus', action='store_true', help='list nessus SCAN_ID')
    parser.add_argument('--export-nessus', dest='scan_id', default=None, help='export nessus SCAN_ID to OUTPUT(.nessus)')
    parser.add_argument('--list-defectdojo', dest='list_defectdojo', action='store_true', help='list defectdojo PRODUCT_NAME')
    parser.add_argument('--import-defectdojo', dest='product_name', default=None, help='import defectdojo PRODUCT_NAME from INPUT as SCAN_TYPE')
    parser.add_argument('--scan-type', dest='scan_type', default="Tenable Scan", help='SCAN_TYPE: Tenable Scan, Scout Suite Scan')
    parser.add_argument('-e', '--env', dest='env', default=None, help='path to environment variable file')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='debug mode')
    return parser.parse_args()

def main():
    args = getArgs()

    load_dotenv(args.env)
    DEFECTDOJO_BASE_URL = os.getenv('DEFECTDOJO_BASE_URL')
    DEFECTDOJO_API_KEY = os.getenv('DEFECTDOJO_API_KEY')
    NESSUS_BASE_URL = os.getenv('NESSUS_BASE_URL')
    NESSUS_ACCESS_KEY = os.getenv('NESSUS_ACCESS_KEY')
    NESSUS_SECRET_KEY = os.getenv('NESSUS_SECRET_KEY')

    if args.list_nessus:
        nessus = Nessus(NESSUS_ACCESS_KEY, NESSUS_SECRET_KEY, base_url=NESSUS_BASE_URL)
        scans = nessus.list_scans()
        for scan in scans:
            print(f"{scan['id']}: {scan['name']}")

    elif args.scan_id and args.output:
        nessus = Nessus(NESSUS_ACCESS_KEY, NESSUS_SECRET_KEY, base_url=NESSUS_BASE_URL)
        scan_id = args.scan_id
        file_id = nessus.export_request(scan_id)
        if file_id == None:
            print("scan id not found")
            sys.exit(1)

        while True:
            status = nessus.export_status(scan_id, file_id)
            if status == "ready":
                print(f"status: {status}  ")
                break
            else:
                print(f"status: {status}", end="\r")
            time.sleep(5)

        file_name = args.output
        ret = nessus.export_download(scan_id, file_id, file_name)
        if ret:
            print(f"Downloaded {file_name}")
        else:
            print("Failed to download scan")
  
    elif args.list_defectdojo:
        dd = DefectDojo(DEFECTDOJO_API_KEY, base_url=DEFECTDOJO_BASE_URL)
        products = dd.list_products()
        if 'results' in products:
            for product in products['results']:
                print(f"{product['id']}: {product['name']}")
     
    elif args.product_name and args.input and args.scan_type:
        dd = DefectDojo(DEFECTDOJO_API_KEY, base_url=DEFECTDOJO_BASE_URL)
        res = dd.import_scan(args.product_name, args.input, args.scan_type)
        if res:
            if args.debug:
                print(res)
            else:
                print("Successfully imported scan")
        else:
            print("Failed to import scan")

if __name__ == "__main__":
    main()
