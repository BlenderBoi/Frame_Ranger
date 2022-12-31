
import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from bpy_extras import anim_utils


def push_all_to_nla(self, selected_only=False ,preclear="NONE"):
    
    strips = []

    action_list = self.get_action_list()

    nla_actions = self.collect_actions_from_nla()
   
    skipped = []
    # ALL / MATCH_TRACK_NAME / MATCH_STRIP_ACTION / EMPTY_MATCH_TRACK / NONE 
    # Remove Empty Track

    if preclear == "ALL":
        self.clear_all_nla_tracks() 



    for index, slot in enumerate(action_list): 

        check = True

        if selected_only:

            if slot.select:
                check = True
            else:
                check = False

        if check:
            
            second_check = True 

            if preclear == "PUSH_IF_NON_EXIST":

                
                if slot.action in nla_actions:
                    second_check = False

                
            if second_check: 
                strip = self.push_to_nla(index)
            else:
                skipped.append(slot.action)

    return skipped 


class FR_OT_BAKER_Bake_Deform_Armature(bpy.types.Operator):
    """Bake Deform Armature"""
    bl_idname = "fr_baker.bake_deform_armature"
    bl_label = "Bake Deform Armature"
    bl_options = {"REGISTER", "UNDO"}

    show_bake_settings: bpy.props.BoolProperty()

    def draw(self, context):

        baker = context.scene.FR_BAKER

        layout = self.layout
        # baker.draw(layout)



        layout.label(text="Rename Settings")
        box = layout.box()
        baker.draw_rename_settings(box)

        layout.separator()

        layout.label(text="Basic Settings")
        box = layout.box()
        baker.draw_basic_settings(box)


        layout.separator()
        box = layout.box()
        if Utility_Function.draw_subpanel(box, "Bake Settings", self, "show_bake_settings"):
            baker.draw_bake_settings(box)

        

    def invoke(self, context, event):
        
        baker = context.scene.FR_BAKER
        if baker.bake_show_popup:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def execute(self, context):

        scn = context.scene
        # obj = context.object

        baker = context.scene.FR_BAKER

        control_armature = baker.bake_from
        deform_armature = baker.bake_to


        if deform_armature and control_armature:

            control_action_helper = OAM_Functions.Action_List_Helper(control_armature)
            deform_action_helper = OAM_Functions.Action_List_Helper(deform_armature)


            OAM = control_action_helper.get_action_list()


            # Pre Process
            Control_Save_Use_NLA = False
            Deform_Save_Use_NLA = False

            control_animation_data = control_action_helper.get_actual_animation_data()
            deform_animation_data = deform_action_helper.get_actual_animation_data()

            if control_animation_data: 
                Control_Save_Use_NLA = control_armature.animation_data.use_nla
                control_armature.animation_data.use_nla = False

            if deform_animation_data: 
                Deform_Save_Use_NLA = deform_armature.animation_data.use_nla
                deform_armature.animation_data.use_nla = False

            if baker.Pre_Unmute:
                for bone in deform_armature.pose.bones:
                    for constraint in bone.constraints:
                        constraint.mute = False

            if baker.load_to_slot:
                if baker.preclear_slots:
                    deform_action_helper.clear(remove_action=False) 


            # if baker.push_to_nla:
            #     if baker.preclear_nla == "ALL":
            #         deform_action_helper.preclear_nla(deform_armature, clear_mode="ALL", action=None)

            # Pre Process Done
            if baker.push_to_nla:
                if baker.preclear_nla == "ALL":
                    deform_action_helper.clear_all_nla_tracks()


            for slot in OAM:
                slot.bake_temp_bool = slot.select 


            for loop in OAM:
                for index, slot in enumerate(OAM):

                    if slot.bake_temp_bool:

                        slot.bake_temp_bool = False
                        action = slot.action

                        if action:

                            control_action_helper.set_active_index(index, sync=True)


                            f_range = control_action_helper.get_slot_frame_range(slot, use_curve_range=False)

                            start_frame = int(f_range[0])
                            end_frame = int(f_range[1])

                            bake_settings = {}

                            bake_settings["only_selected"] = baker.only_selected
                            bake_settings["do_pose"] = baker.bake_pose
                            bake_settings["do_object"] = baker.bake_object
                            bake_settings["do_visual_keying"] = baker.visual_keying   
                            bake_settings["do_constraint_clear"] = baker.clear_constraint
                            bake_settings["do_parents_clear"] = baker.clear_parent
                            bake_settings["do_clean"] = baker.clean_curve


                            Name = Utility_Function.rename_item(baker.rename_mode, action.name, string_a=baker.string_a, string_b=baker.string_b) 

                            if baker.use_bake_name_when_available:
                                if not action.fr_settings.bake_name == "":
                                    Name = action.fr_settings.bake_name


                            
                            # baked_item = OAM_Functions.bake_deform_armature(control_armature, deform_armature, index, bake_settings, name=Name, replace=baker.overwrite, load=baker.load_to_slot)
                            # baked_slot = baked_item[0]
                            # baked_action = baked_item[1] 

                        

                            new_action = bpy.data.actions.new("new_action_" + Name)
                            new_action.frame_start = action.frame_start
                            new_action.frame_end = action.frame_end
                            new_action.use_frame_range = action.use_frame_range



                            if baker.overwrite:
                                replace_action = bpy.data.actions.get(Name)
                                if replace_action:
                                    replace_action.user_remap(new_action)
                                    bpy.data.actions.remove(replace_action)

                            new_action.name = Name

                            target_action = new_action

                            baked_action = Utility_Function.bake_action(deform_armature, None, target_action, start_frame, end_frame, bake_settings)
                            baked_action.use_fake_user = True 

                            if baker.load_to_slot:
                                new_slot = deform_action_helper.load_action(baked_action, use_fake_user=True, update_index=True, sync=True)


                            if baker.push_to_nla:

                                to_push = True

                                if baker.preclear_nla == "PUSH_IF_NON_EXIST":

                                    nla_actions = deform_action_helper.collect_actions_from_nla()

                                    if baked_action in nla_actions:
                                        to_push = False 

                                if to_push:
                                    track = deform_animation_data.nla_tracks.new()
                                    strip = track.strips.new(baked_action.name, 0, baked_action)
                                    track.name = strip.name

                            break


            if baker.Post_Mute:
                for bone in deform_armature.pose.bones:
                    for constraint in bone.constraints:
                        constraint.mute = True
                    

            if control_animation_data: 
                control_armature.animation_data.use_nla = Control_Save_Use_NLA 

            if deform_animation_data: 
                deform_armature.animation_data.use_nla = Deform_Save_Use_NLA 



        return {'FINISHED'}


classes = [FR_OT_BAKER_Bake_Deform_Armature]



def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
