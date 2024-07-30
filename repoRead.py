import requests
from urllib.parse import urlparse

from codemeta import createCodemeta
from githubAPI import gitHubInfo

#Get open-code-repositories
response = requests.get("https://raw.githubusercontent.com/vliz-be-opsci/open-code-list/main/open-code-list.txt")
response.raise_for_status() # Raise an exception for HTTP errors

urls = response.text.splitlines()
for url in urls:
    path = urlparse(url).path.strip('/')
    path_parts = path.split('/')

    if len(path_parts) >= 2:
        repo_owner = path_parts[0]
        repo_name = path_parts[1]
    else:
        raise ValueError("Invalid GitHub URL format")
    
    # get information via GitHub API
    gitHubInfo(repo_owner, repo_name)
    # create codemeta file
    createCodemeta(repo_owner, repo_name)
