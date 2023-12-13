import requests
from tabulate import tabulate
import pandas as pd
import os
base_url = "https://gitlab.com/api/v4"
offset = 0
#bearer_token = "glpat-Aej-jGyTgnFAxDxmZFTJ"
bearer_token = "glpat--VYH3zwqei8DXHcmNSps"
#bearer_token = os.environ.get('GITLAB_TOKEN')
headers = {"Authorization": f"Bearer {bearer_token}"}
all_projects = []
name_project = []
page = 1

print('start')

# while len(all_projects) < 493 :
while True :
  group_id = 9527618
  params = {"include_subgroups": True,"page": page , "per_page": 100 }
  response = requests.get(f"{base_url}/groups/{group_id}/projects", headers=headers, params=params)
  if response.status_code == 200:
      projects = response.json()
      if len(projects) == 0 :
        break
      for project in projects:
        all_projects.append(project)
        name_project.append({"name": project["name"]})
    #   print(page)
      page += 1
# print("infra")
print(len(all_projects))

print('1')

page = 1
while True :
  group_id = 7786252
  params = {"include_subgroups": True,"page": page , "per_page": 100 }
  response = requests.get(f"{base_url}/groups/{group_id}/projects", headers=headers, params=params)
  if response.status_code == 200:
      projects = response.json()
      if len(projects) == 0 :
        break
      for project in projects:
        all_projects.append(project)
    #   print(page)
      page += 1
# print("infra + mobile")
print(len(all_projects))

print('2')

page = 1
while True :
  group_id = 7786271
  params = {"include_subgroups": True,"page": page , "per_page": 100 }
  response = requests.get(f"{base_url}/groups/{group_id}/projects", headers=headers, params=params)
  if response.status_code == 200:
      projects = response.json()
      if len(projects) == 0 :
        break
      for project in projects:
        all_projects.append(project)
    #   print(page)
      page += 1
# print("infra + mobile + inhouse")
print(len(all_projects))

print('3')
print(len(name_project))
print(name_project)

project_data = []
branch_count = {}
for project in all_projects:
    if project["path_with_namespace"].startswith("tltdeveloper/inhouse") or project["path_with_namespace"].startswith("tltdeveloper/infra") or project["path_with_namespace"].startswith("tltdeveloper/mobile"):
    # if project["path_with_namespace"].startswith("tltdeveloper") :
        branches_response = requests.get(f"{base_url}/projects/{project['id']}/repository/branches", headers=headers)
        branches = branches_response.json()
        branch_count[project["name"]] = len(branches)
        branch_names = []
        max_lines = 0
        for branch in branches:
            lines_count = 0
            response = requests.get(f"{base_url}/projects/{project['id']}/repository/tree?ref={branch['name']}", headers=headers)
            files = response.json()
            for file in files:
                # print(type(file))
                # print(file)
                if type(file) == dict:
                  if file["type"] == "blob" and not file["name"].endswith(".md"):
                    file_response = requests.get(f"{base_url}/projects/{project['id']}/repository/files/{file['path']}/raw?ref={branch['name']}", headers=headers)
                    lines = len(file_response.text.split("\n"))
                    lines_count += lines
            if lines_count > max_lines:
                max_lines = lines_count
                branch_names = [branch["name"]]
            elif lines_count == max_lines:
                branch_names.append(branch["name"])
        if max_lines > 0:
            pipeline_response = requests.get(f"{base_url}/projects/{project['id']}/pipelines", headers=headers)
            pipelines = pipeline_response.json()
            if len(pipelines) > 0:
                project_data.append([project["name"], project["path_with_namespace"], ", ".join(branch_names), max_lines])
distinct_project_list = []
for project in project_data:
    if project[0] not in distinct_project_list:
        distinct_project_list.append(project[0])
sum_of_distinct_projects = len(distinct_project_list)
df = pd.DataFrame(project_data, columns=["Project Name", "Project Path", "Branch Name", "Line of Code"])
df.loc[len(df)] = ["Total Projects", sum_of_distinct_projects, "", ""]
###export to csv
# df.to_csv("tltdeveloper-infra3.csv", index=False)
print(tabulate(df, headers=["Project Name", "Project Path", "Branch Name", "Line of Code"]))
# Convert the values in the 'Line of Code' column to integers, but only if they are not empty
df['Line of Code'] = df['Line of Code'].apply(lambda x: int(x) if x else 0)
# Add this line to get the sum of line of code and store it in a variable
total_line_of_code = df['Line of Code'].sum()
# Display the total line of code
print(f"Total line of code: {total_line_of_code}")
print(f"Total projects: {sum_of_distinct_projects}")
  # else:
  #     print("An error occurred:", response.status_code)
  

