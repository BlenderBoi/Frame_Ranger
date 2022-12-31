import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions

class FR_OT_PMM_Add_Pose_Marker_As_Range(bpy.types.Operator):
    """Add Pose Marker to Range"""
    bl_idname = "fr_pmm.add_pose_marker_as_range"
    bl_label = "Add Pose Marker As Range"
    bl_options = {'UNDO', 'REGISTER'}
    
    name: bpy.props.StringProperty()
    frame: bpy.props.IntProperty()
    sync_frame : bpy.props.BoolProperty(default=True)

    target_action: bpy.props.StringProperty()

    mode: bpy.props.StringProperty()

    def draw(self, context):
        scn = context.scene

        layout = self.layout
        layout.prop(self, "name", text="Name")

        row = layout.row(align=True)
        row.prop(self, "sync_frame", text="", icon="UV_SYNC_SELECT")

        if self.sync_frame:
            row.prop(scn, "frame_current")
        else:
            row.prop(self, "frame", text="Frame")


    def invoke(self, context, event):

        preferences = Utility_Function.get_addon_preferences()

        scn = context.scene
        self.frame = scn.frame_current

        action = bpy.data.actions.get(self.target_action) 

        if action:
            self.name = Pose_Marker_Functions.default_name(action)
            return context.window_manager.invoke_props_dialog(self)

        else:
            return {'FINISHED'}

    def execute(self, context):

        scn = context.scene

        if self.sync_frame:
            self.frame = scn.frame_current

        action = bpy.data.actions.get(self.target_action) 

        if action is not None:

            marker = Pose_Marker_Functions.add_pose_marker(action, name=self.name, frame=self.frame)

            if marker is not None:
                if self.mode == "A":
                    action.fr_settings.pose_marker_a = marker.name

                if self.mode == "B":
                    action.fr_settings.pose_marker_b = marker.name

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_PMM_Add_Pose_Marker_As_Range]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
