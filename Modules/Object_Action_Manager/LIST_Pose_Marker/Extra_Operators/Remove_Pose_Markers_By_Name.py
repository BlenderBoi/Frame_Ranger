import bpy

from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions


remove_mode=[("INCLUDE","Include","Include"),("EXCLUDE","Exclude","Exclude"), ("EXACT", "Exact", "Exact")]

class FR_OT_PMM_Remove_To_Markers_By_Name(bpy.types.Operator):

    bl_idname = "fr_pmm.remove_pose_markers_by_name"
    bl_label = "Remove Pose Markers By Name"
    bl_description = "Remove Pose Marker by Name"
    bl_options = {'UNDO', 'REGISTER'}
    
    mode: bpy.props.EnumProperty(items=remove_mode, default="INCLUDE")
    selected_only: bpy.props.BoolProperty()
    name: bpy.props.StringProperty()
    
    show_detected: bpy.props.BoolProperty(default=True)
    target_action: bpy.props.StringProperty()

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        layout.prop(self, "mode", text="Mode")
        layout.prop(self, "name", text="Name")
        layout.prop(self, "selected_only", text="Selected Markers Only")

        layout.label(text="Detected Marker Name")
        
        action = bpy.data.actions.get(self.target_action) 
    
        if action is not None:
            
            count = 0
            if Utility_Function.draw_subpanel(layout, "Detected Marker", self, "show_detected"):
                                               
                layout = layout.box()

                if self.selected_only:
                    markers = set([marker for marker in action.pose_markers if marker.select == True])
                else:
                    markers = set([marker for marker in action.pose_markers])

                for marker in markers:

                    if self.mode == "EXACT":
                        if marker.name == self.name:
                            layout.label(text=marker.name, icon="PMARKER_ACT")
                            count += 1

                    if self.mode == "INCLUDE":
                        if self.name in marker.name:
                            layout.label(text=marker.name, icon="PMARKER_ACT")
                            count += 1

                    if self.mode == "EXCLUDE":
                        if not self.name in marker.name:
                            layout.label(text=marker.name, icon="PMARKER_ACT")
                            count += 1

                if count == 0:
                    layout.label(text="No Match", icon="INFO")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):


        scn = context.scene
        
        action = bpy.data.actions.get(self.target_action) 

        if action:
            if self.selected_only:
                markers = [marker for marker in action.pose_markers if marker.select == True]
            else:
                markers = [marker for marker in action.pose_markers]


            for marker in markers:

                if self.mode == "EXACT":
                    if marker.name == self.name:
                        action.pose_markers.remove(marker)

                if self.mode == "INCLUDE":
                    if self.name in marker.name:
                        action.pose_markers.remove(marker)

                if self.mode == "EXCLUDE":
                    if not self.name in marker.name:
                        action.pose_markers.remove(marker)


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
