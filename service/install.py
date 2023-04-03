"""
QUICK MOTION SHELF INSTALLER
"""
from maya import cmds
from maya import mel
import os, json, sys, getpass

"""====================="""
# Init
"""====================="""
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

if not os.path.exists(tool_dir) or not os.path.exists(install_path):
    raise Warning('Install.mel  not found in {}'.format(tool_dir))

"""====================="""
# Orig User Register
"""====================="""
pt_file_path_ls = [
    os.path.abspath(src_dir + os.sep + 'QuickMotion.py'),
    os.path.abspath(src_dir + os.sep + 'quickmocap/quickmocap.py'),
    os.path.abspath(src_dir + os.sep + 'rtgmatcher/rtgmatcher.py')
]
pt_file_path_ls = [i for i in pt_file_path_ls if os.path.exists(i)]
for pt_path in pt_file_path_ls:
    is_registered = False
    with open(pt_path, 'r') as f:
        l_read = f.readlines()
        l_read_join = '\n'.join(l_read)
        is_registered = not '$usr_orig$' in l_read_join
        f.close()
    if not is_registered:
        print(l_read_join)
        print(pt_path)


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

if not r\'{0}\' in sys.path:
    sys.path.insert(0, r\'{0}\')

import imp
try: imp.reload(QuickMotion)
except:
    import QuickMotion

qm = QuickMotion.quickMotion_Ui()
qm.show_ui()
'''.format(src_dir)

#cmds.shelfButton(stp='python', iol='QM', parent=cur_shelf, ann='BRS QUICK MOTION', i=image_path, c=command)
#cmds.confirmDialog(title='BRS QUICK MOTION', message='Installation Successful.', button=['OK'])
