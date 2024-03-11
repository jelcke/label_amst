import json
import os
import shutil
import cups
import sys

def check_printer_status():
    conn = cups.Connection()

    printers = conn.getPrinters()
    printer_name = 'Zebra-Technologies-ZTC-GK420d'  # replace with your printer's name

    if printer_name not in printers:
        print(f'Error: Printer {printer_name} is not found.')
        sys.exit(1)

    printer_attributes = conn.getPrinterAttributes(printer_name)

    if printer_attributes["printer-state"] != 3:  # 3 means idle
        print(f'Error: Printer {printer_name} is not online.')
        sys.exit(1)

    print(f'Printer {printer_name} is online.')

def generate_label(address):
        zpl = f"""
    ^XA

    ^FX Top section with logo, name and address.
    ^CF0,60
    ^FO50,50^GB100,100,100^FS
    ^FO75,75^FR^GB100,100,100^FS
    ^FO93,93^GB40,40,40^FS
    ^FO220,50^FDAmstelbooks^FS
    ^CF0,30
    ^FO220,115^FDRoute du Moulin du Ranc 550^FS
    ^FO220,155^FD07240 Verrnoux-en-Vivarais^FS
    ^FO220,195^FDFrance^FS
    ^FO50,250^GB700,3,3^FS

    ^FX Second section with recipient address and permit information.
    ^CFA,30

    ^CI28
    ^FH
    ^FO50,300^FDExpédier à / destination :^FS  
    ^FO50,360^FD{address['name']}^FS
    ^FO50,400^FD{address['street']}^FS
    ^FO50,440^FD{address['city']} {address['postal_code']}^FS
    ^FO50,480^FD{address['country']}^FS
    ^FO50,540^FD{address['phone']}^FS


    ^CFA,15

    ^FX Fourth section (the bottom box).
    ^FO50,900^GB700,250,3^FS
    ^CF0,40

    ^FO100,960^FDHandle with care^FS
    ^FO100,1000^FDContains books^FS
    ^FO100,1040^FDContient des livres^FS

    ^XZ
    """
        return zpl

def process_json_file(json_file_path):
    with open(json_file_path, 'r') as f:
        addresses = json.load(f)

    for index, address in enumerate(addresses):
        label_zpl = generate_label(address)
        label_file_path = f'./labels/label_{os.path.basename(json_file_path).replace(".json", "")}_{index}.zpl'
        with open(label_file_path, 'w') as f:
            f.write(label_zpl)
        os.system(f'/usr/bin/lprint submit -d ZebraGK420d {label_file_path}')

def main():
    check_printer_status()
    json_folder = './json'
    processed_folder = './json/processed'

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            json_file_path = os.path.join(json_folder, json_file)
            process_json_file(json_file_path)
            shutil.move(json_file_path, os.path.join(processed_folder, json_file))

if __name__ == "__main__":
    main()
