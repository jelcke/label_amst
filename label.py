import json
import os



def generate_label(data):
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
^FO50,360^FD{data['name']}^FS
^FO50,400^FD{data['street']}^FS
^FO50,440^FD{data['city']} {data['postalCode']}^FS
^FO50,480^FD{data['country']}^FS
^FO50,540^FD{data['phone']}^FS


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

# def main():
#     with open('addresses.json', 'r') as f:
#         addresses = json.load(f)

#     for address in addresses:
#         label = generate_label(address)
#         print(label)

# if __name__ == "__main__":
#     main()


def main():
    with open('./json/addresses.json', 'r') as f:
        addresses = json.load(f)

    for address in addresses:
        label = generate_label(address)
        with open('./labels/label.zpl', 'w') as f:
            f.write(label)
        os.system('/usr/bin/lprint submit -d ZebraGK420d ./labels/label.zpl')
        # /usr/bin/lprint add -d ZebraGK420d -v usb://Zebra%20Technologies/ZTC%20GK420d?serial=28J133302347 -m zpl_4inch-300dpi-dt

if __name__ == "__main__":
    main()
