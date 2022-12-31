import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function


class FR_OT_TMM_Bind_Cameras_To_Markers_By_Name(bpy.types.Operator):

    bl_idname = "fr_tmm.bind_cameras_to_markers_by_name"
    bl_label = "Bind Cameras To Markers By Name"
    bl_description = "Bind Cameras to Marker by Name"
    bl_options = {'UNDO', 'REGISTER'}
    
    selected_only: bpy.props.BoolProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "selected_only", text="Selected Camera Only")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):


        scn = context.scene
        markers = scn.timeline_markers

        if self.selected_only:
            objects = context.selected_objects
        else:
            objects = scn.objects

        Cameras = [camera for camera in objects if camera.type == "CAMERA"]

        for marker in markers:
            for camera in Cameras:
                if camera.name == marker.name:
                    marker.camera = camera

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_TMM_Bind_Cameras_To_Markers_By_Name]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
