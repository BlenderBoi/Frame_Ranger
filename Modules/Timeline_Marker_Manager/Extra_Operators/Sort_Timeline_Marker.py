
import bpy

from Frame_Ranger import Utility_Function
from bpy.types import Preferences
from Frame_Ranger.Utility_Function import Timeline_Marker_Function

ENUM_Mode = [("DOWN", "Down", "Down"),("UP", "Up", "Up")]
ENUM_Sort_By = [("FRAME","Frame","Frame"),("NAME","Name","Name")]

class FR_OT_TMM_Sort_Timeline_Marker(bpy.types.Operator):
    """Sort Timeline Marker"""
    bl_idname = "fr_tmm.sort_timeline_markers"
    bl_label = "Sort Timeline Marker"
    bl_options = {'UNDO', 'REGISTER'}
    
    sort_by: bpy.props.EnumProperty(items=ENUM_Sort_By)
    reversed: bpy.props.BoolProperty(default=False)
    Disable_Warning: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):

        preferences = Utility_Function.get_addon_preferences()

        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.label(text="Sort By")
        layout.prop(self, "sort_by", text="")
        layout.prop(self, "reversed", text="Reverse")
        layout.prop(self, "Disable_Warning", text="Disable Warning")


        if not self.Disable_Warning:
            layout.label(text="This Operator: ", icon="ERROR")
            box = layout.box()
            box.label(text="Removes All Markers and Recreating it", icon="ERROR")
            box.label(text="Depending on the Situation, It might be destructive")
            box = layout.box()
            box.label(text="You Might Lose All Your Markers", icon="ERROR")
            box.label(text="If this Operator Fails Halfway")

    def execute(self, context):

        scn = context.scene
        
        preferences = Utility_Function.get_addon_preferences()


        timeline_markers_index = scn.timeline_markers_index 

        proto_markers = []
        
        for timeline_marker in scn.timeline_markers:
            proto_marker = Timeline_Marker_Function.collect_marker_data(timeline_marker, type="TIMELINEMARKER")
            proto_markers.append(proto_marker)

        Timeline_Marker_Function.clear_timeline_markers(scn)

        if self.sort_by == "NAME":
            proto_markers = sorted(proto_markers, key=lambda item: item.name, reverse=self.reversed)
        if self.sort_by == "FRAME":
            proto_markers = sorted(proto_markers, key=lambda item: item.frame, reverse=self.reversed)

        Timeline_Marker_Function.recreate_timeline_markers(proto_markers, scn)
        scn.timeline_markers_index = timeline_markers_index



        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_TMM_Sort_Timeline_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
