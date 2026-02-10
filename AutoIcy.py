import os
import json
from pathlib import Path
from html.parser import HTMLParser
import pprint
import tkinter as tk
import csv

# -------------
# Globals
# -------------

project_name = ""
task_link_prefix = ""
commits = []
tasks = []

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

def parse_tasks(project_filename, assigned):
    with open(project_filename, 'r') as project_file:
        project_json = json.load(project_file)

        # extract project-level info
        global project_name
        global task_link_prefix
        if "name" in project_json and "slug" in project_json:
            project_name = project_json["name"]
            task_link_prefix = "https://tree.taiga.io/project/" + project_json["slug"] + "/task/"
        else:
            raise Exception("json file not properly formatted")

        # extract tasks
        if 'tasks' in project_json:
            global tasks
            for old_task in project_json['tasks']: # pull the tasks out of the json file
                if old_task["assigned_to"] == assigned: # filter out tasks done by others
                    task_number = old_task['ref']
                    tasks.append(  {
                        'id'      : task_number,
                        'assigned': old_task["assigned_to"],
                        'text'    : old_task["subject"],
                        'text-k'  : old_task["subject"][:30],  # kurz version is < 30 chars
                        'date'    : old_task["finished_date"],
                        'link'    : task_link_prefix + str(task_number)
                    })
        else:
            raise Exception("no tasks in json file")
    return tasks

def parse_commits(github_html_filename):
    global commits
    #commits = []
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
                date = commit["committedDate"][5:7] + '/' + commit["committedDate"][8:10] + '/' + commit["committedDate"][:4]
                commits.append({
                    "date"   : date ,
                    "text"   : commit["shortMessage"],
                    "text-k" : commit["shortMessage"][:40],  # kurz version is < 30 chars
                    "id"     : commit["oid"],
                    "link"   : "https://github.com" + commit["url"],
                    "str"    : date + "-" + commit["shortMessage"][:40]

                })
    return commits

        #for commit in commits:
        #    pprint.pprint(commit)





print ("****")
#print (get_html())
#print (get_json())
#tasks = parse_tasks(get_json(), "rjohn172@asu.edu")
parse_tasks(get_json(), "rjohn172@asu.edu")

#for task in tasks:
#    print(task, tasks[task]["assigned"], tasks[task]["text-k"], tasks[task]["date"], tasks[task]["link"])

#for task in tasks:
#    print(task["assigned"], task["text-k"], task["date"], task["link"])


print ("****")
parse_commits(get_html())
#pprint.pprint( parse_commits(get_html()) )

#commits = parse_commits(get_html())

# -------------
# TK GUI Widgets
# -------------
root = tk.Tk()
root.title("Auto ICy")
root.geometry("1000x320")

# Tasks listbox
task_picker = tk.Listbox(root, width=50, selectmode=tk.SINGLE, exportselection=False)
task_picker.grid(row=3, rowspan=3, column=1)

#
task_load_button = tk.Button(root, text="Load Task JSON")
task_load_button.grid(row=2, column=1)

# Commits listbox
commit_picker = tk.Listbox(root, width=50, selectmode=tk.BROWSE, exportselection=False)
commit_picker.grid(row=3, rowspan=3, column=3)

#
commit_load_button = tk.Button(root, text="Load Commits HTML")
commit_load_button.grid(row=2, column=3)

# join button
join_button = tk.Button(root, text="Join Task with Commit")
join_button.grid ( row=3, column=2)

# remove button
remove_button = tk.Button(root, text="Remove Selected Join")
remove_button.grid ( row=4, column=2)

# Export button
export_button = tk.Button(root, text="Export CSV")
export_button.grid ( row=5, column=2)

# display of joined task/commit
joined_display = tk.Listbox(root, width= 100)
joined_display.grid(row=10, column=1, columnspan=3)


# load the tasks into the listbox
for index, task in enumerate(tasks):
    task_picker.insert(index, task["text"])

# load the commits into the listbox
for index, commit in enumerate(commits):
    commit_picker.insert(index, commit["str"])

# -------------
# TK functions
# -------------
def perform_join():
    pass
    # get the selected items and make sure there is a selection
    task_text = task_picker.get( task_picker.curselection())
    commit_str = commit_picker.get(commit_picker.curselection())
    print(task_text)
    print(commit_str)
    if not task_text or not commit_str:
        raise Exception("Both a task and a commit must be selected to join")
        return
    joined_string = task_text + "|" + commit_str
    joined_display.insert(tk.END, joined_string)

join_button.config( command=perform_join)



def export_CSV():
    csv_task_rows = []
    csv_commit_rows = []
    for i in range(joined_display.size()):
        row_text = joined_display.get(i)
        print(row_text)

        divider_index = row_text.find("|")
        commit_str = row_text[divider_index+1:]
        task_text = row_text[:divider_index]
        print(task_text)
        print(commit_str)

        # look up the commit based on the selected text
        global commits
        commit_index = -1
        for index in range(len(commits)):
            if commits[index]["str"] == commit_str:
                commit_index = index
        if commit_index == -1:  # error if unable to find match
            raise Exception("Could not find commit")
            return
        # look up the task based on the selected text
        global tasks
        task_index = -1
        for index in range(len(tasks)):
            if tasks[index]["text"] == task_text:
                task_index = index
        if task_index == -1:  # error if unable to find match
            raise Exception("Could not find task")
            return

        #format csv lines
        csv_task_rows.append( [tasks[task_index]["link"],tasks[task_index]["id"]])
        csv_commit_rows.append( [commits[commit_index]["link"], commits[commit_index]["date"] ])

    #combine csv_sections
    csv_rows = [["Copy the below into your IC Column's A & B",""]] + csv_task_rows + [["Copy the below into your IC Column's E & F",""]] + csv_commit_rows
    #csv_rows =  csv_task_rows +  csv_commit_rows

    pprint.pprint(csv_rows)

    # write the output to the export file
    with open("export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_rows)


export_button.config( command=export_CSV)




# -------------
# TK Start
# -------------
root.mainloop()