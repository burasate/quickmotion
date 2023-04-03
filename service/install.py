"""
QUICK MOTION SHELF INSTALLER
"""
from maya import cmds
from maya import mel
import os, json, sys

"""====================="""
# Init
"""====================="""
maya_app_dir = mel.eval('getenv MAYA_APP_DIR')
scripts_dir = os.path.abspath(mayaAppDir + os.sep + 'scripts')
tool_dir = os.path.abspath(scripts_dir + os.sep + 'BRSQuickMotion')
install_path = os.path.abspath(tool_dir + os.sep + 'Install.mel')
src_dir = os.path.abspath(tool_dir + os.sep + 'src')
image_path = os.path.abspath(tool_dir + os.sep + 'BRSQuickMotion.png')
print(tool_dir, os.path.exists(tool_dir))
print(install_path, os.path.exists(install_path))
print(src_dir)
print(image_path)

if not os.path.exists(tool_dir) or not os.path.exists(install_path):
    raise Warning('Install.mel  not found in {}'.format(tool_dir))

"""====================="""
# Shelf
"""====================="""
# Create Shelf
top_shelf = mel.eval('$nul = $gShelfTopLevel')
cur_shelf = cmds.tabLayout(top_shelf, q=1, st=1)
command = '''
# -----------------------------------
# BRS QUICK MOTION
# dex3d.gumroad.com
# -----------------------------------
import os, sys

if not \'{0}\' in sys.path:
    sys.path.insert(0, \'{0}\')

import QuickMotion
qm = quickMotion_Ui()
qm.show_ui()
'''.format(src_dir)
#cmds.shelfButton(stp='python', iol='QM', parent=cur_shelf, ann='BRS QUICK MOTION', i=image_path, c=command)
cmds.confirmDialog(title='BRS QUICK MOTION', message='Installation Successful.', button=['OK'])