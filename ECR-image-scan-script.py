#!/bin/python3

####################################################################################
# This Script is developed to run Image scan in AWS ECR and Upload the result in local
# as text file
# ####################################################################################
import os
import subprocess
import yaml
import json
from datetime import datetime

REGION = "us-west-2"

REGISTRY_ID = "xxxxxxx564"

PROFILE = "my-aws"
INPUT_FILE = "input02.yaml"

IMG_NAME = ""
REPO = ""

TAG = ""

# aws ecr describe-image-scan-findings --registry-id xxxxxxx564 --repository-name external-images01/image01 --image-id imageTag=0.24.0 --region us-west-2 --query imageScanFindings.findings --profile my-aws --output table

# This function takes info from input.yaml file Taking info from input file
def read_input_file(file_name):
    IMAGE_NAME = []
    REPO_NAME = []
    IMAGE_TAG = []
    with open(file_name, "r") as f:
        data = yaml.safe_load(f)  
       
    for component in data:
        # print(component)
        IMAGE_NAME += [data[component]["image"]]
        REPO_NAME += [data[component]["repository"]]
        IMAGE_TAG += [data[component]["tag"]]
    ALL_IMG_INFO = [IMAGE_NAME,REPO_NAME,IMAGE_TAG]
    return ALL_IMG_INFO


# This function will create json file of vulnerabilities scanning for given images in input file
def image_scan_info():
    get_cmd = f"aws ecr describe-image-scan-findings --registry-id {REGISTRY_ID} --repository-name {REPO} --image-id imageTag={TAG} --region {REGION} --query imageScanFindings --profile {PROFILE} --output json"
    get_scan = subprocess.run(get_cmd, shell=True, capture_output=True, text=True)
    if get_scan.returncode == 0:
        # with open(f'{read_input_file(INPUT_FILE)[0][i]}.json', 'w') as fi:
        #     get_scan = subprocess.run(get_cmd, shell=True, stdout=fi, text=True)
        data = json.loads(get_scan.stdout)
                
    get_scan_results = json.dumps(data, indent=2)
    return get_scan_results

def get_report():
    result = ""
    data = []
    temp_data = json.loads(image_scan_info())
    for severity in temp_data['findings']:
        if severity['severity'] == "MEDIUM" or severity['severity'] == "HIGH":
            data.append(severity)
    result += f"\t\t\t\t\t\t\t\t# VULNERABILITY SCAN REPORT FOR IMAGE: {IMG_NAME}:{TAG}\n\n"
    result += f"\t\t\t\t\t\t\t\t-----------------------------------------------------------\n\n"
    input_string = temp_data['imageScanCompletedAt']
    input_datetime = datetime.strptime(input_string, "%Y-%m-%dT%H:%M:%S%z")
    formatted_datetime = input_datetime.strftime("%B %d, %Y %I:%M %p")
    result += f"\t\t\t\t\t\t\t\t\tScan Completes Time:\t\t{formatted_datetime}\n\n"
    result += f"## VULNERABILITY COUNTS\n----------------------------\n\n"
    
    
    max_key_length = max(len(key) for key in temp_data['findingSeverityCounts'].keys())
    for key, value in temp_data['findingSeverityCounts'].items():
        if key == "CRITICAL" or key == "HIGH" or key == "MEDIUM":
            formatted_key = key.ljust(max_key_length)
            formatted_value = str(value).rjust(5)
            result += f"{formatted_key}:\t\t{formatted_value}\n\n"
        
    result += f"----------------------------\n\n"
    
    for vul_name in data:
        result += f"## NAME:\t\t\t\t{vul_name['name']}\n"
        if "description" in vul_name.keys():
            result += f"## DESCRIPTION:\t\t\t{vul_name['description']}\n"
        result += f"## SEVERITY:\t\t\t{vul_name['severity']}\n"
        result += f"## URI:\t\t\t\t\t{vul_name['uri']}\n\n"
        result += f" ## ATTRIBUTES\n"
        result += f" --------------\n\n"
        
        for atrribute in vul_name['attributes']:
            result += f"{atrribute['key']}:\t\t{atrribute['value']}\n"
            # max_key_length = max(len(key) for key in atrribute.keys())
            # for key, value in atrribute.items():
            #     formatted_key = atrribute['key'].ljust(max_key_length)
            #     formatted_value = str(atrribute['value']).rjust(5)
            #     result += f"{formatted_key}:\t\t{formatted_value}\n"
        result += f"---------------------------------------------------------------------------------------------------------------------------\n\n\n"
    result += f"\n\n\n\n\n"
    return result
    
def create_vul_file():
    path = './vul.txt'
    check_file = os.path.isfile(path)
    if not check_file:
        with open('image-vulenrability.txt', 'a') as f:
            vul_info = f.write(get_report())
            return vul_info
    else:
        print("You already have the same filename exists. Please delete the file and rerun the script")
        

def get_main():
    global IMG_NAME, REPO, TAG
    for i in range(len(read_input_file(INPUT_FILE)[0])):
        IMG_NAME = read_input_file(INPUT_FILE)[1][i]
        REPO = f"{read_input_file(INPUT_FILE)[2][i]}/{IMG_NAME}"
        TAG = read_input_file(INPUT_FILE)[3][i]
        
        image_scan_info()
        get_report()
        create_vul_file()
  
  
get_main()