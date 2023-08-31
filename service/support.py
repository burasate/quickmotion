#---------------------
#Quick Motion
#Support Service
#---------------------
from maya import cmds
from maya import mel
import os, json, sys, getpass

print('Quick Motion Support Service')
#-----------------------


"""====================="""
# Update version of Quick Motion
"""====================="""
def update_version():
    maya_app_dir = mel.eval('getenv MAYA_APP_DIR')
    scripts_dir = os.path.abspath(maya_app_dir + os.sep + 'scripts')
    tool_dir = os.path.abspath(scripts_dir + os.sep + 'BRSQuickMotion')
    install_path = os.path.abspath(tool_dir + os.sep + 'Install.mel')
    src_dir = os.path.abspath(tool_dir + os.sep + 'src')
    image_path = os.path.abspath(tool_dir + os.sep + 'BRSQuickMotion.png')
    print(tool_dir, os.path.exists(tool_dir))
    print(install_path, os.path.exists(install_path))
    print(src_dir)
    print(image_path)
update_version()
