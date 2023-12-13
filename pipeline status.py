import requests
from tabulate import tabulate
import pandas as pd
import os
base_url = "https://gitlab.com/api/v4"
offset = 0
bearer_token = "glpat--VYH3zwqei8DXHcmNSps"
#bearer_token = os.environ.get('GITLAB_TOKEN')
headers = {"Authorization": f"Bearer {bearer_token}"}
group_ids = [7786194]
all_projects = []
name_project = []
status_success_project = []
status_unsuccess_project = []
page = 1
        
for group_id in group_ids:
    while True :
        params = {"include_subgroups": True,"page": page , "per_page": 100 }
        response = requests.get(f"{base_url}/groups/{group_id}/projects", headers=headers, params=params)
        if response.status_code == 200:
            projects = response.json()
            if len(projects) == 0 :
                break
            for project in projects:
                project_id = project["id"]
                #project_id = int(projects["id"])
            status = requests.get(f"{base_url}/projects/{project_id}/pipelines", headers=headers) #check pipeline status form pipeline id 
            if status.status_code == 200:
                projects = status.json()
                if len(projects) == 0 :
                    break
                for project in projects: #loop for find pipeline status
                    if project['status'] == 'success' :
                        status_success_project.append(project['status'])
                    else : 
                        status_unsuccess_project.append(project['status'])
            print('process id ',group_id,' is done')
            page += 1

print((status_success_project))
print('=============================================================')
print((status_unsuccess_project))
print((len(status_success_project)+len(status_unsuccess_project)))
print('success rate',(len(status_success_project) /(len(status_success_project)+len(status_unsuccess_project))) * 100, 'percent')
