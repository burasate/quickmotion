# -*- coding: utf-8 -*-
# Skeleton Control Matcher
# (c) Burased Uttha (DEX3D).
# =================================
# Only use in $usr_orig$ machine
# =================================

import maya.cmds as cmds
from maya import mel
import time, os, sys, json
from functools import partial

if __name__ == '__main__':
    base_dir = None
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

class RTGMatcher_func:
    def __init__(self):
        self.skel_src_dir = base_dir + os.sep + 'skeleton'
        self.skel_src_path_ls = [base_dir + os.sep + 'skeleton' + os.sep + i
                                 for i in os.listdir(self.skel_src_dir) if i.endswith('.ma')]
        self.data = [
            {'name' : 'global', 'relative_ls' : [], 'grp_pr' : 'ground', 'con_type' : 'parent'},
            {'name' : 'hips', 'relative_ls' : [], 'grp_pr' : 'torso', 'con_type' : 'parent'},
            {'name' : 'spine1', 'relative_ls' : [], 'grp_pr' : 'torso', 'con_type' : 'oreint'},
            {'name' : 'spine2', 'relative_ls' : [], 'grp_pr' : 'torso', 'con_type' : 'oreint'},
            {'name' : 'spine3', 'relative_ls' : [], 'grp_pr' : 'torso', 'con_type' : 'oreint'},
            {'name' : 'spine4', 'relative_ls' : [], 'grp_pr' : 'torso', 'con_type' : 'oreint'},
            {'name' : 'neck', 'relative_ls' : [], 'grp_pr' : 'head', 'con_type' : 'oreint'},
            {'name' : 'head', 'relative_ls' : [], 'grp_pr' : 'head', 'con_type' : 'oreint'},
            {'name' : 'thigh_lf', 'relative_ls' : [], 'grp_pr' : 'leg', 'con_type' : 'oreint'},
            {'name' : 'knee_lf', 'relative_ls' : [], 'grp_pr' : 'leg', 'con_type' : 'oreint'},
            {'name' : 'foot_fk_lf', 'relative_ls' : [], 'grp_pr' : 'foot', 'con_type' : 'oreint'},
            {'name' : 'foot_ik_lf', 'relative_ls' : [], 'grp_pr' : 'foot', 'con_type' : 'parent'},
            {'name' : 'foot_ik_pole_lf', 'relative_ls' : ['lf_pv_foot']*len(self.skel_src_path_ls), 'grp_pr' : 'foot', 'con_type' : 'parent'},
            {'name' : 'toe_lf', 'relative_ls' : [], 'grp_pr' : 'foot', 'con_type' : 'oreint'},
            {'name' : 'thigh_rg', 'relative_ls' : [], 'grp_pr' : 'leg', 'con_type' : 'oreint'},
            {'name' : 'knee_rg', 'relative_ls' : [], 'grp_pr' : 'leg', 'con_type' : 'oreint'},
            {'name' : 'foot_fk_rg', 'relative_ls' : [], 'grp_pr' : 'foot', 'con_type' : 'oreint'},
            {'name' : 'foot_ik_rg', 'relative_ls' : [], 'grp_pr' : 'foot', 'con_type' : 'parent'},
            {'name' : 'foot_ik_pole_rg', 'relative_ls' : ['rg_pv_foot']*len(self.skel_src_path_ls), 'grp_pr' : 'foot', 'con_type' : 'parent'},
            {'name' : 'toe_rg', 'relative_ls' : [], 'grp_pr' : 'foot', 'con_type' : 'oreint'},
            {'name' : 'shoulder_lf', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'oreint'},
            {'name' : 'arm_lf', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'oreint'},
            {'name' : 'forearm_lf', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'oreint'},
            {'name' : 'hand_fk_lf', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'oreint'},
            {'name' : 'hand_ik_lf', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'parent'},
            {'name' : 'hand_ik_pole_lf', 'relative_ls' : ['lf_pv_hand']*len(self.skel_src_path_ls), 'grp_pr' : 'arm', 'con_type' : 'parent'},
            {'name' : 'shoulder_rg', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'oreint'},
            {'name' : 'arm_rg', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'oreint'},
            {'name' : 'forearm_rg', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'oreint'},
            {'name' : 'hand_fk_rg', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'oreint'},
            {'name' : 'hand_ik_rg', 'relative_ls' : [], 'grp_pr' : 'arm', 'con_type' : 'parent'},
            {'name' : 'hand_ik_pole_rg', 'relative_ls' : ['rg_pv_hand']*len(self.skel_src_path_ls), 'grp_pr' : 'arm', 'con_type' : 'parent'},
            {'name' : 'hand_thumb1_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_thumb2_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_thumb3_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_index1_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_index2_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_index3_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_middle1_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_middle2_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_middle3_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_ring1_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_ring2_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_ring3_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_pinky1_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_pinky2_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_pinky3_lf', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_thumb1_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_thumb2_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_thumb3_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_index1_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_index2_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_index3_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_middle1_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_middle2_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_middle3_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_ring1_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_ring2_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_ring3_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_pinky1_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_pinky2_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'},
            {'name' : 'hand_pinky3_rg', 'relative_ls' : [], 'grp_pr' : 'hand', 'con_type' : 'oreint'}
        ]
        # clear relative list
        for i in range(len(self.data)):
            self.data[i]['relative_ls'] = []
        #Load skeleton json
        for j_path in [i.replace('.ma', '.json') for i in self.skel_src_path_ls]:
            with open(j_path) as f:
                skel_rec = json.load(f)
            # append skel name data
            for i in range(len(self.data)):
                self.data[i]['relative_ls'].append(skel_rec[i]['relative_name'])

    def init(self, skel_ns, rig_ns, ctrl_data):
        cmds.currentTime(0.0, e=1)
        cmds.namespace(set=':')
        self.skel_ns = skel_ns
        self.rig_ns = rig_ns
        self.ctrl_data = ctrl_data
        self.base_idx = self.get_base_index(self.skel_ns)
        self.skel_sub_ns = None

    @staticmethod
    def new_scene():
        result = cmds.confirmDialog(message='New Scene without Save?',
                                    button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if result == 'Yes':
            cmds.file(newFile=1, force=1, prompt=1)
        else:
            raise Warning('Cancel')

    @staticmethod
    def sort_by_hierarchy_level(obj_ls):
        zip_obj_children = []
        for i in obj_ls:
            relative_count = cmds.listRelatives(i, allDescendents=1)
            if relative_count == None:
                relative_count = 0
            else:
                relative_count = len(relative_count)
            zip_obj_children.append([relative_count * -1, i])
        zip_obj_children = sorted(zip_obj_children)
        min_hier_level = abs(min([i[0] for i in zip_obj_children]))
        zip_obj_children = [ [zip_obj_children[i][0] + min_hier_level, zip_obj_children[i][1]]
                            for i in range(len(zip_obj_children)) ]
        sorted_obj_ls = [zip_obj_children[i][1] for i in range(len(zip_obj_children))]
        return sorted_obj_ls

    @staticmethod
    def define_t_pose_skeleton(*_):
        root_sel = cmds.ls(type=['joint', 'transform'], sl=1)[0]
        all_joint = [root_sel] + [i for i in cmds.listRelatives(root_sel, c=1, ad=1, s=0)]
        all_joint = [i for i in all_joint if cmds.objectType(i) in ['transform', 'joint']]
        all_joint = RTGMatcher_func.sort_by_hierarchy_level(all_joint)
        print(all_joint)
        confirm_msg = '''
Select Global : {}
Total Skeleton Object Count : {}

Skeleton Name :
'''.format(all_joint[0], len(all_joint))
        result = cmds.promptDialog(
            title='Define New T Pose Skeleton',
            message=confirm_msg,
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
        if result == 'OK':
            name = cmds.promptDialog(q=1, tx=1)
            ma_name = name.lower() + '_skeleton.ma'
            j_name = ma_name.replace('.ma', '.json')
            print(ma_name, j_name)

    def create_pole_vector_joint(self):
        data = [i for i in self.data if '_pole_' in i['name']]
        pole_parent_dict = {
            'foot_ik_pole_lf': self.get_joint_by_name('knee_lf'),
            'foot_ik_pole_rg': self.get_joint_by_name('knee_rg'),
            'hand_ik_pole_lf': self.get_joint_by_name('forearm_lf'),
            'hand_ik_pole_rg': self.get_joint_by_name('forearm_rg')
        }
        for i in data:
            cmds.joint(n=self.get_joint_by_name(i['name']))
            cmds.parent(self.get_joint_by_name(i['name']), pole_parent_dict[i['name']], r=1)

    def optimize_scene(self):
        cmds.optionVar(intValue=("displayerLayerOption", 1))
        os.environ["MAYA_TESTING_CLEANUP"] = "1"
        mel.eval("cleanUpScene(1)")
        del os.environ["MAYA_TESTING_CLEANUP"]

    def get_base_index(self, base_name):
        skel_ls = [os.path.basename(i).split('.')[0] for i in self.skel_src_path_ls]
        return skel_ls.index(base_name)

    def get_joint_by_name(self, name):
        return self.skel_ns + ':' + [i for i in self.data if i['name'] == name][0]['relative_ls'][self.base_idx]

    def get_ctrl_by_name(self, name):
        return self.rig_ns + ':' + self.ctrl_data[name]

    def get_ns_obj_selection(self):
        sel = cmds.ls(sl=1)[0]
        ns, obj = (None, None)
        if ':' in sel:
            ns = sel.split(':')[0]
            obj = sel.split(':')[1]
        else:
            obj = sel
        return (ns,obj)

    def get_loc_pos(self, obj):
        loc = cmds.spaceLocator(n=obj + 'pos_loc')[0]
        cmds.parentConstraint(obj, loc)
        pos = cmds.xform(loc, q=1 ,t=1 ,ws=1)
        cmds.delete(loc)
        return pos

    def load_skeleton(self):
        skel_path = self.skel_src_path_ls[self.base_idx]
        #skel_ns = os.path.basename(skel_path).split('.')[0]
        cmds.file(
            skel_path,
            r=1, type="mayaAscii",
            ignoreVersion=1,
            mergeNamespacesOnClash=0, options='v=0;',
            namespace=self.skel_ns,
            preserveReferences=1
        )

        # reference to Import
        r_file = cmds.referenceQuery(
            cmds.ls(self.skel_ns + '*')[0], f=1)
        cmds.file(r_file, importReference=1)

        # sub namespace
        self.skel_sub_ns = cmds.namespaceInfo(self.skel_ns, lon=1)
        if self.skel_sub_ns != None:
            for ns in self.skel_sub_ns:
                cmds.namespace(rm=':' + ns, mnp=1)
            print('get sub namespace{}'.format(self.skel_sub_ns))
            self.skel_sub_ns = self.skel_sub_ns[0].split(':')[-1]

        # pole vector
        self.create_pole_vector_joint()

    def lock_skeleton_attribute(self):
        lock_attr = ['tx', 'ty', 'tz', 'sx', 'sy', 'sz']
        joint_ls = cmds.listRelatives(self.get_joint_by_name('global'), ad=True, type='joint')
        joint_filter = [i for i in joint_ls if not i in [self.get_joint_by_name('hips')]]
        for a in lock_attr:
            for j in joint_filter:
                cmds.setAttr('{}.{}'.format(j, a), lock=1)

    def match_skeleton_to_controller(self):
        # scale group
        scale_grp = self.skel_ns + ':' + 'global_scale_grp'
        j_root = self.get_joint_by_name('global')
        if not cmds.objExists(scale_grp):
            cmds.group(n=scale_grp, em=1)
            cmds.parent(j_root, scale_grp)

        # ankle heigh
        j_feet_y_pos = [
            self.get_loc_pos(self.get_joint_by_name('foot_fk_lf'))[1],
            self.get_loc_pos(self.get_joint_by_name('foot_fk_rg'))[1]
        ]
        #print(j_feet_y_pos)
        j_feet_y_pos = sum(j_feet_y_pos) / len(j_feet_y_pos)
        c_feet_y_pos = [
            self.get_loc_pos(self.get_ctrl_by_name('foot_fk_lf'))[1],
            self.get_loc_pos(self.get_ctrl_by_name('foot_fk_lf'))[1]
        ]
        #print(c_feet_y_pos)
        c_feet_y_pos = sum(c_feet_y_pos) / len(c_feet_y_pos)
        cmds.setAttr(scale_grp + '.ty', c_feet_y_pos - j_feet_y_pos)
        #print(c_feet_y_pos, j_feet_y_pos, c_feet_y_pos - j_feet_y_pos)

        # scale to all
        cmds.move(0, c_feet_y_pos, scale_grp + '.scalePivot', scale_grp + '.rotatePivot', ws=1)
        c_feet_y_pos = [
            self.get_loc_pos(self.get_ctrl_by_name('foot_fk_lf'))[1],
            self.get_loc_pos(self.get_ctrl_by_name('foot_fk_lf'))[1]
        ]
        c_feet_y_pos = sum(c_feet_y_pos) / len(c_feet_y_pos)
        j_hips_pos = self.get_loc_pos(self.get_joint_by_name('hips'))
        c_hips_pos = self.get_loc_pos(self.get_ctrl_by_name('hips'))
        pos_ratio = (c_hips_pos[1] - c_feet_y_pos) / (j_hips_pos[1] - c_feet_y_pos)
        cmds.setAttr(scale_grp + '.sx', pos_ratio)
        cmds.setAttr(scale_grp + '.sy', pos_ratio)
        cmds.setAttr(scale_grp + '.sz', pos_ratio)

        # hips
        j_hips_pos = self.get_loc_pos(self.get_joint_by_name('hips'))
        c_hips_pos = self.get_loc_pos(self.get_ctrl_by_name('hips'))
        cmds.move(c_hips_pos[0], c_hips_pos[1], c_hips_pos[2], self.get_joint_by_name('hips'), a=1, ws=1)

        # ankle
        c_foot_lf_pos = self.get_loc_pos(self.get_ctrl_by_name('foot_fk_lf'))
        c_foot_rg_pos = self.get_loc_pos(self.get_ctrl_by_name('foot_fk_rg'))
        cmds.move(c_foot_lf_pos[0], j_hips_pos[1], c_foot_lf_pos[2], self.get_joint_by_name('thigh_lf'), a=1, ws=1)
        cmds.move(c_foot_rg_pos[0], j_hips_pos[1], c_foot_rg_pos[2], self.get_joint_by_name('thigh_rg'), a=1, ws=1)

        # align all upper
        all_upper_ls = [i['name'] for i in self.data
                        if not i['name'] in ['global', 'hips', 'thigh_lf', 'knee_lf']]

        c_data_ls = [i for i in self.ctrl_data]
        for i in self.data:
            if not i['name'] in c_data_ls:
                continue
            if not cmds.objExists(self.get_joint_by_name(i['name'])):
                continue
            if i['grp_pr'] in ['torso', 'head', 'arm', 'hand', 'foot']:
                c_i_pos = self.get_loc_pos(self.get_ctrl_by_name(i['name']))
                cmds.move(c_i_pos[0], c_i_pos[1], c_i_pos[2], self.get_joint_by_name(i['name']), a=1, ws=1)

    def retarget_constrain(self):
        translate_at = {'translateX': 'x', 'translateY': 'y', 'translateZ': 'z'}
        rotate_at = {'rotateX': 'x', 'rotateY': 'y', 'rotateZ': 'z'}

        c_data_ls = [i for i in self.ctrl_data]
        for i in self.data:
            if not i['name'] in c_data_ls:
                continue

            joint = self.get_joint_by_name(i['name'])
            ctrl = self.get_ctrl_by_name(i['name'])
            con_type = i['con_type']

            if not cmds.objExists(joint):
                continue

            t_at = [a for a in cmds.listAttr(ctrl, k=1) if a in list(translate_at)]
            r_at = [a for a in cmds.listAttr(ctrl, k=1) if a in list(rotate_at)]
            skip_t_at = [translate_at[a] for a in list(translate_at) if not a in t_at]
            skip_r_at = [rotate_at[a] for a in list(rotate_at) if not a in r_at]
            #print('skip attribute', skip_t_at, skip_r_at)

            cmds.setKeyframe(ctrl, at=t_at + r_at)
            if con_type == 'parent':
                cmds.parentConstraint(joint, ctrl, mo=1, weight=1, skipTranslate=skip_t_at, skipRotate=skip_r_at)
            elif con_type == 'point':
                cmds.pointConstraint(joint, ctrl, mo=1, weight=1, skip=skip_t_at)
            elif con_type == 'oreint':
                cmds.orientConstraint(joint, ctrl, mo=1, weight=1, skip=skip_r_at)

    def retarget_finishing(self):
        cmds.namespace(set=':')
        # clear keyframe
        #all_joint = cmds.listRelatives(self.get_joint_by_name('global'), c=1, ad=1) + [self.get_joint_by_name('global')]
        #cmds.cutKey(all_joint, cl=1)

        # clear unknown
        cmds.delete(cmds.ls(type=['unknown', 'unknownDag', 'unknownTransform']))
        self.optimize_scene()

        # lock joint
        self.lock_skeleton_attribute()

        # remove namespace
        if self.skel_sub_ns == None:
            cmds.namespace(rm=':' + self.skel_ns, mnr=1)
        else:
            cmds.namespace(add=self.skel_sub_ns)
            cmds.namespace(mv=(self.skel_ns, self.skel_sub_ns))
            cmds.namespace(rm=self.skel_ns)

class RTGMatcher_gui:
    def __init__(self):
        self.version = 0.01
        self.win_id = 'BRS_SKELMATCH'
        self.dock_id = self.win_id + '_DOCK'
        self.win_width = 300
        self.win_title = 'RTG Skeleton Matcher  -  v.{}'.format(self.version)
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
            self.func = RTGMatcher_func()

    def init_config(self):
        data = {
            'profile_dir' : base_dir + os.sep + 'profiles',
            'base_skel_dir' : base_dir + os.sep + 'skeleton',
            'export_rtg_dir' : base_dir + os.sep + 'export_rtg',
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

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)
        cmds.text(l=' CHARACTER RIG', fn='smallPlainLabelFont', al='left', w=self.win_width,
                  bgc=self.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)

        cmds.rowColumnLayout(numberOfColumns=3, w=self.win_width)
        cmds.text(l='', w=self.win_width * .2)
        cmds.button(l='Reference Rig', w=self.win_width * .6, bgc=self.color['highlight'], c=lambda arg: self.load_reference())
        cmds.text(l='', w=self.win_width * .2)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)
        cmds.text(l=' RTG SETUP OPTION', fn='smallPlainLabelFont', al='left', w=self.win_width,
                  bgc=self.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)

        self.element['skel_base_menu'] = cmds.optionMenu(label=' Base Skeleton :', w=self.win_width, bgc=self.color['highlight'])
        for item in self.func.skel_src_path_ls:
            cmds.menuItem(label=os.path.basename(item))
        #cmds.optionMenu(self.element['skel_base_menu'], e=1, v='rokoko_skeleton.ma')

        self.element['profile_column'] = cmds.columnLayout(adj=1, w=self.win_width)
        self.element['profile_menu'] = cmds.optionMenu(label=' Profile :', w=self.win_width, bgc=self.color['highlight'])
        cmds.menuItem(label='')
        cmds.setParent('..')

        cmds.rowColumnLayout(numberOfColumns=3, w=self.win_width)
        cmds.button(l='Load', w=self.win_width * .98 / 3, bgc=self.color['highlight'], c=lambda arg: self.load_profile(), h=17)
        cmds.button(l='Save', w=self.win_width * .98 / 3, bgc=self.color['highlight'], c=lambda arg: self.save_profile(), h=17)
        cmds.button(l='Delete', w=self.win_width * .98 / 3, bgc=self.color['highlight'], c=lambda arg: self.del_profile(), h=17)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)
        cmds.text(l=' SKELETON - CONTROLLER', fn='smallPlainLabelFont', al='left', w=self.win_width,
                  bgc=self.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)

        scrollLayout = cmds.scrollLayout(
            h=175, w=self.win_width,
            horizontalScrollBarThickness=16,
            verticalScrollBarThickness=16)
        cmds.rowColumnLayout(numberOfColumns=5)
        cmds.text(al='center', l='ID ', fn='boldLabelFont', bgc=self.color['bg'], h=30)
        cmds.text(al='center', l='Joint', fn='boldLabelFont', bgc=self.color['bg'], h=30)
        cmds.text(al='center', l='', fn='boldLabelFont', bgc=self.color['bg'], h=30)
        cmds.text(al='center', l='Ctrl', fn='boldLabelFont', bgc=self.color['bg'], h=30)
        cmds.text(al='center', l='x', fn='boldLabelFont', bgc=self.color['bg'], h=30)
        for i in self.func.data:
            cap_name = ' '.join([l.replace('lf','L').replace('rg','R').capitalize()
                                 for l in i['name'].split('_')]) + ' :' + ' '*3
            bt = i['name'] + '_bt' #button
            tf = i['name'] + '_tf' #text
            st = i['name'] + '_st' #status
            add_cmd = partial(self.load_text_object, tf)
            remove_cmd = partial(self.clear_text_object, tf)
            cmds.text(al='center', l='{:02d}   '.format(self.func.data.index(i)))
            cmds.text(al='right', l=cap_name)
            self.element[bt] = cmds.button(l='>', w=self.win_width * .08)
            self.element[tf] = cmds.textField(ed=0, w=self.win_width*0.4)
            self.element[st] = cmds.button(w=self.win_width*0.03, bgc=self.color['highlight'], l='')
            cmds.button(self.element[bt], e=1, c=add_cmd)
            cmds.button(self.element[st], e=1, c=remove_cmd)
        cmds.setParent('..') #row column
        cmds.setParent('..') #scroll

        cmds.rowLayout(numberOfColumns=3, columnWidth3=(self.win_width * .3, self.win_width * .6, self.win_width * .1),adj=2)
        cmds.text(al='right', l=' Rig Namspace :')
        self.element['rig_ns'] = cmds.textField(w=self.win_width * .6, ed=0, tx='')
        cmds.button(l='>', w=self.win_width * .08, c=lambda arg: self.get_rig_ns())
        cmds.setParent('..')

        cmds.rowColumnLayout(numberOfColumns=3, w=self.win_width)
        cmds.text(l='', w=self.win_width*.2)
        cmds.button(l='Match Skeleton to Rig', w=self.win_width*.6, bgc=self.color['highlight'],
                    c=lambda arg: self.do_match_skeleton())
        cmds.text(l='', w=self.win_width*.2)
        cmds.setParent('..')

        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)
        cmds.text(l=' EXPORT', fn='smallPlainLabelFont', al='left', w=self.win_width,
                  bgc=self.color['highlight'])
        cmds.text(l='', fn='smallPlainLabelFont', al='center', h=10, w=self.win_width)

        cmds.rowColumnLayout(numberOfColumns=3, w=self.win_width)
        cmds.text(l='', w=self.win_width * .2)
        cmds.button(l='Export RTG File', w=self.win_width * .6, bgc=self.color['highlight'],
                    c=lambda arg: self.export_rtg())
        cmds.text(l='', w=self.win_width * .2)
        cmds.setParent('..')

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
        self.init_config()
        self.init_win()
        self.win_layout()
        self.show_win()
        self.init_dock()
        self.update_ui()

    def update_ui(self):
        # config
        self.init_config()

        # connection list
        tf_ls = []
        st_ls = []
        obj_ls = []
        for i in self.func.data:
            tf = i['name'] + '_tf'
            tf_ls.append(tf)
            st = i['name'] + '_st'
            st_ls.append(st)
            obj_ls.append(cmds.textField(self.element[tf], q=1, tx=1))
        for i in range(len(tf_ls)):
            if obj_ls[i] == '':
                cmds.button(self.element[st_ls[i]], e=1, bgc=self.color['highlight'])
                continue
            if obj_ls.count(obj_ls[i]) > 1:
                cmds.button(self.element[st_ls[i]], e=1, bgc=self.color['red'])
            else:
                cmds.button(self.element[st_ls[i]], e=1, bgc=self.color['green'])

        #profile update
        current_profile = cmds.optionMenu(self.element['profile_menu'], q=True, v=True)
        cmds.deleteUI(self.element['profile_menu'])
        cmds.setParent(self.element['profile_column'])
        self.element['profile_menu'] = cmds.optionMenu(label=' Profile :', w=self.win_width, bgc=self.color['highlight'])
        profie_ls = [i.split('.')[0] for i in os.listdir(self.cfg['profile_dir'])]
        cmds.menuItem(label='')
        for i in profie_ls:
            cmds.menuItem(label=i)
        if not current_profile in [None,'']:
            cmds.optionMenu(self.element['profile_menu'], e=1, v=current_profile)

    def get_ctrl_data(self):
        data = {}
        for i in self.func.data:
            tf = i['name'] + '_tf'
            tx = cmds.textField(self.element[tf], q=1, tx=1)
            if tx != '':
                data[i['name']] = tx
        return data

    def load_profile(self):
        current_profile = cmds.optionMenu(self.element['profile_menu'], q=True, v=True)
        load_path = self.cfg['profile_dir'] + os.sep + '{}.json'.format(current_profile)
        data = json.load(open(load_path))
        for i in data:
            tf = i + '_tf'
            if not tf in self.element:
                continue
            tx = cmds.textField(self.element[tf], e=1, tx=data[i])
        self.update_ui()

    def save_profile(self):
        current_profile = cmds.optionMenu(self.element['profile_menu'], q=True, v=True)
        ctrl_data = self.get_ctrl_data()
        result = cmds.promptDialog(tx = current_profile,
            message='Profile Name:',
            button=['Save', 'Cancel'],
            defaultButton='Save',
            cancelButton='Cancel',
            dismissString='Cancel')
        if result == 'Save':
            name = cmds.promptDialog(q=1, tx=1)
            save_path = self.cfg['profile_dir'] + os.sep + '{}.json'.format(name)
            with open(save_path, 'w') as f:
                json.dump(ctrl_data, f, indent=4)
                f.close()
            self.update_ui()
        cmds.optionMenu(self.element['profile_menu'], e=1, v=name)


    def del_profile(self):
        current_profile = cmds.optionMenu(self.element['profile_menu'], q=True, v=True)
        result = cmds.confirmDialog(title='Delete', message='Delete current profile?', button=['Yes','No'],
                                     defaultButton='Yes', cancelButton='No', dismissString='No')
        if result == 'Yes':
            cmds.optionMenu(self.element['profile_menu'], e=1, v='')
            del_path = self.cfg['profile_dir'] + os.sep + '{}.json'.format(current_profile)
            os.remove(del_path)
        self.update_ui()

    def load_text_object(self, tf_k, n=1):
        name_no_ns = self.func.get_ns_obj_selection()[-1]
        cmds.textField(self.element[tf_k], e=1, tx=name_no_ns)
        self.get_rig_ns()
        self.update_ui()

    def clear_text_object(self, tf_k, n=1):
        cmds.textField(self.element[tf_k], e=1, tx='')
        self.update_ui()

    def export_rtg(self):
        skel_ns = cmds.optionMenu(self.element['skel_base_menu'], q=1, v=1)
        skel_ns = skel_ns.split('.')[0]
        rig_ns = cmds.textField(self.element['rig_ns'], q=1, tx=1)

        sel = [i for i in cmds.ls(type='transform') if rig_ns in i]
        cmds.select(sel)
        skel_sym = skel_ns.split('_')[0][:3]
        file_name = cmds.referenceQuery(sel[0], f=1, shn=1).replace('.mb','.ma')
        ma_path = self.cfg['export_rtg_dir'] + os.sep + file_name.replace('.ma', '_rtg_{}.ma'.format(skel_sym))

        cmds.file(ma_path, es=1, pr=1, typ='mayaAscii', options='v=0;', force=1)
        print(ma_path)

        ctrl_data = self.get_ctrl_data()
        j_path = ma_path.replace('.ma', '.json')
        with open(j_path, 'w') as f:
            json.dump(ctrl_data, f, indent=4)
            f.close()
        print(j_path)

        cmds.confirmDialog(message='export {} finish'.format(os.path.basename(ma_path)), button=['OK'])
        cmds.select(cl=1)

    def get_rig_ns(self):
        cmds.textField(self.element['rig_ns'], e=1, tx=self.func.get_ns_obj_selection()[0])
        self.cfg['rig_ns_last'] = self.func.get_ns_obj_selection()[0]
        self.save_config()
        self.update_ui()

    def load_reference(self):
        RTGMatcher_func.new_scene()
        multiple_filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        result = cmds.fileDialog2(fileFilter=multiple_filters, dialogStyle=2, okc='Load Reference')
        result = result[0] if len(result) != 0 else ''
        if result != '':
            print(result)
            before_ref = cmds.ls(type='reference')
            cmds.file(
                result, r=1, ignoreVersion=1, gl=1,
                mergeNamespacesOnClash=0, options='v=0;',
                preserveReferences=1, namespace=os.path.basename(result).split('.')[0]
            )
            after_ref = [r for r in cmds.ls(type='reference') if not r in before_ref]
            ref_sel = after_ref[0]
            ref_ns = cmds.referenceQuery(ref_sel, namespace=1).replace(':', '')
            cmds.select(cmds.ls(ref_ns + ':*'))
            self.get_rig_ns()
            cmds.select(cl=1)

    def do_match_skeleton(self):
        '''
        1. referent to import skel
        2. match joint
        3. retarget (contraint)
        4. remove skel namspace
        5. clear keyframe
        6. clear unknown and optimize
        7. lock joint attr
        '''
        #skel_ns = cmds.textField(self.element['skel_ns'], q=1, tx=1)
        rig_ns = cmds.textField(self.element['rig_ns'], q=1, tx=1)
        if len(cmds.ls(rig_ns + ':*')) == 0:
            raise Warning('not found namespace {}'.format(rig_ns))
        skel_ns = cmds.optionMenu(self.element['skel_base_menu'], q=1, v=1)
        skel_ns = skel_ns.split('.')[0]
        ctrl_data = self.get_ctrl_data()
        #print(json.dumps(ctrl_data, indent=4))
        print(skel_ns, rig_ns)
        self.func.init(skel_ns, rig_ns, ctrl_data)
        self.func.load_skeleton()
        self.func.match_skeleton_to_controller()
        self.func.retarget_constrain()
        self.func.retarget_finishing()
        print('Match Skeleton s Done\n'),

if __name__ == '__main__':
    skm = RTGMatcher_gui()