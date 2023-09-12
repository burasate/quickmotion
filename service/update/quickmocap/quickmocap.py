# -*- coding: utf-8 -*-
# Quick Mocap
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

#-------------------------------------
# Init Library
#-------------------------------------
if not base_dir in sys.path:
    sys.path.insert(0, base_dir)
import imp, animproc, animexport
imp.reload(animproc)
imp.reload(animexport)

# ----------------Init Plugin-----------------------
cmds.loadPlugin( 'fbxmaya.mll' )
cmds.loadPlugin( 'lookdevKit.mll' )

class quickMocap_func:
    def __init__(self):
        self.rtg_profile = None
        self.mocap_tc_ls = None
        self.namespace = None

    @staticmethod
    def new_scene():
        result = cmds.confirmDialog(message='New Scene without Save?',
                                    button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if result == 'Yes':
            cmds.file(newFile=1, force=1, prompt=1)
        else:
            raise Warning('Cancel')

    def get_import_rtg(self, last_dir):
        quickMocap_func.new_scene()
        result = cmds.fileDialog(dm=last_dir + os.sep + '*_rtg_*.ma')
        if result != '':
            print(result)
            before_ref = cmds.ls(type='reference')
            cmds.file(
                result,
                i=1,  # type="mayaBinary",
                ignoreVersion=1,
                mergeNamespacesOnClash=0, options='v=0;',
                importFrameRate=0, preserveReferences=1
            )
            after_ref = [r for r in cmds.ls(type='reference') if not r in before_ref]
            ref_sel = after_ref[0]
            ref_ns = cmds.referenceQuery(ref_sel, namespace=1).replace(':', '')
            self.namespace = ref_ns

            # Set viewport focus
            cmds.viewFit(all=1, ns=ref_ns, an=1)

            # Profile
            with open(result.replace('.ma', '.json')) as f:
                self.rtg_profile = json.load(f)
                f.close()

            return {
                'namespace' : ref_ns,
                'profile' : self.rtg_profile,
                'last_dir' : os.path.dirname(result)
            }
        else:
            return None

    def get_import_mocap_fbx(self, last_dir):
        result = cmds.fileDialog(dm=last_dir + os.sep + '*.fbx')
        result = str(result)
        if result != '':
            print(result)
            before_ac = cmds.ls(type='animCurve')
            cmds.file(
                result,
                i=1, type="fbx",
                ignoreVersion=1,
                mergeNamespacesOnClash=0, options='v=0;',
                importFrameRate=0, preserveReferences=1
            )
            after_ac = [r for r in cmds.ls(type='animCurve') if not r in before_ac]
            keyframes = cmds.keyframe(after_ac, q=1, tc=1)
            keyframes = list(set([round(i,0) for i in keyframes]))
            self.mocap_tc_ls = keyframes
            cmds.playbackOptions(
                e=1, ast=min(keyframes),
                aet=max(keyframes), min=min(keyframes),
                max=max(keyframes)
            )

            return {
                'fbx_path' : result,
                'frame_start' : min(keyframes),
                'frame_end' : max(keyframes),
                'last_dir' : os.path.dirname(result)
            }
        else:
            return None

    def get_rtg_ctrl(self):
        ctrl_ls = ['{}:{}'.format(self.namespace, self.rtg_profile[i])
                for i in self.rtg_profile]
        ctrl_ls = [i for i in ctrl_ls if cmds.objExists(i)]
        return ctrl_ls

    def bake_anim_rtg(self, f_st, f_en):
        ctrl_ls = self.get_rtg_ctrl()
        at = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        cmds.refresh(suspend=1)
        cmds.bakeResults(ctrl_ls, simulation=1, sampleBy=1, disableImplicitControl=1, preserveOutsideKeys=0,
                         sparseAnimCurveBake=0, t=(f_st, f_en), at=at, minimizeRotation=1)
        cmds.refresh(suspend=0)
        cmds.filterCurve(ctrl_ls)
        self.clear_static_anim()

        cmds.select(ctrl_ls)

    def clear_static_anim(self):
        ctrl_ls = self.get_rtg_ctrl()
        ac_ls = cmds.keyframe(ctrl_ls, q=1, n=1)
        for ac in ac_ls:
            tc = cmds.keyframe(ac, q=1, tc=1)
            vc = cmds.keyframe(ac, q=1, vc=1)
            if min(vc) == max(vc) and len(vc) > 3:
                cmds.cutKey(ac, t=(tc[1], tc[-2]))

    def delete_rtg_skeleton(self):
        scale_grp = cmds.ls(['*global_scale_grp', '::global_scale_grp'],type='transform')
        cmds.delete(scale_grp)
        '''
        ctrl_ls = self.get_rtg_ctrl()
        con_ls = list(set(cmds.listConnections(ctrl_ls, type='constraint')))
        joint_ls = list(set(cmds.listConnections(con_ls, s=1, d=0, type='joint')))
        print(con_ls)
        print(joint_ls)
        parent = list(set(cmds.listRelatives(joint_ls, ap=1)))
        cmds.delete(parent)
        '''

class quickMocap_gui:
    def __init__(self):
        self.version = 0.01
        self.win_id = 'BRS_QUICKMOCAP'
        self.dock_id = self.win_id + '_DOCK'
        self.win_width = 300
        self.win_title = 'Quick Retarget -  v.{}'.format(self.version)
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
        self.cfg_path = base_dir + os.sep + 'config.json'
        self.cfg = None
        self.func = None

        import getpass
        self.user_original, self.user_latest = ['$usr_orig$', getpass.getuser()]
        if self.user_original == self.user_latest:
            self.func = quickMocap_func()

    def init_config(self):
        data = {
            'rtg_dir' : base_dir,
            'mocap_dir' : base_dir,
            'anim_export_dir' : base_dir
        }
        if not os.path.exists(self.cfg_path):
            with open(self.cfg_path, 'w') as f:
                json.dump(data, f, indent=4)
                f.close()
        self.cfg = self.get_config()

    def get_config(self):
        with open(self.cfg_path, 'r') as f:
            return json.load(f)

    def save_config(self):
        with open(self.cfg_path, 'w') as f:
            json.dump(self.cfg, f, indent=4)
            f.close()

    def init_win(self):
        if cmds.window(self.win_id, exists=1):
            cmds.deleteUI(self.win_id)
        cmds.window(self.win_id, t=self.win_title, menuBar=1, rtf=1, nde=1,
                    w=self.win_width, sizeable=1, h=10, retain=0, bgc=self.color['bg'])

    def win_layout(self):
        self.element['tab'] = cmds.columnLayout(adj=1, w=self.win_width)
        #cmds.text(l='{}'.format(self.win_title), al='center', fn='boldLabelFont', bgc=self.color['shadow'], h=15)
        cmds.text(l='', al='center', fn='boldLabelFont', bgc=self.color['shadow'], h=5)

        cmds.text(l=' CHARACTER RIG', fn='smallPlainLabelFont', al='left', w=self.win_width,
                  bgc=self.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)

        cmds.rowColumnLayout(numberOfColumns=3, w=self.win_width)
        cmds.text(l='', w=self.win_width * .2)
        cmds.button(l='Load RTG', w=self.win_width * .6, bgc=self.color['highlight'],
                    c=lambda arg: self.import_rtg_file())
        cmds.text(l='', w=self.win_width * .2)
        cmds.text(l='', w=self.win_width * .2)
        self.element['namespace_tf'] = cmds.text(al='center', w=self.win_width * .6, l='', h=18,
                                                 bgc=self.color['shadow'])
        cmds.text(l='', w=self.win_width * .2)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)
        cmds.text(l=' MOTION CAPTURE', fn='smallPlainLabelFont', al='left', w=self.win_width,
                  bgc=self.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)

        cmds.rowColumnLayout(numberOfColumns=3, w=self.win_width)
        cmds.text(l='', w=self.win_width * .2)
        cmds.button(l='Load FBX', w=self.win_width * .6, bgc=self.color['highlight'],
                    c=lambda arg: self.import_fbx_file())
        cmds.text(l='', w=self.win_width * .2)
        cmds.text(l='', w=self.win_width * .2)
        self.element['mocap_file_tf'] = cmds.text(al='center', w=self.win_width * .6, l='', h=18,
                                                 bgc=self.color['shadow'], )
        cmds.text(l='', w=self.win_width * .2)
        cmds.setParent('..')

        cmds.text(l='', al='center', fn='boldLabelFont', bgc=self.color['bg'], h=5)
        cmds.rowColumnLayout(numberOfColumns=4, w=self.win_width)

        cmds.text(l='', w=self.win_width * .2)
        self.element['bake_frame_in'] = cmds.intField(w=self.win_width * .3, ed=0)
        self.element['bake_frame_out'] = cmds.intField(w=self.win_width * .3, ed=0)
        cmds.text(l='', w=self.win_width * .2)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)
        cmds.text(l=' ANIMATION', fn='smallPlainLabelFont', al='left', w=self.win_width,
                  bgc=self.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)

        cmds.rowColumnLayout(numberOfColumns=4, w=self.win_width)
        for i in self.aap_reg_ls:
            cmds.text(l='', w=self.win_width * .2)
            self.element[i['cb_name']] = cmds.checkBox(l=i['name'], v=0)
            if i['op_name'] != None:
                self.element[i['op_name']] = cmds.floatField(v=i['op_value'], pre=1)
            else:
                cmds.text(l='')
            #self.element[i['sname']+'_st'] = cmds.text(l='', w=self.win_width * .03, bgc=self.color['shadow'])
            #self.element[i['sname']+'_st'] = cmds.text(l='', w=self.win_width * .03, bgc=self.color['shadow'])
            #cmds.text(al='left', l='  {}'.format(i['name']), w=self.win_width * .57)
            #self.element[i['sname']+'_bt'] = cmds.button(l='<', w=self.win_width * .1,
                                                           #bgc=self.color['highlight'], c=i['cmd'])
            cmds.text(l='', w=self.win_width * .2)
        cmds.setParent('..')

        cmds.text(l='', al='center', fn='boldLabelFont', bgc=self.color['bg'], h=5)
        cmds.rowColumnLayout(numberOfColumns=3, w=self.win_width)
        cmds.text(l='', w=self.win_width * .2)
        self.element['bake_anim_bt'] = cmds.button(l='Bake Animation', w=self.win_width * .6, bgc=self.color['highlight'],
                    c=lambda arg: self.bake_anim())
        cmds.text(l='', w=self.win_width * .2)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)
        cmds.text(l=' EXPORT ANIM', fn='smallPlainLabelFont', al='left', w=self.win_width,
                  bgc=self.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)

        self.element['export_to_option'] = cmds.optionMenu(label=' Format :', w=self.win_width,
                                                         bgc=self.color['highlight'], cc=lambda arg: self.update_ui())
        for item in self.ae_reg_ls:
            cmds.menuItem(label=item['name'])

        cmds.text(l='', al='center', fn='boldLabelFont', bgc=self.color['bg'], h=5)
        cmds.rowColumnLayout(numberOfColumns=5, w=self.win_width)
        cmds.text(l='', w=self.win_width * .15)
        cmds.button(l='capture', w=self.win_width * .17, bgc=self.color['bg'], c=lambda arg: self.toggle_capture_window())
        cmds.text(l='', w=self.win_width *.03)
        self.element['anim_export_bt'] = cmds.button(l='Export', w=self.win_width * .5, bgc=self.color['highlight'])
        cmds.text(l='', w=self.win_width * .15)
        cmds.setParent('..')
        cmds.text(l='', al='center', fn='boldLabelFont', bgc=self.color['bg'], h=5)

        if __name__ == '__main__':
            cmds.text(l='', al='center', fn='boldLabelFont', bgc=self.color['shadow'], h=5)
            cmds.text(l='(c) dex3d.gumroad.com', al='center', fn='smallPlainLabelFont', bgc=self.color['bg'], h=15)
        cmds.setParent('..')

    def show_win(self):
        cmds.showWindow(self.win_id)

    def init_dock(self):
        if cmds.dockControl(self.dock_id, q=1, ex=1):
            cmds.deleteUI(self.dock_id)
        cmds.dockControl(self.dock_id, area='bottom', fl=1, content=self.win_id, allowedArea=['all'],
                         sizeable=0, width=self.win_width, label=self.win_title)

    def show_ui(self):
        self.init_anim_proc_cmds()
        self.init_anim_export_cmds()
        self.init_config()
        self.init_win()
        self.win_layout()
        self.show_win()
        self.init_dock()
        self.update_ui()

    def update_ui(self):
        # config
        self.init_config()

        # anim export button
        expt_typ = cmds.optionMenu(self.element['export_to_option'], q=1, v=1)
        expt_cmd = [i for i in self.ae_reg_ls if i['name'] == expt_typ][0]['cmd']
        cmds.button(self.element['anim_export_bt'], e=1, l='{} Export'.format(expt_typ), c=expt_cmd)

    def reset_ui(self):
        self.func = quickMocap_func()
        cmds.text(self.element['namespace_tf'], e=1, l='')
        cmds.text(self.element['mocap_file_tf'], e=1, l='')
        cmds.intField(self.element['bake_frame_in'], e=1, v=0, ed=0)
        cmds.intField(self.element['bake_frame_out'], e=1, v=0, ed=0)
        self.init_anim_proc_cmds()
        self.init_anim_export_cmds()
        for i in self.aap_reg_ls:
            cmds.checkBox(self.element[i['cb_name']],e=1 , v=0)
        cmds.button(self.element['bake_anim_bt'], e=1, l='Bake Animation', c=lambda arg: self.bake_anim())

    # ---------------- Cmds -----------------------
    def import_rtg_file(self):
        self.reset_ui()
        rtg = self.func.get_import_rtg(self.cfg['rtg_dir'])
        if rtg == None:
            return None
        cmds.text(self.element['namespace_tf'],e=1 , l=rtg['namespace'])
        print(json.dumps(rtg['profile'], indent=4))

        self.cfg['rtg_dir'] = rtg['last_dir']
        self.save_config()

    def import_fbx_file(self):
        ns = cmds.text(self.element['namespace_tf'],q=1 , l=1)
        if ns == '':
            return None
        mocap = self.func.get_import_mocap_fbx(self.cfg['mocap_dir'])
        if mocap == None:
            return None
        cmds.text(self.element['mocap_file_tf'], e=1, l=os.path.basename(mocap['fbx_path']))
        self.set_frame_in_out(fio=[mocap['frame_start'], mocap['frame_end']])

        self.cfg['mocap_dir'] = mocap['last_dir']
        self.save_config()

    def set_frame_in_out(self, fio=[0.0,1.0]):
        cmds.intField(self.element['bake_frame_in'], e=1, ed=1, v=fio[0])
        cmds.intField(self.element['bake_frame_out'], e=1, ed=1, v=fio[1])

    def bake_anim(self):
        f_st = cmds.intField(self.element['bake_frame_in'], q=1, v=1)
        f_en = cmds.intField(self.element['bake_frame_out'], q=1, v=1)
        cmds.playbackOptions(e=1, ast=f_st,aet=f_en, min=f_st, max=f_en)
        self.func.bake_anim_rtg(f_st, f_en)
        self.func.delete_rtg_skeleton()
        self.run_anim_processing()
        cmds.button(self.element['bake_anim_bt'], e=1, l='Done', c='')

    def export_anim(self):
        min_time = cmds.playbackOptions(q=1, minTime=1)
        max_time = cmds.playbackOptions(q=1, maxTime=1)

    # ---------------- Anim Proc Cmds -----------------------
    def init_anim_proc_cmds(self):
        self.reload_aap()
        self.aap_reg_ls = [
            {
                'name': 'Time Scale',
                'cb_name': 'timescale_cb',
                'cmd': self.time_scale,
                'op_name': 'timescale_op',
                'op_value': 1.0
            },
            {
                'name' : 'Smooth Animation',
                'cb_name' : 'smooth_a_curve_cb',
                'cmd' : self.smooth_mocap,
                'op_name' : 'smooth_a_curve_op',
                'op_value' : 3
            },
            {
                'name' : 'Locomotion',
                'cb_name' : 'locomotion_cb',
                'cmd' : self.locomotion,
                'op_name' : None,
                'op_value' : 1.0
            },

        ]

    def reload_aap(self):
        imp.reload(animproc)
        self.aap = animproc.autoAnimProcessor

    def run_anim_processing(self):
        for i in self.aap_reg_ls:
             if cmds.checkBox(self.element[i['cb_name']], q=1, v=1):
                 i['cmd']()

    def smooth_mocap(self):
        self.reload_aap()
        sm_strength = cmds.floatField(self.element['smooth_a_curve_op'], q=1, v=1)
        ctrl_ls = self.func.get_rtg_ctrl()
        self.aap.smooth_anim(ctrl_ls, strength=sm_strength)

    def locomotion(self):
        self.reload_aap()
        ctrl_ls = self.func.get_rtg_ctrl()
        pf = self.func.rtg_profile
        placer = [i for i in ctrl_ls if pf['global'] in i][0]
        hips = [i for i in ctrl_ls if pf['hips'] in i][0]
        foot_r = [i for i in ctrl_ls if pf['foot_ik_rg'] in i][0]
        foot_l = [i for i in ctrl_ls if pf['foot_ik_lf'] in i][0]
        head = [i for i in ctrl_ls if pf['head'] in i][0]
        hand_l = [i for i in ctrl_ls if pf['hand_ik_lf'] in i][0]
        hand_r = [i for i in ctrl_ls if pf['hand_ik_rg'] in i][0]
        hand_r = [i for i in ctrl_ls if pf['arm_lf'] in i][0]
        hand_r = [i for i in ctrl_ls if pf['arm_rg'] in i][0]
        leg_pv_l = [i for i in ctrl_ls if pf['foot_ik_pole_lf'] in i][0]
        leg_pv_r = [i for i in ctrl_ls if pf['foot_ik_pole_rg'] in i][0]
        arm_pv_l = [i for i in ctrl_ls if pf['hand_ik_pole_lf'] in i][0]
        arm_pv_r = [i for i in ctrl_ls if pf['hand_ik_pole_rg'] in i][0]
        extra_ls = [hand_l, hand_r, leg_pv_l, leg_pv_r, arm_pv_l, arm_pv_r]
        self.aap.to_locomotion(placer, hips, foot_l, foot_r, head, extra_ls=extra_ls)
        self.func.clear_static_anim()

    def time_scale(self):
        self.reload_aap()
        scale = cmds.floatField(self.element['timescale_op'], q=1, v=1)
        frame_pv = cmds.intField(self.element['bake_frame_in'], q=1, v=1)
        ctrl_ls = self.func.get_rtg_ctrl()
        #print(scale, frame_pv, ctrl_ls)
        self.aap.time_scale(ctrl_ls, frame_pv=frame_pv, factor=scale)

    # ---------------- Anim Export Cmds -----------------------
    def init_anim_export_cmds(self):
        self.reload_ae()
        self.ae_reg_ls = [
            {
                'name': 'Studio Library',
                'cmd': self.export_studio_library
            },
        ]
        self.vpct = animexport.viewport_capture([], tc=[0.0,1.0])
        self.vpct.delete_capture_view()

    def reload_ae(self):
        imp.reload(animexport)
        self.ae = animexport.animExporter()

    def toggle_capture_window(self):
        self.reload_ae()

        ctrl_ls = self.func.get_rtg_ctrl()
        pf = self.func.rtg_profile
        hips = [i for i in ctrl_ls if pf['hips'] in i][0]
        head = [i for i in ctrl_ls if pf['head'] in i][0]
        foot_r = [i for i in ctrl_ls if pf['foot_ik_rg'] in i][0]
        foot_l = [i for i in ctrl_ls if pf['foot_ik_lf'] in i][0]
        obj_ls = [hips, head, foot_r, foot_l]
        tc = cmds.keyframe(obj_ls, q=1, tc=1)

        self.vpct = animexport.viewport_capture(obj_ls, tc=tc)
        if self.vpct.is_view_capture_exist():
            self.vpct.delete_capture_view()
        else:
            self.vpct.create_capture_view()

    def export_studio_library(self, a):
        self.reload_ae()

        ctrl_ls = self.func.get_rtg_ctrl()

        if self.vpct == None:
            raise Warning('need to create viewport captured')
        if not self.vpct.is_view_capture_exist():
            raise Warning('need to create viewport captured')

        result = cmds.fileDialog(mode=1, dm=self.cfg['anim_export_dir'] + os.sep + '*.anim')
        result = str(result)
        if result != '':
            print(result)
            self.ae.to_studio_library(ctrl_ls, result, vpct=self.vpct)
            self.vpct.delete_capture_view()

            self.cfg['anim_export_dir'] = os.path.dirname(result)
            self.save_config()

if __name__ == '__main__':
    qm = quickMocap_gui()