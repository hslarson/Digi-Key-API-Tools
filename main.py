from digikey import *

# API credentials
API_CLIENT_ID = "Y619hciOaxJ7WrkQilA97c7ramApEnz1"
API_CLIENT_SECRET = "n5AMnll87yMMDTxW"

# Get Digi-Key OAuth token
token = get_oauth_token(API_CLIENT_ID, API_CLIENT_SECRET)
auth = {
    "Authorization" : f"Bearer {token}",
    "X-DIGIKEY-Client-Id" : API_CLIENT_ID
}

# Load BOM data
headers, data = read_csv("my_bom.bom")

# Get part numbers
pn_idx = headers.index("Manufacturer PN")
part_nums = [r[pn_idx] for r in data]

# Set up output CSV
output_file = "output.csv"
write_csv_row(output_file, ["Part Number", "Min Operating Temp.", "Max Operating Temp."])

# Iterate through parts
for part in part_nums:
    print(f"Part Number: {part} --> ", end="")

    parameters = get_part_parameters(auth, part)
    if parameters:
        temp_range = get_operating_temp(parameters)
        if temp_range:
            print(f"{temp_range[0]}°C ~ {temp_range[1]}°C")
            write_csv_row(output_file, [part, *temp_range])
            continue
        else:
            print("Lookup Failed, Operating Temperature Not Available")
    else:
        print("Lookup Failed, Part Not Found")
    
    write_csv_row(output_file, [part, "", ""])
