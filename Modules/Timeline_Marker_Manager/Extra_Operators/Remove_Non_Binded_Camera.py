import bpy

from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import Timeline_Marker_Function

class FR_OT_TMM_Remove_Non_Binded_Camera(bpy.types.Operator):

    bl_idname = "fr_tmm.remove_non_binded_camera"
    bl_label = "Remove Non Binded Camera"
    bl_options = {'UNDO', 'REGISTER'}

    confirm: bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure you want to Remove All Non Binded Camera")
        layout.prop(self, "confirm", text="Yes")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        if self.confirm:
            objects = context.view_layer.objects
            Markers_Cameras = [marker.camera for marker in context.scene.timeline_markers]


            for object in objects:
                if object.type == "CAMERA":
                    if not object in Markers_Cameras:
                        bpy.data.objects.remove(object)


            Utility_Function.update_UI()


        return {'FINISHED'}


classes = [FR_OT_TMM_Remove_Non_Binded_Camera]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
