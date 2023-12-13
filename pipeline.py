import requests
import os
import re

base_url = "https://gitlab.com/api/v4"
group_ids = [62085822]  # List of group IDs
# group_ids = [7786252, 7786271]
bearer_token = "glpat--VYH3zwqei8DXHcmNSps"
print("Token = {bearer_token}")
headers = {"Authorization": f"Bearer {bearer_token}"}
  
def set_cicd_variables(project_id, variables):
    cicd_variables_url = f"{base_url}/projects/{project_id}/variables"

    for key, value in variables.items():
        variable_data = {
            "key": key,
            "value": value,
            "protected": True  # You can set this to True or False as needed
        }

        response = requests.post(cicd_variables_url, headers=headers, json=variable_data)

        if response.status_code == 201:
            print(f"Variable {key} set as CI/CD variable for project {project_id}")
        else:
            print(f"Failed to set variable {key} for project {project_id}. Status code: {response.status_code}")

project_info_with_template_infra = []

for group_id in group_ids:
    page = 1
    while True:
        params = {"include_subgroups": True, "page": page, "per_page": 100}
        response = requests.get(f"{base_url}/groups/{group_id}/projects", headers=headers, params=params)
        if response.status_code == 200:
            projects = response.json()
            if len(projects) == 0:
                break
            for project in projects:
                project_id = project["id"]
                response = requests.get(f"{base_url}/projects/{project_id}/repository/files/.gitlab-ci.yml/raw?ref=uat", headers=headers)
                if response.status_code == 200:
                    content = response.text
                    if "tltdeveloper/infra/template-infra" in content:
                        variables = {}
                        new_ci_config_path = ".gitlab-ci.yml@tltdeveloper/infra/template-infra:feature/general-pipeline"
                        data = {"ci_config_path": new_ci_config_path}
                        #update_response = requests.put(f"{base_url}/projects/{project_id}", headers=headers, data=data)
                        if update_response.status_code == 200:
                            print(f"Updated ci_config_path for project {project['name']} (ID: {project_id})")

                        else:
                            print(f"Failed to update ci_config_path for project {project['name']} (ID: {project_id}). Status Code: {update_response.status_code}")
                        # Extract variables and their values
                        for match in re.finditer(r'^\s*([A-Z_]+):\s*["\'](.*?)["\']', content, re.MULTILINE):
                            variable_name, variable_value = match.groups()
                            # Check if the variable is not commented
                            if not re.search(r'#\s*' + variable_name, content):
                                variables[variable_name] = variable_value.strip()

                        project_info_with_template_infra.append({
                            "id": project_id,
                            "name": project["name"],
                            "variables": variables
                        })

                        # Set the collected variables as CI/CD variables
                        #set_cicd_variables(project_id, variables)
                page += 1
        else:
            print(f"An error occurred for group {group_id}: {response.status_code}")

print("Project IDs and Names with .gitlab-ci.yml containing 'template-infra' and their variables:")
for project_info in project_info_with_template_infra:
    print(f"ID: {project_info['id']}, Name: {project_info['name']}, Variables: {project_info['variables']}")