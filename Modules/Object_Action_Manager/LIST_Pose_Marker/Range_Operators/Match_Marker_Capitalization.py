import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions


match = [("MARKER","Rename Marker","Rename Marker"),("MATCH","Match Name","Match Name")]

class FR_OT_OAM_Match_Marker_Name_Capitalization(bpy.types.Operator):
    """Match Marker Name Capitalization"""

    bl_idname = "fr_pmm.match_marker_name_capitalization"
    bl_label = "Match Marker Name Capitalization"
    bl_options = {'UNDO', 'REGISTER'}
    
    match: bpy.props.EnumProperty(items=match, default="MATCH")
    index: bpy.props.IntProperty()
    mode: bpy.props.StringProperty()

    target_action: bpy.props.StringProperty()

    def draw(self, context):

        layout = self.layout
        layout.prop(self, "match", text="Match")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):


        scn = context.scene
        action = bpy.data.actions.get(self.target_action)
        if action is not None:

            for marker in action.pose_markers:


                if self.match == "MATCH":

                    if self.mode == "A":

                        if action.fr_settings.pose_marker_a.lower() == marker.name.lower():
                            action.fr_settings.pose_marker_a = marker.name
                            break

                    if self.mode == "B":

                        if action.fr_settings.pose_marker_b.lower() == marker.name.lower():
                            action.fr_settings.pose_marker_b = marker.name
                            break

                if self.match == "MARKER":

                    if self.mode == "A":

                        if action.fr_settings.pose_marker_a.lower() == marker.name.lower():
                            marker.name = action.fr_settings.pose_marker_a
                            break

                    if self.mode == "B":

                        if action.fr_settings.pose_marker_b.lower() == marker.name.lower():
                            marker.name = action.fr_settings.pose_marker_b
                            break





            Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Match_Marker_Name_Capitalization]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()

















