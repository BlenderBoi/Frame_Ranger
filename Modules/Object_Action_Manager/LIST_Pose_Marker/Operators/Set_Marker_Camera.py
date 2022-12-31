import bpy
from Frame_Ranger import Utility_Function


Set_Marker_Mode = [("VIEW","Create from View","From Current View"), ("ACTIVE","Active Camera","Active Camera"), ("CAMERA","Camera","Camera")]

class FR_OT_PMM_Set_Marker_Camera(bpy.types.Operator):

    bl_idname = "fr_pmm.set_marker_camera"
    bl_label = "Set Marker Camera"
    bl_description = "Set Marker Camera"
    bl_options = {'UNDO', 'REGISTER'}
    
    show_all: bpy.props.BoolProperty(default=False)
    index : bpy.props.IntProperty()
    view : bpy.props.BoolProperty(default=True)
    mode : bpy.props.EnumProperty(items=Set_Marker_Mode, default="CAMERA")
    name: bpy.props.StringProperty()

    target_action: bpy.props.StringProperty()


    def invoke(self, context, event):

        action = bpy.data.actions.get(self.target_action)
        scn = context.scene
    
        if action is not None:
            markers = action.pose_markers

            if len(markers) > self.index:
                marker = markers[self.index]

                scn.MM_Marker_Chooser_Limit = marker.camera
                scn.MM_Marker_Chooser = marker.camera

                self.name = marker.name

                return context.window_manager.invoke_props_dialog(self)

        return {'FINISHED'}


    def draw(self, context):


        #Add From Current View / Use Current View <- Only in View3D
        #Enum [Current View, Camera From Scene]


        action = bpy.data.actions.get(self.target_action)
        scn = context.scene

        if action is not None:

            markers = action.pose_markers

            if len(markers) > self.index:

                marker = markers[self.index]

                layout = self.layout

                layout.prop(self, "mode", text="Mode")

                if self.mode == "VIEW":
                    layout.prop(self, "name", text="Name")
                    layout.prop(self, "view", text="View")

                if self.mode == "CAMERA":

                    layout.prop(self, "show_all", text="Show All Object")

                    if not self.show_all:
                        layout.prop(scn, "MM_Marker_Chooser_Limit", text="", icon="OUTLINER_OB_CAMERA")
                    else:
                        layout.prop(scn, "MM_Marker_Chooser", text="", icon="OUTLINER_OB_CAMERA")



    def execute(self, context):

        scn = context.scene
        action = bpy.data.actions.get(self.target_action)
        
        if action is not None:

            markers = action.pose_markers

            if len(markers) > self.index:

                marker = markers[self.index]

                if self.mode == "CAMERA":

                    if not self.show_all:
                        marker.camera = scn.MM_Marker_Chooser_Limit
                    else:
                        marker.camera = scn.MM_Marker_Chooser

                    scn.MM_Marker_Chooser_Limit = None
                    scn.MM_Marker_Chooser = None

                if self.mode == "ACTIVE":

                    marker.camera = None

                    if context.object:
                        if context.object.type == "CAMERA":
                            marker.camera = context.object

                    if not marker.camera:

                        for object in context.selected_objects:
                            if object.type == "CAMERA":
                                marker.camera = object
                                break

                    if marker.camera:

                        camera = marker.camera

                        if self.view:
                            Utility_Function.view_camera(camera)






                if self.mode == "VIEW":

                    camera = Utility_Function.create_camera_from_view(self.name)
                    marker.camera = camera

                    if self.view:
                        Utility_Function.view_camera(camera)



            Utility_Function.update_UI()

        return {'FINISHED'}
















classes = [FR_OT_PMM_Set_Marker_Camera]





def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
