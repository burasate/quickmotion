import maya.cmds as cmds
from maya import mel
import time, os, sys, json, traceback, shutil, imp
import animproc
imp.reload(animproc)

class viewport_capture:
    '''
    # how to create view (separate function)
    vpct = viewport_capture(['sphere1'], 0.0, 10.0) # frame 0-10
    vpct.create_capture_view()

    # how to capture
    if vpct.is_view_capture_exist():
        vpct.img_seq_capture('thumbnail','C:/Users/kaofang.burased/Desktop/test')
        vpct.video_capture('C:/Users/kaofang.burased/Desktop/test/preview.mov',w=1080 ,h=1080)
        vpct.delete_capture_view()
    '''

    def __init__(self, obj_ls, tc=[0.0,1.0]):
        self.panel_id = 'CAPTUREPANEL'
        self.win_id = 'CAPTUREWINDOW'
        self.min_time, self.max_time = [tc[0], tc[-1]]
        self.obj_ls = obj_ls


    def clear(self):
        clear_ls = ['fitCam', 'fn_typeMesh', 'fn_typeMesh', 'fn_type', 'fn_shellDfm', 'fn_extrude', 'fn_remesh']
        for obj in clear_ls:
            if cmds.objExists(obj):
                try:cmds.delete(obj)
                except:pass

    def is_view_capture_exist(self):
        return cmds.modelPanel(self.panel_id, ex=1)

    def create_current_frame_text(self):
        mel.eval('CreatePolygonType')
        # Cleanup
        clear_ls = [i for i in ['transform1', 'polyAutoProj1', 'polySoftEdge1', 'vectorAdjust1', 'tweak1']
                    if cmds.objExists(i)]
        cmds.delete(clear_ls)
        # Rename
        cmds.rename('typeMesh1', 'fn_typeMesh')
        cmds.rename('type1', 'fn_type')
        cmds.rename('shellDeformer1', 'fn_shellDfm')
        cmds.rename('typeExtrude1', 'fn_extrude')
        cmds.rename('polyRemesh1', 'fn_remesh')
        cmds.rename('typeBlinn', 'fn_shd')
        # Set Attribute
        cmds.setAttr('fn_type.generator', 1)
        cmds.setAttr('fn_type.fontSize', 0.6)
        cmds.setAttr('fn_type.length', 5)
        cmds.setAttr('fn_extrude.enableExtrusion', 0)
        cmds.setAttr('fn_shd.specularRollOff', 0)
        cmds.setAttr('fn_shd.reflectivity', 0)
        cmds.setAttr('fn_shd.color', 1, 1, 1, type='double3')
        cmds.setAttr('fn_shd.incandescence', 1, 1, 1, type='double3')
        cmds.select(cl=1)

    def fit_camera(self):
        cam = cmds.camera()
        cmds.rename(cam[0], 'fitCam')
        cmds.camera(
            'fitCamShape', e=1,
            focalLength=60,
            overscan=1.3,
            nearClipPlane=5,
            aspectRatio=1.0,
            lensSqueezeRatio=1,
            filmFit='overscan'
        )
        cmds.select(cl=1)

    def fit_view_to_object(self):
        if self.obj_ls == []:
            return None
        cmds.select(self.obj_ls)
        print('fit camera to selection', self.obj_ls)
        timeRange = range(int(round(self.max_time - self.min_time)) + 1)
        timeRange = [i + self.min_time for i in timeRange]
        for f in timeRange:
            if f % 2 == 0 or f == self.min_time or f == self.max_time:
                cmds.currentTime(f)
                cmds.viewFit('fitCamShape', all=0, fitFactor=1)
                cmds.setKeyframe('fitCam', shape=0)
        # smooth
        ac_ls = cmds.keyframe('fitCam', q=1, n=1)
        for ac in ac_ls:
            tc = cmds.keyframe(ac, q=1, tc=1)
            vc = cmds.keyframe(ac, q=1, vc=1)
            vc = animproc.vc_transform.smooth(vc, epoc=5)
            [cmds.keyframe(ac, e=1, t=(tc[i],), vc=vc[i])
             for i in range(len(tc))]
        # camera lock
        cmds.camera('fitCamShape', e=1, lockTransform=1)

    def capture_panel(self, close=False):
        if cmds.window(self.win_id, exists=1):
            cmds.deleteUI(self.win_id)
        if cmds.modelPanel(self.panel_id, exists=1):
            cmds.deleteUI(self.panel_id, panel=1)
        if close:
            self.clear()
            return None
        cmds.window(self.win_id, retain=1, sizeable=0, title='Do Not Close')
        cmds.window(self.win_id, e=1, w=256, h=294, titleBar=0)
        cmds.frameLayout(lv=0)
        cmds.modelPanel(self.panel_id, l='CapturePanel')
        cmds.showWindow(self.win_id)

    def show_texture(self):
        cmds.modelEditor(self.panel_id, e=1, backfaceCulling=0, twoSidedLighting=1,
                         displayTextures=1, control=0, nurbsCurves=0, hud=0, locators=0,
                         av=1, manipulators=1)
        cmds.select(cl=1)
        mel.eval('createViewport20OptionsUI;')
        cmds.setAttr('hardwareRenderingGlobals.enableTextureMaxRes', 1)
        cmds.setAttr('hardwareRenderingGlobals.textureMaxResMode', 1)
        cmds.setAttr('hardwareRenderingGlobals.textureMaxResolution', 512)
        cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
        mel.eval('DisplayShadedAndTextured;')
        mel.eval('generateAllUvTilePreviews;')
        mel.eval('window -e -vis 0 Viewport20OptionsWindow;')

    def img_seq_capture(self, file_name, dir_path, skip=3):
        timeRange = range(int(round(self.max_time - self.min_time)) + 1)
        timeRange = [i + self.min_time for i in timeRange]
        for f in timeRange:
            if f % skip == 0 or f == self.min_time or f == self.max_time:
                cmds.currentTime(f)
                file_path = dir_path + '/{}.{:0>4}.jpg'.format(file_name, int(f))
                print('capture', f, file_path)
                cmds.modelEditor(self.panel_id, e=1, activeView=1)
                cmds.refresh(cv=1, fe='jpg', fn=file_path)

    def video_capture(self, file_path, w=540, h=540):
        cmds.modelEditor(self.panel_id, e=1, activeView=1)
        cmds.playblast(
            f=file_path,
            format='qt', sequenceTime=0, clearCache=0, viewer=1,
            showOrnaments=0, fp=4, percent=100, compression='H.264',
            quality=25, widthHeight=(w, h), st=self.min_time, et=self.max_time, forceOverwrite=1
        )

    def create_capture_view(self):
        if len(self.obj_ls) == 0:
            return None
        self.capture_panel(close=True)
        self.create_current_frame_text()
        self.fit_camera()
        cmds.parent('fn_typeMesh', 'fitCam')
        cmds.setAttr('fn_typeMesh.translate', -0.741, -1.938, -9, type='double3')
        cmds.setAttr('fitCam.rotate', -10, 45, 0, type='double3')
        self.capture_panel()
        self.fit_view_to_object()
        self.show_texture()

    def delete_capture_view(self):
        self.capture_panel(close=True)
        self.clear()

class studio_library:
    def __init__(self):
        maya_app_dir = os.path.abspath(mel.eval('getenv MAYA_APP_DIR'))
        script_dir = os.path.abspath(maya_app_dir + os.sep + 'scripts')
        dir_name = 'studiolibrary'
        sl_lsdir = [i for i in os.listdir(script_dir) if dir_name in i]
        if sl_lsdir != []:
            self.src_path = script_dir + os.sep + sl_lsdir[0] + os.sep + 'src'
            if not self.src_path in sys.path:
                sys.path.insert(0, self.src_path)
            import studiolibrary
            from studiolibrarymaya import animitem
            self.anim_item = animitem
        else:
            self.src_path = None
            self.anim_item = None

class animExporter:
    @staticmethod
    def to_studio_library(obj_sl, path, vpct):
        if not path.endswith('.anim'):
            return None

        tc = cmds.keyframe(obj_sl, q=1, tc=1)

        #anim
        sl = studio_library()
        if sl.anim_item == None:
            raise Warning('can\'t found studiolibrary in script path\nplease in install studiolibrary')
        anim_item = sl.anim_item.AnimItem(path)
        anim_item.save(objects=obj_sl, startFrame=tc[0], endFrame=tc[-1], bakeConnected=False)
        print('{} export anim finish'.format(path))

        # img sequences
        seq_dir = path + '/sequence'
        if not os.path.exists(seq_dir):
            os.mkdir(seq_dir)
        vpct.img_seq_capture('thumbnail', seq_dir)
        vpct.video_capture(path.replace('.anim', '_preview.mov'), w=720, h=720)

        # thumbnail
        img_file = [i for i in os.listdir(seq_dir) if i.endswith('.jpg')][0]
        img_path = seq_dir + os.sep + img_file
        new_img_file = 'thumbnail.jpg'
        new_img_path = path + os.sep + new_img_file
        shutil.copy(img_path, new_img_path)
