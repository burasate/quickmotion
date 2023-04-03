"""
QUICK MOTION SHELF INSTALLER
"""
from maya import cmds
from maya import mel
import os, json, sys

maya_app_dir = mel.eval('getenv MAYA_APP_DIR')
scripts_dir = os.path.abspath(mayaAppDir + os.sep + 'scripts')
tool_dir = os.path.abspath(scripts_dir + os.sep + 'BRSQuickMotion')
print(tool_dir, os.path.exists(tool_dir))

"""
from maya import cmds
from maya import mel
import os, json, sys
import datetime as dt
import getpass,base64

def formatPath(path):
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

mayaAppDir = formatPath(mel.eval('getenv MAYA_APP_DIR'))
scriptsDir = formatPath(mayaAppDir + os.sep + 'scripts')
projectDir = formatPath(scriptsDir + os.sep + 'BRSLocDelay')
userFile = formatPath(projectDir + os.sep + 'user')

# -------------
# CREATE USER
# -------------
today = str(dt.date.today())
dataSet = {}

try:
    with open(userFile, 'r') as f:
        dataSet = json.load(f)
except:
    # Email Register
    while True:
        user = cmds.promptDialog(
            title='BRS Loc Delay Register',
            message='BRS Loc Delay Register\nConfirm Your Purchase Email',
            button=['Confirm'],
            defaultButton='Confirm',
            cancelButton='Cancel',
            dismissString='Cancel', bgc=(.2, .2, .2))
        if user == 'Confirm':
            dataSet['email'] = cmds.promptDialog(query=True, text=True)
        else:
            dataSet['email'] = ''

        if not '@' in dataSet['email'] or not '.' in dataSet['email']:
            pass
        elif len(dataSet['email'].split('@')[0]) < 3:
            pass
        else:
            break

    # Create New Dataset
    dataSet['isTrial'] = True
    dataSet['registerDate'] = today
    dataSet['lastUsedDate'] = today
    dataSet['lastUpdate'] = today
    dataSet['days'] = 0
    dataSet['used'] = 0
    dataSet['version'] = 1.2
    dataSet['regUser64'] = base64.b64encode(getpass.getuser())
    dataSet['licenseKey'] = ''

    # Create User
    if sys.version[0] == '3':
        with open(userFile, 'w') as jsonFile:
            json.dump(dataSet, jsonFile, indent=4)
    else:
        with open(userFile, 'wb') as jsonFile:
            json.dump(dataSet, jsonFile, indent=4)

finally:
    # Create Shelf
    topShelf = mel.eval('$nul = $gShelfTopLevel')
    currentShelf = cmds.tabLayout(topShelf, q=1, st=1)
    #command = 'from BRSLocDelay import BRSLocDelaySystem \
    #\nBRSLocDelaySystem.showBRSUI()'

    command = '''
#------------------------------------
# BRS LOCATOR DELAY
# OVERLAPPING TOOL
#------------------------------------
import imp
try:
    imp.reload(BRSLocDelaySystem)
except:
    from BRSLocDelay import BRSLocDelaySystem 

BRSLocDelaySystem.showBRSUI()
'''

    imagePath = projectDir + os.sep + 'BRSLocDelaySystem.png'
    cmds.shelfButton(stp='python', iol='DELAY', parent=currentShelf, ann='BRS LOCATOR DELAY SYSTEM', i=imagePath, c=command)

    # Finish
    cmds.confirmDialog(title='BRS LOCATOR DELAY', message='Installation Successful.', button=['OK'])
    try:
        exec (command)
    except:pass

"""