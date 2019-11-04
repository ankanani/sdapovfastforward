#!/usr/bin/env python


#
#   AUTHOR: ANAND KANANI
#   PURPOSE: THIS SCRIPT HELPS IN SDA POV DEMO CONFIGURATION FAST-FORWARDING.
#   REQUIREMENTS: IT NEEDS PYTHON3 (NOT PYTHON2) INSTALLED. AND IT REQUIRES REACHABILITY TO THE DNAC, ISE, WLC.
#   HOW TO USE: JUST DOWNLOAD AND EXECUTE THIS SCRIPT - https://raw.githubusercontent.com/ankanani/sdapovfastforward/master/sdapovfastforward.py
#

import os
import sys
import subprocess
import hashlib

print("")
print("  === WELCOME TO THE SDA POV DEMO CONFIGURATION FAST-FORWARDING SCRIPT ===\n")

# ask users to use python3 if they are on python2
python_major_version = sys.version_info[0]
if python_major_version == 3:
    pass
elif python_major_version == 2:
    print("IMPORTANT: IT APPEARS THAT THIS CODE IS EXECUTED USING PYTHON V2.")
    print("YOU NEED TO EXECUTE THIS SCRIPT USING PYTHON V3.")
    print("INSTALL PYTHON V3 AND ADD IT TO THE SYSTEM PATH, CHANGE .PY FILE ASSOCIATION TO PYTHON V3, IF REQUIRED.")
    input("PRESS ENTER TO EXIT")
    os._exit(0)
else:
    print("COULD NOT DETERMINE PYTHON VERSION. SO EXITING.\n")
    input("PRESS ENTER TO EXIT")
    os._exit(0)

# checking for special python modules and installing them if not already present
try:
    import git
except:
    print("==> INSTALLING THE REQUIRED PYTHON MODULE - gitpython\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "gitpython"])
    import git
try:
    import requests
    from requests.exceptions import HTTPError
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
except:
    print("==> INSTALLING THE REQUIRED PYTHON MODULE - requests\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    from requests.exceptions import HTTPError
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
try:
    from postpython.core import PostPython
except:
    print("==> INSTALLING THE REQUIRED PYTHON MODULE - postpython\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "postpython"])
    from postpython.core import PostPython

# critical variables are in uppercase
GIT_REPO_URL = "https://github.com/ankanani/sdapovfastforward.git"
SCRIPT_WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"sdapovfastforward")
SCRIPT_WORK_DIR_TEMP = os.path.join(os.path.dirname(os.path.abspath(__file__)),"sdapovfastforward","temp")

# clone git repo if not exists already
try:
    repo = git.Repo(os.path.dirname(os.path.abspath(__file__)))
    print("==> FOUND LOCAL GIT REPO\n")
except git.exc.InvalidGitRepositoryError:
    print("==> LOCAL GIT REPO NOT FOUND. WILL FETCH ONE FROM THE INTERNET. YOU WILL SEE A NEW DIRECTORY CREATED AT THE END.\n")
    if not os.path.exists(SCRIPT_WORK_DIR):
        try:
            repo = git.Repo.clone_from(GIT_REPO_URL, SCRIPT_WORK_DIR)
            os.unlink(os.path.abspath(__file__))
            print ("==> JUST EXECUTE THIS SCRIPT AGAIN FROM sdapovfastforward DIRECTORY\n")
        except Exception as e:
            print("==> GIT REPO READING EXCEPTION %s. SO EXITING." % str(e))
    else:
        print("==> CANNOT FETCH GIT REPO SINCE A LOCAL DIRECTORY sdapovfastforward EXISTS. KINDLY DELETE OR RENAME THAT DIRECTORY TO SOMETHING ELSE AND TRY AGAIN.\n")
    input("PRESS ENTER TO EXIT")
    sys.exit(0)
except Exception as e:
    print("==> GIT REPO READING EXCEPTION %s. SO EXITING." % str(e))
    input("PRESS ENTER TO EXIT")
    sys.exit(0)

# calculating self checksum
orig_sum = hashlib.md5(open(os.path.abspath(__file__),"rb").read()).hexdigest()

# update local git repo
try:
    repo = git.Repo(os.path.dirname(os.path.abspath(__file__)))
    print("==> CHECKING FOR UPDATES.\n")
    repo.remotes.origin.fetch()
    repo.remotes.origin.pull()
    print("==> UPDATE CHECK COMPLETE.\n")
    new_sum = hashlib.md5(open(os.path.abspath(__file__),"rb").read()).hexdigest()
    if new_sum != orig_sum:
        print("==> THIS SCRIPT IS UPDATED. SO YOU NEED TO EXECUTE IT AGAIN.")
        input("PRESS ENTER TO EXIT")
        sys.exit(0)
except Exception as e:
    if "commit your changes" in str(e):
        print("==> IT SEEMS YOU MODIFIED THE SCRIPT FILES LOCALLY. SO THE SCRIPT CANNOT PULL AND OVERWRITE THE NEW UPDATES.\n")
        while True:
            a = input("WOULD YOU LIKE TO OVERRIDE THE LOCAL CHANGES BEFORE UPDATING? [Y/N] ")
            if a.lower() in ["yes","y"]:
                repo.git.reset('--hard','origin/master')
                repo.remotes.origin.pull()
                print("\n==> LOCAL CHANGES ARE OVERWRITTEN AND UPDATE COMPLETE.\n")
                break
            elif a.lower() in ["no","n"]:
                while True:
                    print("")
                    a = input("WOULD YOU LIKE TO CONTINUE WITH EXISTING VERSION OF THE SCRIPT? [Y/N] ")
                    if a.lower() in ["yes","y"]:
                        print("\n==> WILL CONTINUE WITH EXISTING VERSION OF THE SCRIPT.\n")
                        break
                    elif a.lower() in ["no","n"]:
                        input("PRESS ENTER TO EXIT")
                        sys.exit(0)
                    else:
                        print("ENTER EITHER YES/NO")
                break
            else:
                print("ENTER EITHER YES/NO")
    else:
        print("==> COULD NOT CHECK FOR UPDATES DUE TO THE FOLLOWING EXCEPTION - %s" % str(e))
        print("==> WILL CONTINUE WITH EXISTING VERSION OF THE SCRIPT.\n")
    

# parsing the API Files
print ("Now the real work")
input("PRESS ENTER TO EXIT")