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
    import os, base64, getpass
    is_py3 = sys.version[0] == '3'
    if is_py3:
        import urllib.request as uLib
    else:
        import urllib as uLib

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

    """====================="""
    # Orig User Register to Files
    """====================="""
    py_ls = ['QuickMotion.py', 'quickmocap/quickmocap.py', 'rtgmatcher/rtgmatcher.py']
    py_file_path_ls = [src_dir + os.sep + i for i in py_ls]
    #pt_file_path_ls = [i for i in pt_file_path_ls if os.path.exists(i)]
    src_url = 'https://raw.githubusercontent.com/burasate/quickmotion/main/service/update'
    for py_path, src_py in zip(py_file_path_ls, py_ls):
        if not os.path.exists(py_path): continue
        #print(py_path)
        #print(py_path[len(src_dir):])
        #print(src_url + py_path[len(src_dir):].replace('\\','/'))
        url = src_url + '/' + src_py


        response = uLib.urlopen(url)
        read = response.read()
        read = read.decode('utf-8') if type(read) == type(b'') else read
        username = getpass.getuser()
        u_read = read.replace('$usr_orig$', username)
        print('------------')
        #print(u_read)
        print('url', url, py_path)
        with open(py_path, 'w') as f:
            f.writelines(u_read)
            f.close()
            print('{}  is  updated..'.format(py_path))

        '''
        is_registered = False
        with open(py_path, 'r') as f:
            l_read = f.readlines()
            l_read_join = ''.join(l_read)
            is_registered = not '$usr_orig$' in l_read_join
            f.close()
        print('is_registered', is_registered)
        '''

        '''
        l_read_join = l_read_join.replace('$usr_orig$', getpass.getuser())
        with open(py_path, 'w') as f:
            f.writelines(l_read_join)
            f.close()
        print('update : ', py_path)
        '''

update_version()
