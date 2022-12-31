
import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


# ENUM_Preclear_Mode = [("PUSH_IF_NON_EXIST","Skip Push if Exist","Skip Push If Exist"), ("ALL", "Clear All NLA Track", "Clear All NLA Track"),("MATCH_TRACK_NAME","Clear Matching NLA Tracks by Name","Clear Matching NLA Tracks by Name"),("MATCH_STRIP_ACTION","Clear Matching NLA Strips by Action","Clear Matching NLA Strips by Action"),("MATCH_STRIP_NAME","Clear Matching NLA Strips by Name","Clear Matching NLA Strips by Name"), ("EMPTY_MATCH_TRACK","Clear All Strips From Matching NLA Tracks","Clear All Strips From Matching NLA Tracks by Name"), ("NONE","None","None")]
ENUM_Preclear_Mode = [("PUSH_IF_NON_EXIST","Skip Push if Exist","Skip Push If Exist"), ("ALL", "Clear All NLA Track", "Clear All NLA Track"), ("NONE","None","None")]


class FR_OT_OAM_Push_To_NLA(bpy.types.Operator):
    """Push to NLA"""
    bl_idname = "fr_oam.push_all_to_nla"
    bl_label = "Push to NLA"
    bl_options = {'UNDO', 'REGISTER'}
   
    target_object: bpy.props.StringProperty()

    selected_only: bpy.props.BoolProperty(default=False)
    preclear: bpy.props.EnumProperty(items=ENUM_Preclear_Mode, default="NONE")
    clear_empty_tracks: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "selected_only", text="Selected Only")
        layout.prop(self, "preclear", text="Preclear NLA")

        layout.prop(self, "clear_empty_tracks", text="Clear Empty NLA Tracks")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 
       
        if obj:

            bpy.ops.fr_oam.clean_action_list(target_object=obj.name)
            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            skipped_actions = action_list_helper.push_all_to_nla(selected_only=self.selected_only, preclear=self.preclear)

            for action in skipped_actions:
                self.report({"INFO"}, action.name + " already in NLA, skip push")

            if self.clear_empty_tracks:
                animation_data = action_list_helper.get_actual_animation_data()
               
                for loop in animation_data.nla_tracks:
                    for track in animation_data.nla_tracks:
                        if len(track.strips) == 0:
                            animation_data.nla_tracks.remove(track)
                            break


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Push_To_NLA]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
