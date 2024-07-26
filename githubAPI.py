import requests
import json
import base64
import os
import logging
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("githubAPI.log"),
                        logging.StreamHandler()
                    ])

# Get a logger instance
logger = logging.getLogger(__name__)

# SIDENOTE: only public repositories

def ensure_folder_exists(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        logger.info(f"Folder '{folder_path}' created.")
    else:
        logger.info(f"Folder '{folder_path}' already exists.")


def check_requirements_file(repo_owner, repo_name, requirements_file):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/"
    logger.info(url)
    response = requests.get(url)
    logger.info(response.status_code)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file' and item['name'] == requirements_file:
                return True
        return False
    else:
        logger.info(f"Failed to access repository: {response.status_code}")
        return False


def request_info(repo_owner, repo_name, path):
    
    """Function to retrieve information using GitHub API"""

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()
        if 'content' in content:
            file_content = base64.b64decode(content['content']).decode('utf-8')
            return file_content
        else:
            return None
    else:
        return None


def gitHubInfo(repo_owner:str, repo_name:str) -> None:
    
    """Function to retrieve various information for a specified GitHub-repository 
    & (for now) write it to json files"""

    #Set urls
    urls = {"github": f"https://api.github.com/repos/{repo_owner}/{repo_name}", 
        "contents": f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/",
        "contributors": f"https://api.github.com/repos/{repo_owner}/{repo_name}/contributors",
        "languages": f"https://api.github.com/repos/{repo_owner}/{repo_name}/languages"
        }
    
    #Check requirements files:
    requirements_files = ['requirements.txt', 'package.json', 'Gemfile', 'Pipfile', 'docker-compose.yml']
    for requirement_file in requirements_files:
        if check_requirements_file(repo_owner, repo_name, requirement_file):
            urls[f'requirement_{requirement_file}'] = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{requirement_file}"

    logger.info(urls)

    # check if path exists & create in case it doesn't
    if not os.path.exists(f'./input/{repo_owner}/{repo_name}'):
        os.makedirs(f'./input/{repo_owner}/{repo_name}')
    
    #Get information
    for k,v in urls.items():
        logger.info(k,v)
        response = requests.get(v)
        logger.info(response.status_code)
        if response.status_code == 200:
            logger.info(response.json())
            with open(f'./input/{repo_owner}/{repo_name}/{k}.json', 'w') as json_file:
                json.dump(response.json(), json_file, indent=4)
