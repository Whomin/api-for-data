import requests
import os

base_url = "https://gitlab.com/api/v4"
group_ids = [62085822]  # List of group IDs
bearer_token = "glpat--VYH3zwqei8DXHcmNSps"
headers = {"Authorization": f"Bearer {bearer_token}"}
project_info_with_template_infra = []

for group_id in group_ids:
    page = 1
    while True:
        params = {"include_subgroups": True, "page": page, "per_page": 100}
        response = requests.get(f"{base_url}/groups/{group_id}/projects", headers=headers, params=params)
        #if response.status_code :
        projects = response.json()
        if len(projects) == 0:
            break
        for project in projects:
            project_id = project["id"]
            response = requests.get(f"{base_url}/projects/{project_id}/repository/files/.gitlab-ci.yml/raw?ref=main", headers=headers)
            #if response.status_code == 200:
            content = response.text
            #if "test" in content:
            project_info_with_template_infra.append({"id": project_id, "name": project["name"]})
            page += 1
        #else:
            #print(f"An error occurred for group {group_id}: {response.status_code}")

print("Project IDs and Names with .gitlab-ci.yml containing 'template-infra':")
for project_info in project_info_with_template_infra:
    print(f"ID: {project_info['id']}, Name: {project_info['name']}")
    