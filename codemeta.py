from pysubyt.subyt import Subyt
from pathlib import Path
import os

## Generate codemeta file ##
def createCodemeta(repo_owner:str, repo_name: str):

    """ Generate codemeta.json file 
    Using retrieved information from github repo & github API
    & template """

    # check if path exists & create in case it doesn't
    if not os.path.exists(f'./output/{repo_owner}/{repo_name}'):
        os.makedirs(f'./output/{repo_owner}/{repo_name}')

    #Set variables
    files = [file.stem for file in Path(f'./input/{repo_owner}/{repo_name}').iterdir() if file.is_file()]
    source_dict = { f'{file}':f'./input/{repo_owner}/{repo_name}/{file}.json'  for file in files}

    subyt_sheet = Subyt(
        extra_sources=source_dict,
        sink=f'./output/{repo_owner}/{repo_name}/codemeta.jsonld',
        template_name="codemeta.json.ldt.j2",
        template_folder="./templates/",
    )
    #genereate output
    subyt_sheet.process()