import os
import json
import csv
import subprocess
from datetime import datetime

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result.stdout, result.returncode

git_add = "git add ."
commit_message = input("Enter your commit message: ")
git_commit = f'git commit -m "{commit_message}"'
git_push = "git push origin main"

run_command(git_add)
run_command(git_commit)
output, return_code = run_command(git_push)

if return_code != 0:
    print("Git push failed. Aborting.")
else:
    git_username = input("Enter your Git username: ")
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_id, _ = run_command("git rev-parse HEAD")

    # Additional fields
    git_origin, _ = run_command("git config --get remote.origin.url")
    git_branch, _ = run_command("git branch --show-current")

    entry = {
        "name": git_username,
        "commit": commit_message,
        "date": current_date,
        "commitId": commit_id.strip(),
        "origin": git_origin.strip(),
        "branch": git_branch.strip()
    }

report_file = "report.json"

if os.path.exists(report_file) and os.path.getsize(report_file) > 0:
    with open(report_file, "r") as json_file:
        data = json.load(json_file)
else:
    data = []
data.append(entry)
with open(report_file, "w") as json_file:
    json.dump(data, json_file, indent=4)
    report_csv_file = "report.csv"
    with open(report_csv_file, "a", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["name", "commit", "date", "commitId", "origin", "branch"])
        if not os.path.exists(report_csv_file):
            csv_writer.writeheader()
        csv_writer.writerow(entry)

    print("Code pushed successfully and report updated.")
