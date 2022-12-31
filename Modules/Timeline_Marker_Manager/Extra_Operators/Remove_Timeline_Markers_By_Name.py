import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function

remove_mode=[("INCLUDE","Include","Include"),("EXCLUDE","Exclude","Exclude"), ("EXACT", "Exact", "Exact")]

class FR_OT_PMM_Remove_To_Markers_By_Name(bpy.types.Operator):

    bl_idname = "fr_tmm.remove_timeline_markers_by_name"
    bl_label = "Remove Timeline Markers By Name"
    bl_description = "Remove Timeline Marker by Name"
    bl_options = {'UNDO', 'REGISTER'}
    
    mode: bpy.props.EnumProperty(items=remove_mode, default="INCLUDE")
    selected_only: bpy.props.BoolProperty()
    name: bpy.props.StringProperty()
    show_detected: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        obj = context.object

        layout.prop(self, "mode", text="Mode")
        layout.prop(self, "name", text="Name")
        layout.prop(self, "selected_only", text="Selected Markers Only")

        layout.label(text="Detected Marker Name")
        

        if self.selected_only:
            markers = set([marker for marker in scn.timeline_markers if marker.select == True])
        else:
            markers = set([marker for marker in scn.timeline_markers])

        count = 0
        if Utility_Function.draw_subpanel(layout, "Detected Marker", self, "show_detected"):

            layout = layout.box()
            for marker in markers:

                if self.mode == "EXACT":
                    if marker.name == self.name:
                        layout.label(text=marker.name, icon="MARKER_HLT")
                        count += 1

                if self.mode == "INCLUDE":
                    if self.name in marker.name:
                        layout.label(text=marker.name, icon="MARKER_HLT")
                        count += 1

                if self.mode == "EXCLUDE":
                    if not self.name in marker.name:
                        layout.label(text=marker.name, icon="MARKER_HLT")
                        count += 1

            if count == 0:
                layout.label(text="No Match", icon="INFO")


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):


        scn = context.scene


        if self.selected_only:
            markers = [marker for marker in scn.timeline_markers if marker.select == True]
        else:
            markers = [marker for marker in scn.timeline_markers]


        for marker in markers:

            if self.mode == "EXACT":
                if marker.name == self.name:
                    scn.timeline_markers.remove(marker)

            if self.mode == "INCLUDE":
                if self.name in marker.name:
                    scn.timeline_markers.remove(marker)

            if self.mode == "EXCLUDE":
                if not self.name in marker.name:
                    scn.timeline_markers.remove(marker)


            scn.timeline_markers_index = len(scn.timeline_markers) - 1


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_PMM_Remove_To_Markers_By_Name]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
