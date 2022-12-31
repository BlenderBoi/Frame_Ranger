
import bpy
import blf
from Frame_Ranger import Utility_Function
from bpy_extras import anim_utils



# FREE HANGLE
def free_handle(action):

    for fc in action.fcurves:
        
        for kf in fc.keyframe_points:
            kf.handle_left_type = "FREE"
            kf.handle_right_type = "FREE"


def Insert_Start_End(object, action, start, end):

        for fc in action.fcurves:

                path = fc.data_path

                start_value = fc.evaluate(start)
                end_value = fc.evaluate(end)

                start_point = [start_value, start]
                end_point = [end_value, end]


                fc.keyframe_points.insert(start_point[1], start_point[0])
                fc.keyframe_points.insert(end_point[1], end_point[0])

                fc.update()
                Utility_Function.update_UI()




def Delete_Outside_Frame_Range(object, action, start, end):


    # current_action = object.animation_data.action

    object.animation_data.action = action


    for fc in action.fcurves:


        path = fc.data_path

        delete_list = []

        for kf in fc.keyframe_points:

            frame = kf.co.x

            if frame < start or frame > end:

                # fc.keyframe_points.remove(kf)
                # object.keyframe_delete(data_path=path, frame=kf.co.x)
                delete_list.append(kf)

        delete_list.reverse()

        for kf in delete_list:
            fc.keyframe_points.remove(kf, fast=True)





        # object.animation_data.action = current_action


def Offset_Action(action, start, end):

    scn = bpy.context.scene



    for fc in action.fcurves:
        for kf in fc.keyframe_points:
            kf.co.x -= start
            kf.handle_left[0] -= start
            kf.handle_right[0] -= start

    scn.frame_start = start-start
    scn.frame_end = end-start


def Frame_Range_From_Action(action):

    scn = bpy.context.scene

    start = action.frame_range[0]
    end = action.frame_range[1]

    scn.frame_start = start
    scn.frame_end = end





def Trim_Action(object, action, start, end, isInsertFrame=True, isOffset=True, isDelete=True):

    scn = bpy.context.scene

    free_handle(action)

    if isInsertFrame:
        Insert_Start_End(object, action, start, end)

    if isDelete:
        Delete_Outside_Frame_Range(object, action, start, end)


    free_handle(action)



def Mid_Point(value1, value2):

    return (value1+value2)/2


def Remap(value, source_frame_range, target_frame_range, subframe=True):
#    print(int((((value - source_frame_range[0]) * (target_frame_range[1] - target_frame_range[0])) / (source_frame_range[1] - source_frame_range[0])) + target_frame_range[0]))

    if subframe:

        return (((value - source_frame_range[0]) * (target_frame_range[1] - target_frame_range[0])) / (source_frame_range[1] - source_frame_range[0])) + target_frame_range[0]

    else:
        return int((((value - source_frame_range[0]) * (target_frame_range[1] - target_frame_range[0])) / (source_frame_range[1] - source_frame_range[0])) + target_frame_range[0])


def Reverse_Keyframe(keyframes):

    start = min([kf.co[0] for kf in keyframes])
    end = max([kf.co[0] for kf in keyframes])

    action = keyframes[0].id_data

    for kf in keyframes:
        kf.co[0] = -kf.co[0]
        kf.handle_left[0] = -kf.handle_left[0]
        kf.handle_right[0] = -kf.handle_right[0]

    for fc in action.fcurves:
        fc.update()

    for kf in keyframes:
        kf.co[0] = kf.co[0] + start + end
        kf.handle_left[0] = kf.handle_left[0] + start + end
        kf.handle_right[0] = kf.handle_right[0] + start + end


def Reverse_Action(action):

    keyframes = []
    fcurves = []

    start = action.frame_range[0]
    end = action.frame_range[1]

    for fc in action.fcurves:
        fcurves.append(fc)
        for kf in fc.keyframe_points:
            keyframes.append(kf)

    Reverse_Keyframe(keyframes)



def Scale_Point(value1, value2, rate, center):


    value1 = ((value1-center)*rate) + center
    value2 = ((value2-center)*rate) + center

    return [value1, value2]



def Time_Scale(keyframes, source_frame_range, target_frame_range):

    for kf in keyframes:

        kf.co[0] = Remap(kf.co[0], source_frame_range, target_frame_range)
        kf.handle_left[0] = Remap(kf.handle_left[0], source_frame_range, target_frame_range)
        kf.handle_right[0] = Remap(kf.handle_right[0], source_frame_range, target_frame_range)



def Time_Scale_Mode(keyframes, Source, Target):

    if Target[0] == "REMAP":

        if Target[1] > Target[2]:
            Reverse_Keyframe(keyframes)
            target_frame_range = [Target[2], Target[1]]

        else:
            target_frame_range = [Target[1], Target[2]]



    if Target[0] == "PERCENTAGE":

        rate = Target[1]/100
        center = Target[2]

        if center == "START":
            center = Source[0]

        if center == "END":
            center = Source[1]

        if center == "CENTER":
            center = Mid_Point(Source[0],Source[1])

        if type(center) == int:
            center = center

        target_frame_range = Scale_Point(Source[0], Source[1], rate, center)

    Time_Scale(keyframes, Source, target_frame_range)



def Time_Scale_Advanced(action, limit, Source, Target):

    keyframes = []

    for fc in action.fcurves:
        for kf in fc.keyframe_points:

            if limit == "ALL":
                keyframes.append(kf)

            if limit == "SELECTED":
                if kf.select_control_point:
                    keyframes.append(kf)

            if limit == "RANGE":
                if kf.co[0] >= Source[0] and kf.co[0] <= Source[1]:
                    keyframes.append(kf)

    Time_Scale_Mode(keyframes, Source, Target)




def Time_Scale_Action_Remap(action, start, end):

    Source = [action.frame_range[0], action.frame_range[1]]
    Target = ["REMAP", start, end]



    keyframes = []

    for fc in action.fcurves:
        for kf in fc.keyframe_points:

            keyframes.append(kf)

    Time_Scale_Mode(keyframes, Source, Target)



def Time_Scale_Action_Percentage(action, percentage, center):



    Source = [action.frame_range[0], action.frame_range[1]]
    Target = ["PERCENTAGE", percentage, center]

    keyframes = []

    for fc in action.fcurves:
        for kf in fc.keyframe_points:

            keyframes.append(kf)

    Time_Scale_Mode(keyframes, Source, Target)

    for fc in action.fcurves:
        fc.update()

#-------------------------------------------------------------------------------



def Time_Scale_LIVE(keyframes, source_frame_range, target_frame_range, use_Subframe, reverse):


    # if reverse:
    #     kfs = [kf[0] for kf in keyframes]
    #     Reverse_Keyframe(kfs)
    #
    for kf in keyframes:

        kf[0].co[0] = Remap(kf[1], source_frame_range, target_frame_range, use_Subframe)
        kf[0].handle_left[0] = Remap(kf[2], source_frame_range, target_frame_range, use_Subframe)
        kf[0].handle_right[0] = Remap(kf[3], source_frame_range, target_frame_range, use_Subframe)




def get_Ref_Keyframe(action, limit, start, end):

    keyframes = []

    for fc in action.fcurves:
        for kf in fc.keyframe_points:

            if limit == "ALL":
                keyframes.append(kf)

            if limit == "SELECTED":
                if kf.select_control_point:
                    keyframes.append(kf)

            if limit == "RANGE":
                if kf.co[0] >= start and kf.co[0] <= end:
                    keyframes.append([kf, kf.co[0], kf.handle_left[0], kf.handle_right[0]])


    return keyframes



#-------------------------------------------------------------------------------



def Frame_Modal_Operator_Callback(self, context):


    font_size = 10
    scaled_font_size = int(font_size * bpy.context.preferences.system.ui_scale)

    if self.Mode == "TIMESCALE":
        mode = "Timescale"
    if self.Mode == "TRIM":
        mode = "Trim"
    if self.Mode == "SETFRAME":
        mode = "Set Frame"
    if self.Mode == "BAKE":
        mode = "Bake"


    if self.Side == "END":
        text = """{} Start (Tab): {}""".format(mode, context.scene.frame_end)
    if self.Side == "START":
        text = """{} End (Tab): {}""".format(mode, context.scene.frame_start)

    text2 = """Subframe (Alt): {}""".format(self.use_Subframe)

    text3 = """Reverse (Ctrl): {}""".format(self.reverse)

    blf.size(0, scaled_font_size, 72)
    if len(self.mouse_path) > 0:
        blf.position(0, self.mouse_path[-1][0], self.mouse_path[-1][1]-20, 0)
        blf.draw(0, text2)

        blf.position(0, self.mouse_path[-1][0], self.mouse_path[-1][1], 0)
        blf.draw(0, text)

        # if self.Mode == "TIMESCALE":
        #     blf.position(0, self.mouse_path[-1][0], self.mouse_path[-1][1]-40, 0)
        #     blf.draw(0, text3)


        x, y = context.region.view2d.region_to_view(*self.mouse_path[-1] )
        # print(self.mouse_path[-1])
        if self.Side == "END":
            bpy.context.scene.frame_end = int(x)
        if self.Side == "START":
            bpy.context.scene.frame_start = int(x)




class FR_ACTION_OT_Frame_Modal_Operator(bpy.types.Operator):
    """Frame Modal Operator"""
    bl_idname = "fr.action_frame_modal"
    bl_label = "Frame Modal Operator"
    bl_options = {"REGISTER", "UNDO"}

    Mode: bpy.props.EnumProperty(default="TIMESCALE", items=[(("TIMESCALE"),("Timescale"),("Timescale")),(("SETFRAME"),("Set Frame"),("Set Frame")),(("TRIM"),("Trim"),("Trim")),(("BAKE"),("Bake"),("Bake"))])
    Side: bpy.props.EnumProperty(default="END", items=[(("START"),("Start"),("Start")),(("END"),("End"),("End"))])
    use_Subframe: bpy.props.BoolProperty(default=False)
    reverse: bpy.props.BoolProperty(default=True)
#    def execute(self, context):
#
#
#
#
#        if self.Mode == "TIMESCALE":
#
#            print("TIMESCALE")
#            action = context.object.animation_data.action
#            limit = "RANGE"
#            start = context.scene.frame_start
#            end = context.scene.frame_end
#
#            self.Keyframes_Pair = get_Ref_Keyframe(action, limit, start, end)
#
#
#        self.mouse_path = []
#
#        self.intial_Start = context.scene.frame_start
#        self.intial_End = context.scene.frame_end
#
#
#        context.window_manager.modal_handler_add(self)
#
#
#
#        args = (self, context)
#        self._handle = bpy.types.SpaceDopeSheetEditor.draw_handler_add(Frame_Modal_Operator_Callback, args, 'WINDOW', 'POST_PIXEL')
#
#        return {'RUNNING_MODAL'}
#





    def modal(self, context, event):

        context.area.tag_redraw()
        region = context.region
        #
        # if event.type == 'MOUSEMOVE':
        #
        #

        if self.Mode == "TIMESCALE":

            for object in bpy.context.selected_objects:
                if object.animation_data:
                    if object.animation_data.action:

                        action = object.animation_data.action

                        Source = [self.intial_Start, self.intial_End]
                        Target = [context.scene.frame_start, context.scene.frame_end]

                        for Keyframe_Pair in self.Keyframes_Pairs:

                            Time_Scale_LIVE(Keyframe_Pair, Source, Target, self.use_Subframe, self.reverse)



        self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))


        if event.type == 'TAB' and event.value == "PRESS":


            if self.Side == "END":
                self.Side = "START"

                #WRAP FUNCTION

                x, y = context.region.view2d.view_to_region(bpy.context.scene.frame_start, 0, clip=False)

                if (context.region.width + context.region.x) < x or x < 0 :
                    # bpy.ops.action.view_all()
                    x, y = bpy.context.region.view2d.view_to_region(bpy.context.scene.frame_start, 0, clip=False)

                x = x + context.region.x

                # context.window.cursor_warp(x, event.mouse_y)
                #


            elif self.Side == "START":

                self.Side = "END"

                x, y = context.region.view2d.view_to_region(bpy.context.scene.frame_end, 0, clip=False)

                if (context.region.width + context.region.x) < x or x < 0 :
                    bpy.ops.action.view_all()
                    x, y = bpy.context.region.view2d.view_to_region(bpy.context.scene.frame_end, 0, clip=False)

                x = x + context.region.x

                # context.window.cursor_warp(x, event.mouse_y)

#

        if event.type == 'LEFTMOUSE' and event.value == "PRESS":


            # bpy.types.SpaceDopeSheetEditor.draw_handler_remove(self._handle, 'WINDOW')

            if context.space_data.type == "DOPESHEET_EDITOR":
                bpy.types.SpaceDopeSheetEditor.draw_handler_remove(self._handle, 'WINDOW')

            if context.space_data.type == "GRAPH_EDITOR":
                bpy.types.SpaceGraphEditor.draw_handler_remove(self._handle, 'WINDOW')

            if context.space_data.type == "SEQUENCE_EDITOR":
                bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle, 'WINDOW')

            if context.space_data.type == "NLA_EDITOR":
                bpy.types.SpaceNLA.draw_handler_remove(self._handle, 'WINDOW')





            if self.Mode == "TRIM":

                for object in context.selected_objects:
                    if object.animation_data:
                        if object.animation_data.action:
                            Trim_Action(object, object.animation_data.action, context.scene.frame_start, context.scene.frame_end, isInsertFrame=True, isOffset=False, isDelete=True)


            if self.Mode == "BAKE":

                scn = context.scene
                for obj in context.selected_objects:

                    if obj.type == "ARMATURE":
                        do_pose = True
                    else:
                        do_pose = False


                    if obj.animation_data:
                        if obj.animation_data.action:

                            Insert_Start_End(obj, obj.animation_data.action, scn.frame_start, scn.frame_end)
                            free_handle(obj.animation_data.action)
                            frame = [i for i in range(scn.frame_start, scn.frame_end+1)]
                            obj_act = [[obj, obj.animation_data.action]]

                            Baked_Action = anim_utils.bake_action_objects(obj_act, frames=frame, only_selected=True, do_pose=do_pose, do_object=True, do_visual_keying=True, do_constraint_clear=False, do_parents_clear=False, do_clean=False)







            return {'FINISHED'}

        if event.type == "LEFT_ALT" and event.value=="PRESS":
            if self.use_Subframe:
                self.use_Subframe= False
            else:
                self.use_Subframe= True

        if event.type == "LEFT_CTRL" and event.value=="PRESS":
            if self.reverse:
                self.reverse= False
            else:
                self.reverse= True




        if event.type in ("MIDDLEMOUSE", "WHEELUPMOUSE", "WHEELDOWNMOUSE"):
            return {'PASS_THROUGH'}


        if event.type == 'RIGHTMOUSE':
            context.scene.frame_start = self.intial_Start
            context.scene.frame_end = self.intial_End

            if self.Mode == "TIMESCALE":



                for Keyframe_Pair in self.Keyframes_Pairs:
                    for keyframe_pair in Keyframe_Pair:
                        keyframe_pair[0].co[0] = keyframe_pair[1]

                self.Keyframes_Pairs.clear()

            # bpy.types.SpaceDopeSheetEditor.draw_handler_remove(self._handle, 'WINDOW')

            if context.space_data.type == "DOPESHEET_EDITOR":
                bpy.types.SpaceDopeSheetEditor.draw_handler_remove(self._handle, 'WINDOW')

            if context.space_data.type == "GRAPH_EDITOR":
                bpy.types.SpaceGraphEditor.draw_handler_remove(self._handle, 'WINDOW')

            if context.space_data.type == "SEQUENCE_EDITOR":
                bpy.types.SpaceSequenceEditor.draw_handler_remove(self._handle, 'WINDOW')

            if context.space_data.type == "NLA_EDITOR":
                bpy.types.SpaceNLA.draw_handler_remove(self._handle, 'WINDOW')


            return {'FINISHED'}


        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        context.scene.FR_TU_Autofit_Keyframe = False

        if not context.object and not self.Mode=="SETFRAME" :
            self.report({"INFO"}, "No Selected Object")
            return {'FINISHED'}





        if not context.selected_objects and not self.Mode=="SETFRAME" :
            context.object.select_set(True)


        if self.Mode == "TIMESCALE":

            self.Keyframes_Pairs = []

            for object in bpy.context.selected_objects:
                if object.animation_data:
                    if object.animation_data.action:

                        action = object.animation_data.action
                        limit = "RANGE"
                        start = context.scene.frame_start
                        end = context.scene.frame_end

                        self.Keyframes_Pairs.append(get_Ref_Keyframe(action, limit, start, end))


        self.mouse_path = []

        self.intial_Start = context.scene.frame_start
        self.intial_End = context.scene.frame_end


        context.window_manager.modal_handler_add(self)



        args = (self, context)

        if context.space_data.type == "DOPESHEET_EDITOR":
            self._handle = bpy.types.SpaceDopeSheetEditor.draw_handler_add(Frame_Modal_Operator_Callback, args, 'WINDOW', 'POST_PIXEL')

        if context.space_data.type == "GRAPH_EDITOR":
            self._handle = bpy.types.SpaceGraphEditor.draw_handler_add(Frame_Modal_Operator_Callback, args, 'WINDOW', 'POST_PIXEL')

        if context.space_data.type == "SEQUENCE_EDITOR":
            self._handle = bpy.types.SpaceSequenceEditor.draw_handler_add(Frame_Modal_Operator_Callback, args, 'WINDOW', 'POST_PIXEL')

        if context.space_data.type == "NLA_EDITOR":
            self._handle = bpy.types.SpaceNLA.draw_handler_add(Frame_Modal_Operator_Callback, args, 'WINDOW', 'POST_PIXEL')



        return {'RUNNING_MODAL'}

#        return context.window_manager.invoke_props_dialog(self)




class FR_TU_MT_Frame_Modal_Pie(bpy.types.Menu):

    bl_label = "Frame Modal Operator"
    bl_id = "fr_tu.frame_modal_operator_pie"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        pie = layout.menu_pie()
        # operator = pie.operator("fr.action_frame__snap_modal", text="Frame")
        operator = pie.operator("fr.action_frame_modal", text="Timescale Keyframe (Slow)", icon="TIME")
        operator.Mode = "TIMESCALE"
        operator.Side = "END"
        operator = pie.operator("fr.action_frame_modal", text="Set Frame Range", icon="PREVIEW_RANGE")
        operator.Mode = "SETFRAME"
        operator.Side = "END"
        operator = pie.operator("fr.action_frame_modal", text="Trim Keyframe", icon="NLA")
        operator.Mode = "TRIM"
        operator.Side = "END"
        pie.prop(scn, "FR_TU_Autofit_Keyframe", text="Auto Frame Range", icon="NOCURVE")

        operator = pie.operator("fr.action_frame_modal", text="Bake Keyframe (Experimental)", icon="DECORATE_KEYFRAME")
        operator.Mode = "BAKE"
        operator.Side = "END"

        # operator = pie.menu("FR_MT_KU_keyframe_utils_menu", text="Keyframe Utils")
        operator = pie.operator("fr_ku.randomize_keyframes", text="Randomize Keyframes", icon="MOD_NOISE")

#Work on other Animation Editor / Add and Remove Handler
#Limit Operator to Appropriate Editor / Poll
#Viewport Scrubber

#H To Hide Text Display
#Draw Frame/Line so No more Reliant on Start and End Frame
#F To Use Frame Range

#Experiment (Macro Function) -Frame Range / Get Intitial, Then Trim or Time Scale, Color Indicate Mode


#Optional --Number Input to Move Frame
#Add Move Frame to Pie


#WORK FOR ALL OBJECT


#WORK FOR SELECTED OBJECT -- Done
#Warp Mouse Position When Swapping -- Done


classes = [FR_ACTION_OT_Frame_Modal_Operator, FR_TU_MT_Frame_Modal_Pie]


def register():


    for cls in classes:

        bpy.utils.register_class(cls)



def unregister():

    # for km, kmi in addon_keymaps:
    #     km.keymap_items.remove(kmi)
    # addon_keymaps.clear()


    for cls in classes:

        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
