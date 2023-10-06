# import json
# data1 = []
# with open('grafana.json', 'r') as f:
#     data = json.load(f)
# for severity in data['findings']:
    # print(severity)
# for i in range(1,len(data['findings'])):
#     for severity in data['findings']:
#         print(f"A{i} = {severity['severity']}")
#     print(severity['severity'])
# print(data['findings']['name'])
# for attributes in data['findings']:
#     for key in attributes['attributes']:
#         print(key['key'], key['value'])
# for key, value in data['findingSeverityCounts'].items():
#     print(key,value)
# for vul_name in data['findings']:
#     print(vul_name)
#     if vul_name['severity'] == "MEDIUM" or vul_name['severity'] == "HIGH":
#         data1.append(vul_name)      
# print(data1)

# for vul in data1:
#     max_key_length = max(len(key) for key in vul.keys())
#     # print(vul)
#     for key, value in vul.items():
#         formatted_key = key.ljust(max_key_length)
#         formatted_value = str(value).rjust(5)  # Adjust the width as needed

#         print(f"{formatted_key}:\t\t{formatted_value}")
# strg = f"\t\t\t\t\t\t\t\tVulnerability Scan Report for Image: grafana\n"
# strg += f"\t\t\t\t\t\t\t------------------------------------------------------------\n"
# strg += f"  ATTRIBUTES\n"
# strg += f" ------------"

# print(strg)

# data = {
#     'HIGH': 1,
#     'MEDIUM': 25,
#     'LOW': 20,
#     'UNDEFINED': 17,
#     'INFORMATIONAL': 58
# }

# max_key_length = max(len(key) for key in data.keys())
# for key, value in data.items():
#     formatted_key = key.ljust(max_key_length)
#     formatted_value = str(value).rjust(5)  # Adjust the width as needed
    
#     print(f"{formatted_key}: {formatted_value}")


# from datetime import datetime

# input_string = "2023-03-13T23:53:17+05:30"
# input_datetime = datetime.strptime(input_string, "%Y-%m-%dT%H:%M:%S%z")

# formatted_datetime = input_datetime.strftime("%B %d, %Y %I:%M %p")
# print(formatted_datetime)






# import pandas as pd

# # Create a sample DataFrame
# data = {'Name': ['John', 'Alice', 'Bob'],
#         'Age': [25, 30, 35]}

# df = pd.DataFrame(data)

# # Specify the Excel file path where you want to save your DataFrame
# excel_file_path = 'my_dataframe.xlsx'

# # Export the DataFrame to Excel
# df.to_excel(excel_file_path, index=False)  # Set index=False to exclude the index column in the Excel file
# with pd.ExcelWriter('output.xlsx',mode='a') as writer:
#     df.to_excel(excel_file_path, index=False)

import yaml

INPUT_FILE = "input.yaml"

def read_input_file(file_name):
    RELEASE_NAME = []
    IMAGE_NAME = []
    REPO_NAME = []
    IMAGE_TAG = []
    with open(file_name, "r") as f:
        data = yaml.safe_load(f)  
    # for component in data:
        # print(component['version'])
    RELEASE_NAME += [f"release-{data['release']['version']}"]
    for component in data['images']:
        # print(component)
        IMAGE_NAME += [component["image"]]
        REPO_NAME += [component["repository"]]
        IMAGE_TAG += [component["tag"]]
    ALL_IMG_INFO = [RELEASE_NAME, IMAGE_NAME,REPO_NAME,IMAGE_TAG]
    return ALL_IMG_INFO
    # print(RELEASE_NAME)
    # print(IMAGE_NAME)

# read_input_file(INPUT_FILE)

ALL_IMG = read_input_file(INPUT_FILE)
RELEASE = ALL_IMG[0][0]

print(RELEASE)
# print(ALL_IMG)

for i in range(len(ALL_IMG[1])):
        IMG_NAME = ALL_IMG[1][i]
        REPO = f"{ALL_IMG[2][i]}/{IMG_NAME}"
        TAG = ALL_IMG[3][i]
        # print(i)
        print(IMG_NAME, REPO, TAG)