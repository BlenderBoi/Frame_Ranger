import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function

Add_Camera_Mode = [("VIEW","Create from View","From Current View"), ("ACTIVE","Active Camera","Active Camera"), ("CAMERA","Camera","Camera")]



class FR_OT_TMM_Add_Timeline_Marker(bpy.types.Operator):

    bl_idname = "fr_tmm.add_timeline_marker"
    bl_label = "Add Timeline Marker to Scene"
    bl_description = "Add a new Timeline Marker to Scene"
    bl_options = {'UNDO', 'REGISTER'}
    
    Name: bpy.props.StringProperty()
    Frame: bpy.props.IntProperty()
    Sync_Frame : bpy.props.BoolProperty(default=True)


    View: bpy.props.BoolProperty(default=True)


    Bind: bpy.props.BoolProperty(default=False)
    Mode : bpy.props.EnumProperty(items=Add_Camera_Mode, default="CAMERA")
    Use_Custom_Name: bpy.props.BoolProperty(default=False)
    Camera_Name: bpy.props.StringProperty()
    Only_Camera: bpy.props.BoolProperty(default=True)





    def draw(self, context):
        scn = context.scene

        layout = self.layout
        layout.prop(self, "Name")

        row = layout.row(align=True)
        row.prop(self, "Sync_Frame", text="", icon="UV_SYNC_SELECT")

        if self.Sync_Frame:
            row.prop(scn, "frame_current")
        else:
            row.prop(self, "Frame")

            

        row = layout.row(align=True)

        row.prop(self, "Bind", text="Bind Camera")
        row = layout.row(align=True)
        if self.Bind:
            row.prop(self, "Mode", text="")

            if self.Mode == "VIEW":

                row = layout.row(align=True)

                if self.Use_Custom_Name:

                    row.prop(self, "Camera_Name", text="Camera")
                    row.prop(self, "Use_Custom_Name", text="", icon="SORTALPHA")
                else:
                    row.prop(self, "Use_Custom_Name", text="Set Camera Name", icon="SORTALPHA")



            if self.Mode == "CAMERA":

                row = layout.row(align=True)


                row.prop(self, "Only_Camera", text="", icon="VIEW_CAMERA")


                if self.Only_Camera:
                    row.prop(scn, "MM_Marker_Chooser_Limit", text="")
                else:
                    row.prop(scn, "MM_Marker_Chooser", text="")

                row = layout.row(align=True)


            row = layout.row()
            row.prop(self, "View", text="View Camera")



    def invoke(self, context, event):

        preferences = Utility_Function.get_addon_preferences()

        scn = context.scene
        self.Frame = scn.frame_current

        scn.MM_Marker_Chooser = scn.camera
        scn.MM_Marker_Chooser_Limit = scn.camera

        self.Name = "Timeline_Marker_" + str(len(scn.timeline_markers))
        self.Camera_Name = self.Name

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene

        if self.Sync_Frame:
            self.Frame = scn.frame_current

        Marker = Timeline_Marker_Function.add_timeline_marker(scn, name=self.Name, frame=self.Frame)


        if self.Bind:

            if self.Mode == "VIEW":

                if self.Use_Custom_Name:
                    Camera_Name = self.Camera_Name
                else:
                    Camera_Name = Marker.name


                camera = Utility_Function.create_camera_from_view(Camera_Name)
                Marker.camera = camera

                if self.View:
                    Utility_Function.view_camera(camera)


            if self.Mode == "CAMERA":
                if self.Only_Camera:
                    Marker.camera = scn.MM_Marker_Chooser_Limit
                else:
                    Marker.camera = scn.MM_Marker_Chooser


                camera = Marker.camera

                if self.View:
                    Utility_Function.view_camera(camera)


                scn.MM_Marker_Chooser_Limit = None
                scn.MM_Marker_Chooser = None


            if self.Mode == "ACTIVE":

                Marker.camera = None

                if context.object:
                    if context.object.type == "CAMERA":
                        Marker.camera = context.object

                if not Marker.camera:

                    for object in context.selected_objects:
                        if object.type == "CAMERA":
                            Marker.camera = object
                            break

                if Marker.camera:

                    camera = Marker.camera

                    if self.View:
                        Utility_Function.view_camera(camera)






        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_TMM_Add_Timeline_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
