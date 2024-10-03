import requests
import csv
import re


# Get OAuth token
def get_oauth_token(client_id, client_setret):
    url = 'https://api.digikey.com/v1/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_setret,
    }

    response = requests.post(url, headers=headers, data=data)
    assert response.ok, "Failed to get OAuth token"
    return response.json()['access_token']


# Load BOM csv
def read_csv(filepath):
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        
        data = []
        for row in csv_reader:
            data.append(row)

    return headers, data


# Write a csv row
def write_csv_row(filepath, row):
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(row)


# Get a list of Digi-Key part parameters
def get_part_parameters(headers, part_number):
    if len(part_number.strip()) == 0:
        return None

    url = f"https://api.digikey.com/products/v4/search/{part_number}/productdetails"

    response = requests.get(url, headers=headers)
    if not response.ok:
        return None

    return response.json()["Product"]["Parameters"]


# Return a tuple containing the min and max operating temperature
def get_operating_temp(parameter_list):
    for param in parameter_list:
        # Extract operating temp.
        if param['ParameterId'] == 252:
            matches = re.findall(r'-?\d+', param['ValueText'])
            if len(matches) == 2:
                return tuple(matches)
            elif len(matches) == 1:
                return ("", matches[0])
    else:
        return None
