#!/usr/bin/env python

#
#   AUTHOR: ANAND KANANI
#   PURPOSE: THIS SCRIPT HELPS IN SDA POV DEMO CONFIGURATION FAST-FORWARDING.
#

import os
import sys
import subprocess

print ("  === WELCOME TO THE SDA POV DEMO CONFIGURATION FAST-FORWARDING SCRIPT ===\n")

# ask users to use python3 if they are on python2
python_major_version = sys.version_info[0]
if python_major_version == 3:
    pass
elif python_major_version == 2:
    print("IMPORTANT: THIS CODE IS NO LONGER SUPPORTED ON PYTHON V2. USE PYTHON V3 INSTEAD.\n")
    raw_input("PRESS ENTER TO EXIT")
    os._exit(0)
else:
    print("COULD NOT DETERMINE PYTHON VERSION. SO EXITING.\n")
    raw_input("PRESS ENTER TO EXIT")
    os._exit(0)

# checking for special python modules and installing them if not already present
try:
    import git
except:
    print("==> INSTALLING THE REQUIRED PYTHON MODULE - gitpython")
    subprocess.call([sys.executable, "-m", "pip", "install", "gitpython"])
    import git
try:
    import requests
    from requests.exceptions import HTTPError
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
except:
    print("==> INSTALLING THE REQUIRED PYTHON MODULE - requests")
    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    from requests.exceptions import HTTPError
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# critical variables are in uppercase
GIT_REPO_URL = "https://github.com/ankanani/sdapovfastforward.git"
SCRIPT_WORK_DIR = os.path.join(".","sdapovfastforward")
SCRIPT_WORK_DIR_TEMP = os.path.join(".","sdapovfastforward","temp")

# clone git repo if not exists already
try:
    repo = git.Repo(".")
    print("==> FOUND LOCAL GIT REPO")
except git.exc.InvalidGitRepositoryError:
    print("==> LOCAL GIT REPO NOT FOUND. WILL FETCH ONE FROM THE INTERNET. YOU WILL SEE A NEW DIRECTORY CREATED AT THE END.")
    repo = git.Repo.clone_from(GIT_REPO_URL, SCRIPT_WORK_DIR)
    os.unlink(os.path.abspath(__file__))
    print ("==> JUST EXECUTE THIS SCRIPT AGAIN FROM sdapovfastforward DIRECTORY\n")
    raw_input("PRESS ENTER TO EXIT")
    sys.exit(0)
except Exception as e:
    print("==> GIT REPO READING EXCEPTION %s. SO EXITING." % str(e))
    raw_input("PRESS ENTER TO EXIT")
    sys.exit(0)
