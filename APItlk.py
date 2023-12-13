import requests
from tabulate import tabulate
import pandas as pd
import os
import csv
from datetime import datetime
base_url = "https://gitlab.com/api/v4"
offset = 0
bearer_token = "glpat--VYH3zwqei8DXHcmNSps"
#bearer_token = os.environ.get('GITLAB_TOKEN')
project_ids = []
project_details = []
docker_scout = ['docker_scout_uat','docker_scout_prd' ,'docker_scout_dev']
qualys_sensor = ['qualys_sensor_uat' ,'qualys_sensor_prt' ,'qualys_sensor_dev']
headers = {"Authorization": f"Bearer {bearer_token}"}
group_ids = [7786194] #7786522 7786194
page = 1

for group_id in group_ids:
    print(group_id) # check group id
    
    while True :
        params = {"include_subgroups": True,"page": page , "per_page": 100 }
        response = requests.get(f"{base_url}/groups/{group_id}/projects", headers=headers, params=params)
        
        if response.status_code == 200:
            projects = response.json()
            
            if len(projects) == 0 :
                break
            
            for project in projects:
                if project['id'] not in project_ids :
                    project_ids.append({
                        'project_id' : project['id'],
                        'project_name' : project['name']
                        })
            print('process id ',group_id,' is done')
            #print(len(project_ids))
            #print(project_ids)
            page += 1
    
    for find_project_id in project_ids:
        page = 1
        project_id = find_project_id['project_id']
        while True:
            params = {"page": page, "per_page": 100}
            pipeline_response = requests.get(f"{base_url}/projects/{project_id}/pipelines", headers=headers, params=params)

            if pipeline_response.status_code == 200:
                pipelines = pipeline_response.json()
                
                # if project don't have pipeline
                if not pipelines:
                    project_details.append({
                        "project id": project_id,
                        "project name": find_project_id['project_name'],
                        "pipeline status": "don't have pipeline",
                        "scan status" : False,
                        "checkMarx": 0 ,     
                        "docker scout": 0 ,
                        "qualys sensor": 0 ,
                        "timestamp" : datetime.now()
                    })
                    print(f"project ID {project_id} not have pipeline")
                    break
                
                # if have pipeline
                if len(pipelines) != 0 :
                    for find_pipeline_status in pipelines: #loop for find pipeline status
                        pipeline_status = find_pipeline_status['status']
                    latest_pipeline_id = pipelines[0]['id']
                    job_response = requests.get(f"{base_url}/projects/{project_id}/pipelines/{latest_pipeline_id}/jobs", headers=headers)

                    if job_response.status_code == 200:
                        jobs = job_response.json() 
                        scan_status = False
                        checkmarx_list = 'disable' #clear list checkmarx
                        docker_scout_list = 'disable' #clear list docker
                        qualys_sensor_list = 'disable' #clear list qualys
 
                        #get checkmarx/docker/qualys if found in pipeline
                        for job in jobs:
                            if job['name'] == 'CheckMarx' :
                                checkmarx_list = 'enable'  # add checkmarx to checkmarx list if pipeline has a checkmarx

                            if job['name'] in docker_scout:
                                docker_scout_list = 'enable' # add docker scout to docker scout list if pipeline has a docker scout
                            
                            if job['name'] in qualys_sensor :
                                qualys_sensor_list = 'enable' # add qualys sensor to qualys sensor list if pipeline has a qualys sensor 
                                         
                        if (checkmarx_list == 'enable') & (docker_scout_list == 'enable') & (qualys_sensor_list == 'enable') :
                            scan_status = True
                                         
                        project_details.append({ # add value in to a project detait (id , name , status , checkmarx , docker scout , qualys)
                            "project id": project_id,
                            "project name": find_project_id['project_name'],
                            "pipeline status": pipeline_status,
                            "scan status" : scan_status,
                            "checkMarx": checkmarx_list ,     
                            "docker scout": docker_scout_list ,
                            "qualys sensor": qualys_sensor_list ,
                            "timestamp" : datetime.now()
                        })
                        print(f'project {project_id} have {checkmarx_list} & {docker_scout_list} & {qualys_sensor_list} & {scan_status}') # check in terminal
                        break
                    else:
                        print(f"Failed to fetch jobs for project ID {project_id}. Status code: {job_response.status_code}")
                page += 1
                
            else:
                print(f"Failed to fetch pipelines for project ID {project_id}. Status code: {pipeline_response.status_code}")
                break

# create csv for save data
headers = project_details[0].keys()

with open('dataforapi', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    
    # Write headers
    writer.writeheader()
    
    # Write data rows
    writer.writerows(project_details)

print(f"CSV file data has been created successfully.")