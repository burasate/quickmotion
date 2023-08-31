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