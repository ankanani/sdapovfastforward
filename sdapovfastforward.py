#!/usr/bin/env python


#
#   AUTHOR: ANAND KANANI
#   PURPOSE: THIS SCRIPT HELPS IN SDA POV DEMO CONFIGURATION FAST-FORWARDING.
#   REQUIREMENTS: IT NEEDS PYTHON3 (NOT PYTHON2) INSTALLED. AND IT REQUIRES REACHABILITY TO THE DNAC, ISE, WLC.
#   HOW TO USE: JUST DOWNLOAD AND EXECUTE THIS SCRIPT - https://raw.githubusercontent.com/ankanani/sdapovfastforward/master/sdapovfastforward.py
#               THE SCRIPT IS INTERACTIVE AND WILL TELL YOU WHAT IT IS DOING.
#   NOTE: ITS FIRST EXECUTION WILL TAKE A FEW MINUTES AND WILL TAKE A COUPLE OF ITERATIONS.
#         THIS IS A ONE TIME THING ONLY, SINCE IT CHECKS FOR ANY DEPENDENCIES AND INSTALLS THEM AS REQUIRED.
#

import os
import sys
import subprocess
import hashlib
import platform

# critical variables are in uppercase
GIT_REPO_URL = "https://github.com/ankanani/sdapovfastforward.git"
POSTMAN_REPO = "https://github.com/ankanani/sdapovfastforward-postman"
SCRIPT_WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"sdapovfastforward")
SCRIPT_WORK_DIR_POSTMAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),"postman")
POSTMAN_COLLECTION_FILTER = "postman_collection"
POSTMAN_ENVIRONMENT_FILTER = "postman_environment"

print("")
print("  === Welcome to the SDA POV demo Configuration Fast-Forwarding script ===\n")

# ask users to use python3 if they are on python2
python_major_version = sys.version_info[0]
if python_major_version == 3:
    pass
elif python_major_version == 2:
    print("Important: It appears that this code is executed using Python v2.")
    print("You need to execute this script using Python v3.")
    print("Install Python v3 and add it to the system path, change .py file association to Python v3, if required.")
    input("Press <enter> to exit")
    os._exit(0)
else:
    print("Could not determine Python version. So exiting.\n")
    input("Press <enter> to exit")
    os._exit(0)


# checking for python wget module and installing it if not already present
try:
    import wget
except:
    print("==> Installing the required python module - WGET\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "wget"])
    import wget


# checking if git exists
try:
    subprocess.check_output(["git", "--version"])
    print("==> Found GIT installed\n")
except OSError as e:
    print ("==> It seems GIT is not installed on your system. Git is required. This scipt will attempt to download and install GIT")
    while True:
        print("")
        a = input("Would you like to continue with download and installation of GIT? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("Press <enter> to exit")
            os._exit(0)
        else:
            print("Enter either yes/no")
    
    print("\n==> Downloading GIT setup. This takes a few minutes")
    if platform.system().lower() == "windows":
        if platform.machine().endswith('64'):
            url = "https://github.com/git-for-windows/git/releases/download/v2.24.0.windows.2/Git-2.24.0.2-32-bit.exe"
            wget.download(url, "./")
            print("\n\n==> installing GIT setup. This takes a few minutes")
            subprocess.call('Git-2.24.0.2-32-bit.exe /silent')
        else:
            url = "https://github.com/git-for-windows/git/releases/download/v2.24.0.windows.2/Git-2.24.0.2-64-bit.exe"
            wget.download(url, "./")
            print("\n\n==> installing GIT setup. This takes a few minutes")
            subprocess.call('Git-2.24.0.2-64-bit.exe /silent')
        
        print("\n==> GIT installation is complete.  Now run this script again so that the script can use it.")
        input("Press <enter> to exit")
        os._exit(0)
    else:
        print("This script could not find GIT installed on your system. Please install GIT and then try again.")
        input("Press <enter> to exit")
        os._exit(0)



# checking for special python modules and installing them if not already present
try:
    import git
except:
    print("==> Installing the required python module - GITPYTHON\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "gitpython"])
    import git
try:
    import requests
    from requests.exceptions import HTTPError
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
except:
    print("==> Installing the required python module - REQUESTS\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    from requests.exceptions import HTTPError
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
try:
    from postpython.core import PostPython
except:
    print("==> Installing the required python module - POSTPYTHON\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "postpython"])
    from postpython.core import PostPython

print("==> Found all required python packages.\n")

# clone git repo if not exists already
try:
    repo = git.Repo(os.path.dirname(os.path.abspath(__file__)))
    print("==> Found local git repo\n")
except git.exc.InvalidGitRepositoryError:
    print("==> Local git repo NOT found. Will fetch one from the Internet. You will see a new directory created at the end.\n")
    if not os.path.exists(SCRIPT_WORK_DIR):
        try:
            repo = git.Repo.clone_from(GIT_REPO_URL, SCRIPT_WORK_DIR)
            os.unlink(os.path.abspath(__file__))
            print ("==> Just execute this script again from SDAPOVFASTFORWARD directory\n")
        except Exception as e:
            print("==> Git repo reading exception %s. So exiting." % str(e))
    else:
        print("==> Cannot fetch git repo since a local directory SDAPOVFASTFORWARD exists. Kindly delete or rename that directory to something else and try again.\n")
    input("Press <enter> to exit")
    os._exit(0)
except Exception as e:
    print("==> Git repo reading exception %s. So exiting." % str(e))
    input("Press <enter> to exit")
    os._exit(0)

# calculating self checksum
orig_sum = hashlib.md5(open(os.path.abspath(__file__),"rb").read()).hexdigest()

# update local git repo
try:
    repo = git.Repo(os.path.dirname(os.path.abspath(__file__)))
    print("==> Checking for code updates.\n")
    repo.remotes.origin.fetch()
    repo.remotes.origin.pull()
    print("==> Update check complete.\n")
    new_sum = hashlib.md5(open(os.path.abspath(__file__),"rb").read()).hexdigest()
    if new_sum != orig_sum:
        print("==> This script is updated. So you need to execute it again.")
        input("Press <enter> to exit")
        os._exit(0)
except Exception as e:
    if "commit your changes" in str(e):
        print("==> It seems you modified the script files locally. So the script cannot pull and overwrite the new updates.\n")
        while True:
            a = input("Would you like to override the local changes before updating? [Y/N] ")
            if a.lower() in ["yes","y"]:
                repo.git.reset('--hard','origin/master')
                repo.remotes.origin.pull()
                print("\n==> Local changes are overwritten and update is complete.\n")
                break
            elif a.lower() in ["no","n"]:
                while True:
                    print("")
                    a = input("Would you like to continue with existing version of the script? [Y/N] ")
                    if a.lower() in ["yes","y"]:
                        print("\n==> Will continue with existing version of the script.\n")
                        break
                    elif a.lower() in ["no","n"]:
                        input("Press <enter> to exit")
                        os._exit(0)
                    else:
                        print("Enter either yes/no")
                break
            else:
                print("Enter either yes/no")
    else:
        print("==> Could NOT check for updates due to the following exception - %s" % str(e))
        print("==> Will continue with existing version of the script.\n")
    

# checking if node.js exists for - "newman" program
try:
    subprocess.check_output(["node", "-v"])
    print("==> Found NODE.JS\n")
except OSError as e:
    print ("==> It seems NODE.JS is NOT installed on your system. NODE.JS is required. This scipt will attempt to download and install NODE.JS")
    while True:
        print("")
        a = input("Would you like to continue with download and installation of NODE.JS? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("Press <enter> to exit")
            os._exit(0)
        else:
            print("Enter either yes/no")
    
    print("\n==> Downloading NODE.JS setup. This takes a few minutes")
    if platform.system().lower() == "windows":
        if platform.machine().endswith('64'):
            url = "https://nodejs.org/dist/v12.13.0/node-v12.13.0-x64.msi"
            wget.download(url, "./")
            print("\n\n==> Installing NODE.JS setup. This takes a few minutes")
            subprocess.call('msiexec.exe /qb /i node-v12.13.0-x64.msi')
        else:
            url = "https://nodejs.org/dist/v12.13.0/node-v12.13.0-x86.msi"
            wget.download(url, "./")
            print("\n\n==> Installing NODE.JS setup. This takes a few minutes")
            subprocess.call('msiexec.exe /qb /i node-v12.13.0-x86.msi')
        
        print("\n==> NODE.JS installation is complete.  Now run this script again so that the script can use it.")
        input("Press <enter> to exit")
        os._exit(0)
    elif platform.system().lower() == "darwin":
            url = "https://nodejs.org/dist/v12.13.0/node-v12.13.0.pkg"
            wget.download(url, "./")
            print("NODE.JS is downloaded. Just double-click to install it and then run this script again.")
            input("Press <enter> to exit")
            os._exit(0)
    else:
        print("This script is running on an unsupported OS. Currently only Windows and MAC are supported.")
        input("Press <enter> to exit")
        os._exit(0)


# checking for the existence of node- "newman"
try:
    subprocess.check_output(["newman", "-v"], shell=True)
    print("==> Found NEWMAN (cli-based POSTMAN) node package\n")
except subprocess.CalledProcessError as e:
    print ("\n==> It seems NEWMAN (cli-based POSTMAN) node package is NOT installed. \nThis scipt will attempt to download and install NEWMAN (cli-based POSTMAN) node package")
    while True:
        print("")
        a = input("Would you like to continue with download and installation of NEWMAN (cli-based POSTMAN) node package? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("Press <enter> to exit")
            os._exit(0)
        else:
            print("Enter either yes/no")
    
    print("\n==> Installing NEWMAN (cli-based POSTMAN) package setup. This takes a few minutes")
    subprocess.call(["npm", "install", "-g", "newman"], shell=True)
    print("")
    try:
        subprocess.check_output(["newman", "-v"], shell=True)
        print("==> NEWMAN (cli-based POSTMAN) package installed successfully\n")
    except subprocess.CalledProcessError as e:
        print("NEWMAN (cli-based POSTMAN) package could not be installed automatically. try installing it manually using the command \"node install -g newman\" and then run this script again.")
        input("Press <enter> to exit")
        os._exit(0)

# now the core part
print("==> All dependencies checked. Now lets get into action")

# search for postman collections and ask the user to choose one
print("\n")
all_postman_collection_files = [f for f in os.listdir(SCRIPT_WORK_DIR_POSTMAN) if os.path.isfile( os.path.join(SCRIPT_WORK_DIR_POSTMAN, f) ) and POSTMAN_COLLECTION_FILTER in f ]
if len(all_postman_collection_files) > 0:
    print("==> The following Postman Collections were found:")
    count = 0
    for f in all_postman_collection_files:
        count+=1
        print("%s - %s" % (count,f) )
else:
    print("==> Could not find any file that appear to be a Postman Collection!")
    input("Press <enter> to exit")
    os._exit(0)

selected_postman_collection_file = ''
if len(all_postman_collection_files)==1:
    selected_postman_collection_file = all_postman_collection_files[0]
    while True:
        a = input("\nWould you like to continue with this option? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("Press <enter> to exit")
            os._exit(0)
        else:
            print("Enter either yes/no")
else:
    while True:
        print("")
        try:
            a = int(input("Which one would you like to utilize? [1-%s] " % (len(all_postman_collection_files)) ))
            selected_postman_collection_file = all_postman_collection_files[a-1]
            print("\nYou have selected Postman Collection:- %s" % (selected_postman_collection_file) )
            
            a = input("\nWould you like to continue with this option? [Y/N] ")
            if a.lower() in ["yes","y"]:
                break
            elif a.lower() in ["no","n"]:
                input("Press <enter> to exit")
                os._exit(0)
        except:
            print("That's not a valid option!")


# search for postman environments and ask the user to choose one
print("\n")
all_postman_environment_files = [f for f in os.listdir(SCRIPT_WORK_DIR_POSTMAN) if os.path.isfile( os.path.join(SCRIPT_WORK_DIR_POSTMAN, f) ) and POSTMAN_ENVIRONMENT_FILTER in f ]
if len(all_postman_environment_files) > 0:
    print("==> The following Postman Environments were found.")
    count = 0
    for f in all_postman_environment_files:
        count+=1
        print("%s - %s" % (count,f) )
else:
    print("==> Could not find any file that appear to be a Postman Environment!")
    input("Press <enter> to exit")
    os._exit(0)

selected_postman_environment_file = ''
if len(all_postman_environment_files)==1:
    selected_postman_environment_file = all_postman_environment_files[0]
    while True:
        a = input("\nWould you like to continue with this option? [Y/N] ")
        if a.lower() in ["yes","y"]:
            break
        elif a.lower() in ["no","n"]:
            input("Press <enter> to exit")
            os._exit(0)
        else:
            print("Enter either yes/no")
else:
    while True:
        print("")
        try:
            a = int(input("Which one would you like to utilize? [1-%s] " % (len(all_postman_environment_files)) ))
            selected_postman_environment_file = all_postman_environment_files[a-1]
            print("\nYou have selected Postman Environment:- %s" % (selected_postman_environment_file) )
            
            a = input("\nWould you like to continue with this option? [Y/N] ")
            if a.lower() in ["yes","y"]:
                break
            elif a.lower() in ["no","n"]:
                input("Press <enter> to exit")
                os._exit(0)
        except:
            print("That's not a valid option!")


# Now lets run the "newman"
while True:
    print("\n==> With the following selection?\nPostman Collection - %s\nPostman Environment - %s\n" % (selected_postman_collection_file,selected_postman_environment_file))
    a = input("\nAre you ready to fast forward your SDA POV? [Y/N] ")
    if a.lower() in ["yes","y"]:
        break
    elif a.lower() in ["no","n"]:
        input("Press <enter> to exit")
        os._exit(0)
    else:
        print("Enter either yes/no")

print("\n\n==> Executing NEWMAN (cli-based POSTMAN) now to run the API calls\n")
subprocess.call(["newman", "run", os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_collection_file), "-e", os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_environment_file), "-k"], shell=True)

print("\n\n==> If all API calls worked in the above run then you are all set.\n")
input("Press <enter> to exit")
os._exit(0)
