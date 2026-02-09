import os
import json
from pathlib import Path
from html.parser import HTMLParser
import pprint

# -------------
# Globals
# -------------

project_name = ""
#task_link_prefix = ""
#commits = []
#tasks = {}

# -------------
# HTML parser class
# clunky, but I am trying to avoid making people install beautiful soup
# -------------

class JSON_Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.json_data = ""

    def handle_starttag(self, tag, attrs):
        '''
        Hardcoded to seek out the tag with the commit json data in a github page
        '''
        if tag == "script":
            attrs = dict(attrs)
            if (
                attrs.get("type") == "application/json"
                and attrs.get("data-target") == "react-app.embeddedData"
            ):
                self.capture = True

    def handle_data(self, data):
        if self.capture:
            self.json_data += data

    def handle_endtag(self, tag):
        if tag == "script" and self.capture:
            self.capture = False

# -------------
# Functions
# -------------

def get_html():
    for filepath in Path('.').iterdir():
        if filepath.suffix == '.html':
            return filepath
    return None


def get_json():
    for filepath in Path('.').iterdir():
        if filepath.suffix == '.json':
            return filepath
    return None

def parse_tasks(project_filename):
    tasks = {}
    with open(project_filename, 'r') as project_file:
        project_json = json.load(project_file)

        # extract project-level info
        global project_name
        #global task_link_prefix
        if "name" in project_json and "slug" in project_json:
            project_name = project_json["name"]
            task_link_prefix = "https://tree.taiga.io/project/" + project_json["slug"] + "/task/"
        else:
            raise Exception("json file not properly formatted")

        # extract tasks
        if 'tasks' in project_json:
            #global tasks
            for old_task in project_json['tasks']: # pull the tasks out of the json file
                task_number = old_task['ref']
                tasks[task_number] = {
                    'assigned' : old_task["assigned_to"],
                    'text'     : old_task["subject"],
                    'text-k'   : old_task["subject"][:30], # kurz version is < 30 chars
                    'date'     : old_task["finished_date"],
                    'link'     : task_link_prefix + str(task_number)
                }
        else:
            raise Exception("no tasks in json file")
    return tasks

def parse_commits(github_html_filename):
    #global commits
    commits = []
    with open(github_html_filename, 'r') as commit_file:
        commit_html = commit_file.read()
        parser = JSON_Extractor()
        parser.feed(commit_html)

        commits_json_str = parser.json_data.strip()
        commits_json_all = json.loads(commits_json_str)
        #pprint.pprint(commits_json_all)
        # this is the structure to get at the commits. It is messy
        #commits_json = commits_json_all["payload"]["commitGroups"][0]["commits"]
        commits_json_groups = commits_json_all["payload"]["commitGroups"]
        commits_json = {}
        for commit_group in commits_json_groups:
            #print(commit_group)
            for commit in commit_group["commits"]:
                #print (commit)
                commits.append({
                    "date"   : commit["committedDate"][5:7] + '/' + commit["committedDate"][8:10] + '/' + commit["committedDate"][:4] ,
                    "text"   : commit["shortMessage"],
                    "text-k" : commit["shortMessage"][:30],  # kurz version is < 30 chars
                    "text-k" : commit["shortMessage"][:30],  # kurz version is < 30 chars
                    "id"     : commit["oid"],
                    "link"   : "https://github.com" + commit["url"]

                })
    return commits

        #for commit in commits:
        #    pprint.pprint(commit)





print ("****")
#print (get_html())
#print (get_json())
tasks = parse_tasks(get_json())

for task in tasks:
    print(task, tasks[task]["assigned"], tasks[task]["text-k"], tasks[task]["date"], tasks[task]["link"])

print ("****")

pprint.pprint( parse_commits(get_html()) )

