#!/usr/bin/env python


#
#   AUTHOR: ANAND KANANI
#   PURPOSE: THIS SCRIPT HELPS IN SDA POV DEMO CONFIGURATION FAST-FORWARDING.
#   REQUIREMENTS: IT NEEDS PYTHON3 (NOT PYTHON2) INSTALLED. AND IT REQUIRES REACHABILITY TO THE DNAC, ISE, WLC.
#   HOW TO USE: JUST DOWNLOAD AND EXECUTE THIS SCRIPT - https://raw.githubusercontent.com/ankanani/sdapovfastforward/master/sdapovfastforward.py
#               THE SCRIPT IS VERY INTERACTIVE.
#

import os
import sys
import subprocess
import hashlib
import platform

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
    import wget
except:
    print("==> INSTALLING THE REQUIRED PYTHON MODULE - wget\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "wget"])
    import wget
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

print("==> FOUND ALL REQUIRED PYTHON PACKAGES\n")

# critical variables are in uppercase
GIT_REPO_URL = "https://github.com/ankanani/sdapovfastforward.git"
SCRIPT_WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"sdapovfastforward")
SCRIPT_WORK_DIR_POSTMAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),"postman")

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
    print("==> CHECKING FOR CODE UPDATES.\n")
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
    

# checking if node.js exists for - "newman" program
try:
    subprocess.check_output(["node", "-v"])
    print("==> FOUND NODE.JS\n")
except OSError as e:
    print ("==> IT SEEMS NODE.JS IS NOT INSTALLED. THIS SCIPT WILL ATTEMPT TO DOWNLOAD AND INSTALL NODE.JS")
    while True:
        print("")
        a = input("WOULD YOU LIKE TO CONTINUE WITH DOWNLOAD AND INSTALLATION OF NODE.JS? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("PRESS ENTER TO EXIT")
            sys.exit(0)
        else:
            print("ENTER EITHER YES/NO")
    
    print("\n==> DOWNLOADING NODE.JS SETUP. THIS TAKES A FEW MINUTES")
    if platform.system().lower() == "windows":
        if platform.machine().endswith('64'):
            url = "https://nodejs.org/dist/v12.13.0/node-v12.13.0-x64.msi"
            wget.download(url, "./")
            print("\n\n==> INSTALLING NODE.JS SETUP. THIS TAKES A FEW MINUTES")
            subprocess.call('msiexec.exe /qb /i node-v12.13.0-x64.msi')
        else:
            url = "https://nodejs.org/dist/v12.13.0/node-v12.13.0-x86.msi"
            wget.download(url, "./")
            print("\n\n==> INSTALLING NODE.JS SETUP. THIS TAKES A FEW MINUTES")
            subprocess.call('msiexec.exe /qb /i node-v12.13.0-x86.msi')
        
        print("\n==> NODE.JS IS INSTALLATION COMPLETE.  NOW RUN THIS SCRIPT AGAIN.")
        input("PRESS ENTER TO EXIT")
        sys.exit(0)
    elif platform.system().lower() == "darwin":
            url = "https://nodejs.org/dist/v12.13.0/node-v12.13.0.pkg"
            wget.download(url, "./")
            print("NODE.JS IS DOWNLOADED. JUST DOUBLE-CLICK TO INSTALL IT AND THEN RUN THIS SCRIPT AGAIN.")
            input("PRESS ENTER TO EXIT")
            sys.exit(0)
    else:
        print("THIS SCRIPT IS RUNNING ON AN UNSUPPORTED OS. CURRENTLY ONLY WINDOWS OR MAC ARE SUPPORTED.")
        input("PRESS ENTER TO EXIT")
        sys.exit(0)


# checking for the existence of node- "newman"
try:
    subprocess.check_output(["newman", "-v"], shell=True)
    print("==> FOUND POSTMAN - NEWMAN NODE PACKAGE\n")
except subprocess.CalledProcessError as e:
    print ("\n==> IT SEEMS POSTMAN - NEWMAN PACKAGE IS NOT INSTALLED. \nTHIS SCIPT WILL ATTEMPT TO DOWNLOAD AND INSTALL POSTMAN - NEWMAN NODE PACKAGE")
    while True:
        print("")
        a = input("WOULD YOU LIKE TO CONTINUE WITH DOWNLOAD AND INSTALLATION OF POSTMAN - NEWMAN NODE PACKAGE? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("PRESS ENTER TO EXIT")
            sys.exit(0)
        else:
            print("ENTER EITHER YES/NO")
    
    print("\n==> INSTALLING POSTMAN - NEWMAN PACKAGE SETUP. THIS TAKES A FEW MINUTES")
    subprocess.call(["npm", "install", "-g", "newman"], shell=True)
    print("")
    try:
        subprocess.check_output(["newman", "-v"], shell=True)
        print("==> POSTMAN - NEWMAN PACKAGE INSTALLED SUCCESSFULLY\n")
    except subprocess.CalledProcessError as e:
        print("POSTMAN - NEWMAN PACKAGE COULD NOT BE INSTALLED AUTOMATICALLY. TRY INSTALLING IT MANUALLY USING THE COMMAND node install -g newman AND THEN RUN THIS SCRIPT AGAIN.")
        input("PRESS ENTER TO EXIT")
        sys.exit(0)

# now the core part
print("==> NOW LETS GET WORKING")

# search for postman collections and ask the user to choose one
print("\n")
all_postman_collection_files = [f for f in os.listdir(SCRIPT_WORK_DIR_POSTMAN) if os.path.isfile( os.path.join(SCRIPT_WORK_DIR_POSTMAN, f) ) and "postman_collection" in f ]
if len(all_postman_collection_files) > 0:
    print("==> THE FOLLOWING POSTMAN COLLECTIONS WERE FOUND.")
    count = 0
    for f in all_postman_collection_files:
        count+=1
        print("%s - %s" % (count,f) )
else:
    print("==> COULD NOT FIND ANY FILE THAT APPEAR TO BE A POSTMAN COLLECTION!")
    input("PRESS ENTER TO EXIT")
    sys.exit(0)

selected_postman_collection_file = ''
if len(all_postman_collection_files)==1:
    selected_postman_collection_file = all_postman_collection_files[0]
    while True:
        a = input("\nWOULD YOU LIKE TO CONTINUE WITH THIS OPTION? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("PRESS ENTER TO EXIT")
            sys.exit(0)
        else:
            print("ENTER EITHER YES/NO")
else:
    while True:
        print("")
        try:
            a = int(input("WHICH ONE WOULD YOU LIKE TO UTILIZE? [1-%s] " % (len(all_postman_collection_files)) ))
            selected_postman_collection_file = all_postman_collection_files[a-1]
            print("\nYOU HAVE SELECTED POSTMAN COLLECTION:- %s" % (selected_postman_collection_file) )
            
            a = input("\nWOULD YOU LIKE TO CONTINUE WITH THIS OPTION? [Y/N] ")
            if a.lower() in ["yes","y"]:
                break
        except:
            print("THAT'S NOT A VALID OPTION!")


# search for postman environments and ask the user to choose one
print("\n")
all_postman_environment_files = [f for f in os.listdir(SCRIPT_WORK_DIR_POSTMAN) if os.path.isfile( os.path.join(SCRIPT_WORK_DIR_POSTMAN, f) ) and "postman_environment" in f ]
if len(all_postman_environment_files) > 0:
    print("==> THE FOLLOWING POSTMAN ENVIRONMENTS WERE FOUND.")
    count = 0
    for f in all_postman_environment_files:
        count+=1
        print("%s - %s" % (count,f) )
else:
    print("==> COULD NOT FIND ANY FILE THAT APPEAR TO BE A POSTMAN ENVIRONMENT!")
    input("PRESS ENTER TO EXIT")
    sys.exit(0)

selected_postman_environment_file = ''
if len(all_postman_environment_files)==1:
    selected_postman_environment_file = all_postman_environment_files[0]
    while True:
        a = input("\nWOULD YOU LIKE TO CONTINUE WITH THIS OPTION? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("PRESS ENTER TO EXIT")
            sys.exit(0)
        else:
            print("ENTER EITHER YES/NO")
else:
    while True:
        print("")
        try:
            a = int(input("WHICH ONE WOULD YOU LIKE TO UTILIZE? [1-%s] " % (len(all_postman_environment_files)) ))
            selected_postman_environment_file = all_postman_environment_files[a-1]
            print("\nYOU HAVE SELECTED POSTMAN ENVIRONMENT:- %s" % (selected_postman_environment_file) )
            
            a = input("\nWOULD YOU LIKE TO CONTINUE WITH THIS OPTION? [Y/N] ")
            if a.lower() in ["yes","y"]:
                break
        except:
            print("THAT'S NOT A VALID OPTION!")


# Now lets run the "newman"
while True:
    print("\n==> WITH THE FOLLOWING SELECTION?\nPOSTMAN COLLECTION - %s\nPOSTMAN ENVIRONMENT - %s\n" % (selected_postman_collection_file,selected_postman_environment_file))
    a = input("\nARE YOU READY TO FAST FORWARD YOUR SDA POV? [Y/N] ")
    if a.lower() in ["yes","y"]:
        break
    elif a.lower() in ["no","n"]:
        input("PRESS ENTER TO EXIT")
        sys.exit(0)
    else:
        print("ENTER EITHER YES/NO")

print("\n\n==> EXECUTING NEWMAN NOW\n")
subprocess.call(["newman", "run", os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_collection_file), "-e", os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_environment_file)], shell=True)

print("\n\n==> IF ALL API CALLS WORKED IN THE ABOVE RUN THEN YOU ARE ALL SET.\n")
input("PRESS ENTER TO EXIT")
sys.exit(0)
