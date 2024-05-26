import json
import os

def parse_address_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read().strip()
    
    addresses = data.split('\n\n')
    
    address_list = []
    for address in addresses:
        lines = [line.strip() for line in address.split('\n') if line.strip()]
        
        if len(lines) < 5:
            raise ValueError(f"Unexpected address format: {address}")

        name = lines[0]
        street = lines[1]
        city = lines[2]
        country = lines[3]
        phone = lines[4]
        
        address_dict = {
            "name": name,
            "street": street,
            "city": city,
            "country": country,
            "phone": phone
        }
        address_list.append(address_dict)
    
    return address_list

def convert_to_json(address_list):
    return json.dumps(address_list, indent=4, ensure_ascii=False)

def save_to_json_file(json_data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(json_data)

if __name__ == "__main__":
    input_file = 'addresses.txt'
    output_file = 'json/addresses.json'
    
    try:
        address_list = parse_address_file(input_file)
        json_data = convert_to_json(address_list)
        save_to_json_file(json_data, output_file)
        print(f"Addresses have been successfully converted to JSON and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
