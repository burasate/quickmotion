# For Autodesk Maya
from maya import mel
import maya.cmds as cmds
import sys, json, ssl

class gr_license:
    def __init__(self, product_name, product_code):
        self.product_name = product_name
        self.product_code = product_code
        self.ui_element = {}
        self.verify_result = False
        self.win_id = 'BRSACTIVATOR'

    is_py3 = str(sys.version[0]) == '3'
    if is_py3:
        import urllib.request as uLib
    else:
        import urllib as uLib

    def get_license_verify(self, key):
        '''
        :param key: buy license key
        :return: email and license key
        '''
        license_key, license_email = ['','']

        if not cmds.about(cnt=1):
            return None

        url_verify = 'https://api.gumroad.com/v2/licenses/verify'
        data = {
            'product_permalink': self.product_code,
            'license_key': key,
            'increment_uses_count': 'false'
        }

        if gr_license.is_py3:
            import urllib.parse
            verify_params = urllib.parse.urlencode(data)
        else:
            verify_params = gr_license.uLib.urlencode(data)
        verify_params = verify_params.encode('ascii')
        #print(verify_params)
        response = gr_license.uLib.urlopen(url_verify, verify_params, context=ssl._create_unverified_context())
        license = json.loads(response.read())
        #print(license)
        if license['success']:
            #print(license['message'] + '\n')
            license_key = license['purchase']['license_key']
            license_email = license['purchase']['email']
        return (license_key, license_email)

    def do_verify(self, *_):
        agreement_accept = cmds.checkBox(self.ui_element['agreement_accept'], q=1, v=1)
        if not agreement_accept:
            return None
        email = cmds.textField(self.ui_element['email_text'], q=1, tx=1)
        key = cmds.textField(self.ui_element['key_text'], q=1, tx=1)
        print(email, key),

        verify = self.get_license_verify(key=key)
        print(verify == None)
        if verify == None:
            cmds.warning('Please make sure the internet connection is connect')
            return None

        found_license_key = verify[0] != '' and verify[1] == email
        #print(found_license_key)
        self.verify_result = found_license_key

        if self.verify_result:
            msg_dialog = '''
Email : {}
Product key : {}

Thank you for purchasing our product
Have a nice day!
'''.format(email, key)
            cmds.confirmDialog(title='Found Licence Key', message=msg_dialog, button=['Continue'])
            self.close_ui()
            # get self.verify_result to record
        else:
            msg_dialog = '''
Can\'t verify!
Please check your email or license key

https://app.gumroad.com/library
'''
            cmds.confirmDialog(title='Cannot Found Licence Key', message=msg_dialog, button=['OK'])
            print('')

    def show_ui(self):
        win_width = 600

        if cmds.window(self.win_id, exists=True):
            cmds.deleteUI(self.win_id)
        cmds.window(self.win_id, t='DEX3D Gumroad License Argeement',
            w=win_width, sizeable=1, h=10,
            retain=0, bgc=(.2, .2, .2))

        cmds.columnLayout(adj=0, w=win_width)

        cmds.text(l='', fn='boldLabelFont', h=30, w=win_width)

        ct_w_percentile = win_width*.88
        bd_w_percentile = (win_width-ct_w_percentile)*.5
        cmds.rowLayout(numberOfColumns=3,
                       columnWidth3=(bd_w_percentile, ct_w_percentile,bd_w_percentile),
                       columnAlign3=['center', 'center', 'center'], adj=2)
        cmds.columnLayout(adj=0);cmds.setParent('..')

        cmds.columnLayout(adj=0, w=ct_w_percentile)

        eula_message = '''
{0}
END USER LICENSE AGREEMENT
=======================================

Last updated: December 22, 2022

IMPORTANT- READ CAREFULLY: 
THIS EULA IS A LEGAL AGREEMENT BETWEEN YOU (EITHER AN INDIVIDUAL OR A SINGLE ENTITY) AND THE AUTHOR OF TWEENER. BY INSTALLING, COPYING, OR OTHERWISE USING THE TWEENER SOFTWARE, YOU AGREE TO BE BOUND BY THE TERMS OF THIS AGREEMENT.

LICENSE GRANT: 
The author grants you a non-exclusive, non-transferable license to use the {1} maya script in accordance with the terms and conditions of this EULA.

USE: 
You may use the {1} maya script for personal or commercial purposes. You may not sell, rent, lease, or distribute the {1} maya script or any portion of it to any third party.

OWNERSHIP: 
The author owns all right, title, and interest in and to the {1} maya script, including any and all intellectual property rights. You acknowledge that you have no ownership or other proprietary interest in the {1} maya script.

LIMITATIONS: 
You may not modify, reverse engineer, decompile, disassemble, or create derivative works based on the {1} maya script. You may not remove or modify any copyright notices or other proprietary notices on the {1} maya script. You may not use the {1} maya script to develop or distribute software that competes with the {1} maya script.

DISCLAIMER OF WARRANTIES: 
The {1} maya script is provided "AS IS," without warranty of any kind. The author does not warrant that the {1} maya script will meet your requirements or that the operation of the {1} maya script will be uninterrupted or error-free.

LIMITATION OF LIABILITY: 
The author will not be liable for any indirect, incidental, special, or consequential damages arising out of the use or inability to use the {1} maya script, even if the author has been advised of the possibility of such damages. In no event shall the author's liability exceed the purchase price paid for the {1} maya script.

TERMINATION: 
This EULA will terminate immediately if you breach any of its terms. Upon termination, you must destroy all copies of the {1} maya script in your possession.

GOVERNING LAW: 
This EULA shall be governed by and construed in accordance with the laws of the jurisdiction in which the author resides.

ENTIRE AGREEMENT: 
This EULA constitutes the entire agreement between you and the author with respect to the {1} maya script and supersedes all prior or contemporaneous communications and proposals, whether oral or written.

SEVERABILITY: 
If any provision of this EULA is held to be invalid or unenforceable, the remaining provisions will remain in full force and effect.

By installing, copying, or otherwise using the {1} maya script, you acknowledge that you have read this EULA, understand it, and agree to be bound by its terms and conditions. If you do not agree to the terms and conditions of this EULA, do not use the {1} maya script.
'''.format(self.product_name.upper(), self.product_name)
        eula_message = '\n'.join([i.center(int(round(ct_w_percentile*.13,0)), ' ') for i in eula_message.split('\n')])

        cmds.scrollField(h=150, w=ct_w_percentile, editable=0, wordWrap=1, text=eula_message, bgc=(.95,.95,.8))
        cmds.text(l='', h=15, w=ct_w_percentile)
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(ct_w_percentile * .2, ct_w_percentile * .8),
                       columnAlign2=['right', 'left'], adj=1, h=30)
        cmds.text(al='right', l='')
        self.ui_element['agreement_accept'] = cmds.checkBox(label='I accept the terms in the License Agreement', v=1)
        cmds.setParent('..')
        cmds.text(l='', h=15, w=ct_w_percentile)

        cmds.rowLayout(numberOfColumns=2, columnWidth2=(ct_w_percentile * .2, ct_w_percentile * .8),
                       columnAlign2=['right', 'left'], adj=1, h=30)
        cmds.text(al='right', l='Product Name : ')
        cmds.textField(tx=self.product_name, ed=0, w=ct_w_percentile * .7)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(ct_w_percentile*.2, ct_w_percentile*.8),
                       columnAlign2=['right', 'left'], adj=1, h=30)
        cmds.text(al='right', l='Product Code : ')
        cmds.textField(tx=self.product_code, ed=0, w=ct_w_percentile * .7)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(ct_w_percentile * .2, ct_w_percentile * .8),
                       columnAlign2=['right', 'left'], adj=1, h=30)
        cmds.text(al='right', l='Email Address : ')
        self.ui_element['email_text'] = cmds.textField(tx='', w=ct_w_percentile * .7)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(ct_w_percentile * .2, ct_w_percentile * .8),
                       columnAlign2=['right', 'left'], adj=1, h=30)
        cmds.text(al='right', l='License Key : ')
        self.ui_element['key_text'] = cmds.textField(tx='', w=ct_w_percentile * .7)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(ct_w_percentile * .2, ct_w_percentile * .8),
                       columnAlign2=['right', 'left'], adj=1, h=30)
        cmds.text(al='right', l='')
        cmds.button(l='Register and Verify', al='center', w=150, bgc=(.4,.4,.4), c=self.do_verify)
        cmds.setParent('..')

        cmds.setParent('..') #columnLayout

        cmds.columnLayout(adj=0);cmds.setParent('..')
        cmds.setParent('..') #rowLayout2

        cmds.text(l='', h=30, w=ct_w_percentile)

        cmds.showWindow(self.win_id)

    def close_ui(self):
        cmds.deleteUI(self.win_id)

# How to
#grl = gr_license(product_name = 'BRS Quick Motion', product_code = 'uznhu')
#grl.show_ui()
