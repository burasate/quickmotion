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
    raise Warning('WARNING!!\ndo not found \"Install.mel\" in {}'.format(tool_dir))

"""====================="""
# Gumroad License Key
"""====================="""
'''
gr_url = 'https://raw.githubusercontent.com/burasate/AniMateAssist/main/service/licsence.py'
gr_u_read = uLib.urlopen(gr_url).read()
gr_perma = 'uznhu'
gr_tool_name = 'BRS Quick Motion'
exec(gr_u_read)
grl = gr_license(product_name=gr_tool_name, product_code=gr_perma)
grl.show_ui()
print(grl.verify_result)
'''

"""====================="""
# Orig User Register to Files
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
        l_read_join = ''.join(l_read)
        is_registered = not '$usr_orig$' in l_read_join
        f.close()
    if not is_registered:
        l_read_join = l_read_join.replace('$usr_orig$', getpass.getuser())
        with open(pt_path, 'w') as f:
            f.writelines(l_read_join)
            f.close()
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

cmds.shelfButton(stp='python', iol='QM', parent=cur_shelf, ann='BRS QUICK MOTION', i=image_path, c=command)
cmds.confirmDialog(title='BRS QUICK MOTION', message='Installation Successful.', button=['OK'])
