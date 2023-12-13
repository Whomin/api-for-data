import requests
from tabulate import tabulate
import pandas as pd
import os
import csv
base_url = "https://gitlab.com/api/v4"
offset = 0
bearer_token = "glpat--VYH3zwqei8DXHcmNSps"
#bearer_token = os.environ.get('GITLAB_TOKEN')
headers = {"Authorization": f"Bearer {bearer_token}"}
group_ids = [7786522] #7786522 7786194
# all_projects = []
# name_project = []
project_ids = []
#pipeline_ids = []
project_details = []
docker_scout = ['docker_scout_uat','docker_scout_prd' ,'docker_scout_dev']
qualys_sensor = ['qualys_sensor_uat' ,'qualys_sensor_prt' ,'qualys_sensor_dev']

page = 1


for group_id in group_ids:
    print(group_id)
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
            #project_ids_clean = list(dict.fromkeys(project_ids))
            #print(len(project_ids_clean))
            print(len(project_ids))
            print(project_ids)
            page += 1
    
    for find_project_id in project_ids:
        page = 1
        project_id = find_project_id['project_id']
        while True:
            params = {"page": page, "per_page": 100}
            pipeline_response = requests.get(f"{base_url}/projects/{project_id}/pipelines", headers=headers, params=params)

            if pipeline_response.status_code == 200:
                pipelines = pipeline_response.json()
                if not pipelines:
                    project_details.append({
                        "project_id": project_id,
                        "project_name": find_project_id['project_name'],
                        "pipeline_status": "don't have pipeline",
                        "CheckMarx": 0 ,     
                        "docker_scout": 0 ,
                        "qualys_sensor": 0   
                    })
                    print(f"project ID {project_id} not have pipeline")
                    break
                
                if len(pipelines) != 0 :
                    for find_pipeline_status in pipelines: #loop for find pipeline status
                        pipeline_status = find_pipeline_status['status']
                    latest_pipeline_id = pipelines[0]['id']
                    job_response = requests.get(f"{base_url}/projects/{project_id}/pipelines/{latest_pipeline_id}/jobs", headers=headers)

                    if job_response.status_code == 200:
                        jobs = job_response.json()
                        checkmarx_list = []
                        docker_scout_list =[]
                        qualys_sensor_list = []

                        for job in jobs:
                            if job['name'] == 'CheckMarx' :
                                checkmarx_list.append(job['name'])
                            #jobs_names.append(job['name'])
                            if job['name'] in docker_scout:
                                docker_scout_list.append(job['name'])
                            
                            if job['name'] in qualys_sensor :
                                qualys_sensor_list.append(job['name'])
                                         
                        project_details.append({
                            "project_id": project_id,
                            "project_name": find_project_id['project_name'],
                            "pipeline_status": pipeline_status,
                            "CheckMarx": len(checkmarx_list) ,     
                            "docker_scout": len(docker_scout_list) ,
                            "qualys_sensor": len(qualys_sensor_list)
                        })
                        print(f'project {project_id} have {checkmarx_list} & {docker_scout_list} & {qualys_sensor_list}')
                        break

                        # if len(jobs_names) != 0 and len(docker_scout) != 0 and len(qualys_sensor) !=0 : #('CheckMarx' in jobs_names)
                        #     project_details.append({
                        #         "project_id": project_id,
                        #         "project_name": find_project_id['project_name'],
                        #         "pipeline_status": pipeline_status,
                        #         "CheckMarx": 1 ,     
                        #         "docker_scout": 1,
                        #         "qualys_sensor": 1
                        #     })
                            
                        #     print(f'project {project_id} have CheckMarx & Docker scout & qualys sensor')
                        #     break
                        
                        # if len(jobs_names) != 0 and len(docker_scout) == 0 and len(qualys_sensor) !=0 : #('CheckMarx' in jobs_names)
                        #     project_details.append({
                        #         "project_id": project_id,
                        #         "project_name": find_project_id['project_name'],
                        #         "pipeline_status": pipeline_status,
                        #         "CheckMarx": 1 ,     
                        #         "docker_scout": 0,
                        #         "qualys_sensor": 1
                        #     })
                            
                        #     print(f"project {project_id} have CheckMarx & qualys sensor ,don't have Docker scout")
                        #     break
                        
                        # if len(jobs_names) != 0 and len(docker_scout) != 0 and len(qualys_sensor) == 0 : #('CheckMarx' in jobs_names)
                        #     project_details.append({
                        #         "project_id": project_id,
                        #         "project_name": find_project_id['project_name'],
                        #         "pipeline_status": pipeline_status,
                        #         "CheckMarx": 1 ,     
                        #         "docker_scout": 1,
                        #         "qualys_sensor": 0
                        #     })
                            
                        #     print(f"project {project_id} have CheckMarx & Docker scout ,don't have qualys sensor")
                        #     break
                        
                        # if len(jobs_names) == 0 and len(docker_scout) != 0 and len(qualys_sensor) !=0 : #('CheckMarx' in jobs_names)
                        #     project_details.append({
                        #         "project_id": project_id,
                        #         "project_name": find_project_id['project_name'],
                        #         "pipeline_status": pipeline_status,
                        #         "CheckMarx": 0 ,     
                        #         "docker_scout": 1,
                        #         "qualys_sensor": 1
                        #     })
                            
                        #     print(f"project {project_id} have CheckMarx & Docker scout ,don't have qualys sensor")
                        #     break
                        
                        # if len(jobs_names) == 0 and len(docker_scout) == 0 and len(qualys_sensor) !=0 : #('CheckMarx' in jobs_names)
                        #     project_details.append({
                        #         "project_id": project_id,
                        #         "project_name": find_project_id['project_name'],
                        #         "pipeline_status": pipeline_status,
                        #         "CheckMarx": 0 ,     
                        #         "docker_scout": 0,
                        #         "qualys_sensor": 1
                        #     })
                            
                        #     print(f'project {project_id} have CheckMarx & Docker scout & qualys sensor')
                        #     break
                        
                        # if len(jobs_names) == 0 and len(docker_scout) != 0 and len(qualys_sensor) ==0 : #('CheckMarx' in jobs_names)
                        #     project_details.append({
                        #         "project_id": project_id,
                        #         "project_name": find_project_id['project_name'],
                        #         "pipeline_status": pipeline_status,
                        #         "CheckMarx": 0 ,     
                        #         "docker_scout": 1,
                        #         "qualys_sensor": 0
                        #     })
                            
                        #     print(f'project {project_id} have CheckMarx & Docker scout & qualys sensor')
                        #     break
                        
                        # if len(jobs_names) != 0 and len(docker_scout) == 0 and len(qualys_sensor) ==0 : #('CheckMarx' in jobs_names)
                        #     project_details.append({
                        #         "project_id": project_id,
                        #         "project_name": find_project_id['project_name'],
                        #         "pipeline_status": pipeline_status,
                        #         "CheckMarx": 1 ,     
                        #         "docker_scout": 0,
                        #         "qualys_sensor": 0
                        #     })
                            
                        #     print(f'project {project_id} have CheckMarx & Docker scout & qualys sensor')
                        #     break
                    
                        # else :
                        #     project_details.append({
                        #         "project_id": project_id,
                        #         "project_name": find_project_id['project_name'],
                        #         "pipeline_status": pipeline_status,
                        #         "CheckMarx": 0 ,   
                        #         "docker_scout": 0,
                        #         "qualys_sensor": 0   
                        #     })
                        #     print(jobs)
                        #     print(f"project {project_id} don't have CheckMarx & Docker scout & qualys sensor")
                        #     break                       
                    else:
                        print(f"Failed to fetch jobs for project ID {project_id}. Status code: {job_response.status_code}")
                page += 1
                
            else:
                print(f"Failed to fetch pipelines for project ID {project_id}. Status code: {pipeline_response.status_code}")
                break

#print(project_ids)
#page = 1

# for project_id_S in project_ids :
#     print(project_id_S)
#     params = {"include_subgroups": True,"page": page , "per_page": 100 }
#     pipeline_response = requests.get(f"{base_url}/projects/{project_id_S}/pipelines", headers=headers, params=params)
#     if pipeline_response.status_code == 200 :
#         pipeline_state = pipeline_response.json()
#         if len(pipeline_state) != 0 :
#             latest_pipeline_id = pipeline_state[0]['id']
#             job_response = requests.get(f"{base_url}/projects/{project_id_S}/pipelines/{latest_pipeline_id}/jobs", headers=headers, params=params)
#             if job_response.status_code == 200 :
#                 jobs = job_response.json()
#                 for job in jobs :
#                     if job['name'] == 'CheckMarx' :
#                         pipeline_id.append(job['name'])
#                     else : print('error')
#         else : print('no!')
#     else : print(f'this project {project_id_S} has issue {job_response.status_code}')
        
#https://gitlab.com/api/v4/projects/{project id}/pipelines/{pipeline id}/jobs
# print(pipeline_id)
# print(len(pipeline_id))

#52230076 2023-11-16T10:13:20.962Z

print(project_details)
print(len(project_details))

# project_data = []
# branch_count = {}
# for project in project_details:
#     if project["path_with_namespace"].startswith("tltdeveloper/inhouse") or project["path_with_namespace"].startswith("tltdeveloper/infra") or project["path_with_namespace"].startswith("tltdeveloper/mobile"):
#     # if project["path_with_namespace"].startswith("tltdeveloper") :
#         branches_response = requests.get(f"{base_url}/projects/{project['id']}/repository/branches", headers=headers)
#         branches = branches_response.json()
#         branch_count[project["name"]] = len(branches)
#         branch_names = []
#         max_lines = 0
#         for branch in branches:
#             lines_count = 0
#             response = requests.get(f"{base_url}/projects/{project['id']}/repository/tree?ref={branch['name']}", headers=headers)
#             files = response.json()
#             for file in files:
#                 # print(type(file))
#                 # print(file)
#                 if type(file) == dict:
#                   if file["type"] == "blob" and not file["name"].endswith(".md"):
#                     file_response = requests.get(f"{base_url}/projects/{project['id']}/repository/files/{file['path']}/raw?ref={branch['name']}", headers=headers)
#                     lines = len(file_response.text.split("\n"))
#                     lines_count += lines
#             if lines_count > max_lines:
#                 max_lines = lines_count
#                 branch_names = [branch["name"]]
#             elif lines_count == max_lines:
#                 branch_names.append(branch["name"])
#         if max_lines > 0:
#             pipeline_response = requests.get(f"{base_url}/projects/{project['id']}/pipelines", headers=headers)
#             pipelines = pipeline_response.json()
#             if len(pipelines) > 0:
#                 project_data.append([project["name"], project["path_with_namespace"], ", ".join(branch_names), max_lines])
# distinct_project_list = []
# for project in project_data:
#     if project[0] not in distinct_project_list:
#         distinct_project_list.append(project[0])
# sum_of_distinct_projects = len(distinct_project_list)
# df = pd.DataFrame(project_details, columns=["Project Name", "Project Path", "Branch Name", "Line of Code"])
# df.loc[len(df)] = ["Total Projects", sum_of_distinct_projects, "", ""]
# ###export to csv
# # df.to_csv("tltdeveloper-infra3.csv", index=False)
# print(tabulate(df, headers=["Project Name", "Project Path", "Branch Name", "Line of Code"]))
# # Convert the values in the 'Line of Code' column to integers, but only if they are not empty
# df['Line of Code'] = df['Line of Code'].apply(lambda x: int(x) if x else 0)
# # Add this line to get the sum of line of code and store it in a variable
# total_line_of_code = df['Line of Code'].sum()
# # Display the total line of code
# print(f"Total line of code: {total_line_of_code}")
# print(f"Total projects: {sum_of_distinct_projects}")

headers = project_details[0].keys()

with open('data', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    
    # Write headers
    writer.writeheader()
    
    # Write data rows
    writer.writerows(project_details)

print(f"CSV file data has been created successfully.")