import os
import json
from pathlib import Path

project_name = ""
task_link_prefix = ""
commits = {}
tasks = {}


def get_html():
    for filepath in Path('.').iterdir():
        if filepath.suffix == '.html':
            return filepath


def get_json():
    for filepath in Path('.').iterdir():
        if filepath.suffix == '.json':
            return filepath

def parse_tasks(project_filename):

    with open(project_filename, 'r') as project_file:
        project_json = json.load(project_file)


        # extract project-level info
        global project_name
        global task_link_prefix
        project_name = project_json["name"]
        task_link_prefix = "https://tree.taiga.io/project/" + project_json["slug"] + "/task/"

        # extract tasks
        if 'tasks' in project_json:
            global tasks
            for old_task in project_json['tasks']: # pull the tasks out of the json file
                task_number = old_task['ref']
                tasks[task_number] = {
                    'assigned' : old_task["assigned_to"],
                    'text'     : old_task["subject"],
                    'text-k'   : old_task["subject"][:30], # kurz version is < 30 chars
                    'date'     : old_task["finished_date"]
                }

        else:
            raise Exception("no tasks in json file")


print ("****")
print (get_html())
print (get_json())
parse_tasks(get_json())

for task in tasks:
    print(task, tasks[task]["assigned"], tasks[task]["text-k"], tasks[task]["date"])



