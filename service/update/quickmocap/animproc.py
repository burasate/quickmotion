import maya.cmds as cmds
from maya import mel
import time, os, sys, json, traceback

class animlayer:
    def __init__(self):
        self.test = 'load test done'

class vc_transform:
    @staticmethod
    def smooth(vc,  epoc=3):
        for e in range(epoc):
            new_vc = []
            for i in range(1, len(vc) - 1):
                v_prev = vc[i - 1]
                v_cur = vc[i]
                v_next = vc[i + 1]
                v_avg = (v_prev + v_cur + v_next) / 3
                new_vc.append(v_avg)
            new_vc.insert(0, vc[0])
            new_vc.append(vc[-1])
            vc = new_vc
        return vc

class util:
    @staticmethod
    def get_fps(*_):
        timeUnitSet = {'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
        timeUnit = cmds.currentUnit(q=True, t=True)
        if timeUnit in timeUnitSet:
            return timeUnitSet[timeUnit]
        else:
            return float(str(''.join([i for i in timeUnit if i.isdigit() or i == '.'])))

    @staticmethod
    def get_anim_loc(obj):
        tc = cmds.keyframe(obj, q=1, tc=1)
        if tc == None:
            return None
        loc = cmds.spaceLocator(n=obj + '_anm_loc')[0]
        return loc

    @staticmethod
    def get_alt_parent_constraint(target, obj):
        con_ls = []
        r_at = ['rx', 'ry', 'rz']
        t_at = ['tx', 'ty', 'tz']
        attr_ls = [i for i in cmds.listAttr(obj, sn=1, iu=1, se=1, k=1)
                   if i in r_at + t_at]
        r_at_skip = [i[1] for i in r_at if not i in t_at and i not in attr_ls]
        t_at_skip = [i[1] for i in t_at if not i in r_at and i not in attr_ls]
        if len(t_at_skip) < 3:
            p_con = cmds.pointConstraint(target, obj, mo=0, skip=t_at_skip)[0]
            con_ls += [p_con]
        if len(r_at_skip) < 3:
            o_con = cmds.orientConstraint(target, obj, mo=0, skip=r_at_skip)[0]
            if r_at_skip == []:
                cmds.setAttr(o_con + '.interpType', 0)
            con_ls += [o_con]
        return con_ls

    @staticmethod
    def bake_anim(obj_ls, t=(0.0,0.0), at=['tx','ty','tz','rx','ry','rz']):
        try:
            cmds.refresh(su=1)
            cmds.bakeResults(obj_ls, simulation=1, sampleBy=1, disableImplicitControl=1, preserveOutsideKeys=1,
                             sparseAnimCurveBake=0, t=t, at=at)
            cmds.filterCurve(obj_ls)
        except:
            cmds.warning(str(traceback.format_exc()))
        finally:
            cmds.refresh(su=0)

class autoAnimProcessor:
    @staticmethod
    def smooth_anim(obj_ls, strength=3):
        keyframes = sorted([round(i, 0) for i in cmds.keyframe(obj_ls, q=1, tc=1)])

        # constraint locators
        loc_ls = []
        con_ls = []
        skip_ls = []
        for obj in obj_ls:
            loc = util.get_anim_loc(obj)
            if loc == None:
                skip_ls += [obj]
                continue
            loc_ls += [loc]
            con_ls += [cmds.parentConstraint(obj, loc, mo=0)[0]]
        obj_ls = [i for i in obj_ls if not i in skip_ls]
        util.bake_anim(loc_ls, t=(keyframes[0], keyframes[-1]))
        cmds.delete(con_ls)

        # smooth anim curves
        ac_ls = cmds.keyframe(loc_ls, q=1, n=1)
        for ac in ac_ls:
            #cmds.selectKey(ac, k=1)
            tc = cmds.keyframe(ac, q=1, tc=1)
            vc = cmds.keyframe(ac, q=1, vc=1)
            if min(vc) == max(vc):
                continue
            vc_sm = vc_transform.smooth( vc, epoc=int(round(strength,0)) )
            vc = [(vc_sm[i] + vc[i])*.5
                  for i in range(len(tc))]
            [cmds.keyframe(ac, e=1, t=(tc[i],), vc=vc[i])
             for i in range(len(tc))]

        # constraint and bake to guide loctors
        con_ls = []
        print(len(obj_ls),obj_ls) #62
        print(len(loc_ls),loc_ls) #61
        for obj in obj_ls:
            cmds.select(obj)
            loc = loc_ls[obj_ls.index(obj)]
            con_ls += util.get_alt_parent_constraint(loc, obj)
        util.bake_anim(obj_ls, t=(keyframes[0], keyframes[-1]))
        cmds.delete(con_ls + loc_ls)

        cmds.select(obj_ls)

    @staticmethod
    def to_locomotion(placer, hip, foot_l, foot_r, head, extra_ls=[]):
        # feet loc
        feet_loc = util.get_anim_loc(foot_l)
        cmds.pointConstraint([foot_r, foot_l], feet_loc, mo=0)[0]

        # center of gravity loc
        cog_loc = util.get_anim_loc(placer)
        cmds.setAttr(cog_loc+'.rotateOrder', 3)
        placer_pos = cmds.xform(placer, q=1 ,t=1 ,ws=1)
        cmds.move(placer_pos[0], placer_pos[1], placer_pos[2], cog_loc, a=1, ws=1)
        p_con = cmds.pointConstraint([hip, head, feet_loc],
                                     cog_loc, mo=0, skip=['y'])[0]
        o_con = cmds.orientConstraint(hip, cog_loc, mo=0)[0]
        cmds.setAttr(o_con+'.interpType', 0)
        keyframes = sorted([round(i, 0) for i in cmds.keyframe(hip, q=1, tc=1)])
        util.bake_anim(cog_loc, t=(keyframes[0], keyframes[-1]))
        cmds.delete([p_con, o_con])
        cmds.cutKey(cog_loc, at=['rx', 'rz'])
        cmds.setAttr(cog_loc+'.rx', 0.0)
        cmds.setAttr(cog_loc+'.rz', 0.0)

        # smooth locomotion cog
        ac_ls = cmds.keyframe(cog_loc, q=1, n=1)
        for ac in ac_ls:
            tc = cmds.keyframe(ac, q=1, tc=1)
            vc = cmds.keyframe(ac, q=1, vc=1)
            if min(vc) == max(vc):
                continue
            sm_lev = 3
            if 'Y' in ac:
                sm_lev = sm_lev * 5
            vc = vc_transform.smooth(vc, epoc=sm_lev)
            [cmds.keyframe(ac, e=1, t=(tc[i],), vc=vc[i])
             for i in range(len(tc))]

        # mimic locator
        loc_ls = []
        con_ls = []
        non_placer_ls = [hip, foot_r, foot_l, head] + extra_ls
        for obj in non_placer_ls:
            loc = util.get_anim_loc(obj)
            loc_ls += [loc]
            con_ls += [cmds.parentConstraint(obj, loc, mo=0)[0]]
        #con_ls += [cmds.parentConstraint(cog_loc, placer, mo=0)[0]]
        util.bake_anim(loc_ls, t=(keyframes[0], keyframes[-1]))
        cmds.delete(con_ls)

        # constraint lock
        con_ls = []
        for loc in loc_ls:
            obj = non_placer_ls[loc_ls.index(loc)]
            con_ls += util.get_alt_parent_constraint(loc, obj)
        con_ls += [cmds.parentConstraint(cog_loc, placer, mo=0)[0]]
        util.bake_anim([placer]+non_placer_ls, t=(keyframes[0], keyframes[-1]))
        cmds.delete(con_ls + loc_ls + [cog_loc, feet_loc])

        cmds.select([placer]+non_placer_ls)

    @staticmethod
    def time_scale(obj_ls, frame_pv=0, factor=1.00):
        if factor < 0.01:
            factor = 0.01
        ac_ls = cmds.keyframe(obj_ls, q=1, n=1)
        cmds.scaleKey(ac_ls, ts=factor, tp=frame_pv)

        #new keyframe
        tc_ls = list(set([round(i, 0) for i in cmds.keyframe(ac_ls, q=1, tc=1)]))
        cmds.playbackOptions(e=1, ast=min(tc_ls), aet=max(tc_ls), min=min(tc_ls), max=max(tc_ls))
        util.bake_anim(ac_ls, t=(tc[0], tc[-1]))
        tc_ls = list(set([round(i, 0) for i in cmds.keyframe(ac_ls, q=1, tc=1)]))
        [cmds.cutKey(ac_ls, t=(tc_ls[i],)) for i in range(len(tc_ls)) if round(tc_ls[i],0) != tc_ls[i]]


#al = animationLayer()
#print(al.test)

#print(util.get_anim_loc('NC11_woman:head_CTL'))