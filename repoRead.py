import requests
import yaml
import os

from codemeta import createCodemeta
from githubAPI import gitHubInfo

#Get open-code-repositories
response = requests.get("https://api.github.com/repos/vliz-be-opsci/open-code-list/contents")
response.raise_for_status() # Raise an exception for HTTP errors

for item in response.json():
    download_url = item.get("download_url")
    if download_url:
        response = requests.get(download_url)
        response.raise_for_status()
        open_code_repos = yaml.safe_load(response.text) # Load the YAML content


for repo in open_code_repos:
    repo_name = repo['name']
    repo_owner = repo['owner']

    # check if path exists & create in case it doesn't
    if not os.path.exists(f'./output/{repo_owner}/{repo_name}'):
        os.makedirs(f'./output/{repo_owner}/{repo_name}')

    # get information via GitHub API
    gitHubInfo(repo_owner, repo_name)
    # create codemeta file
    createCodemeta(repo_owner, repo_name)
