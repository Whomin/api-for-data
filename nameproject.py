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
page = 1

for group_id1 in group_ids:
    while True :
        params = {"include_subgroups": True,"page": page , "per_page": 100 }
        response = requests.get(f"{base_url}/groups/{group_id1}/projects", headers=headers, params=params)
        if response.status_code == 200:
            projects = response.json()
            if len(projects) == 0 :
                break
            for project in projects:
                all_projects.append(project)
                name_project.append(project["name"])
                #print(project["name"])
            #print(project)
            print('process id ',group_id1,' is done')
            page += 1
            

print(len(name_project))

