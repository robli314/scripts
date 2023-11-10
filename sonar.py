import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime

def fetch_issues(api_url, username, password):
    total_issues = get_total_issues(api_url, username, password)
    issues = []

    if total_issues > 0:
        page_size = 500
        total_pages = total_issues // page_size + 1

        for page in range(1, total_pages + 1):
            issues += get_page_issues(api_url, page, page_size, username, password)

    return issues

def get_total_issues(api_url, username, password):
    response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
    return response.json()['total']

def get_page_issues(api_url, page, page_size, username, password):
    params = {'statuses': 'OPEN', 'ps': page_size, 'p': page}
    response = requests.get(api_url, params=params, auth=HTTPBasicAuth(username, password))
    return response.json()['issues']

def write_to_json(issues, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(issues, json_file, indent=2)

def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config.get('username'), config.get('password'), config.get('sonar_url')

if __name__ == "__main__":
    

    # Load username and password from config file
    username, password, sonar_url = load_config()

    api_url = sonar_url + "/api/issues/search"

    fetched_issues = fetch_issues(api_url, username, password)
    
    # Append the current date to the JSON file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    json_file_path = f'issues_{current_date}.json'

    # Write the issues to the JSON file
    write_to_json(fetched_issues, json_file_path)

    print(f"Issues have been written to {json_file_path}")
