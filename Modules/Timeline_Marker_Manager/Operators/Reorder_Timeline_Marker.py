import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function

ENUM_Mode = [("DOWN", "Down", "Down"),("UP", "Up", "Up")]

class FR_OT_TMM_Reorder_Timeline_Marker(bpy.types.Operator):
    """Reorder Timeline Marker"""
    bl_idname = "fr_tmm.reorder_timeline_marker"
    bl_label = "Reorder Timeline Marker"
    bl_options = {'UNDO', 'REGISTER'}
    
    Index: bpy.props.IntProperty()
    Mode: bpy.props.EnumProperty(items=ENUM_Mode)

    Disable_Warning: bpy.props.BoolProperty(default=True)

    def invoke(self, context, event):

        preferences = Utility_Function.get_addon_preferences()

        if preferences.OAM_Timeline_Marker_Warning:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)


    def draw(self, context):
        layout = self.layout
        layout.label(text="This Operator: ", icon="ERROR")
        box = layout.box()
        box.label(text="Removes All Markers and Recreating it", icon="ERROR")
        box.label(text="Depending on the Situation, It might be destructive")
        box = layout.box()
        box.label(text="You Might Lose All Your Markers", icon="ERROR")
        box.label(text="If this Operator Fails Halfway")
        layout.prop(self, "Disable_Warning", text="Disable Warning")

    def execute(self, context):

        scn = context.scene
        
        preferences = Utility_Function.get_addon_preferences()

        if preferences.OAM_Timeline_Marker_Warning:
            if self.Disable_Warning:
                preferences.OAM_Timeline_Marker_Warning = False

        
        timeline_markers_index = scn.timeline_markers_index 

        proto_markers = []
        
        for timeline_marker in scn.timeline_markers:
            proto_marker = Timeline_Marker_Function.collect_marker_data(timeline_marker, type="TIMELINEMARKER")
            proto_markers.append(proto_marker)



        if self.Mode == "UP":
            if self.Index-1 >= 0:

                Timeline_Marker_Function.clear_timeline_markers(scn)
                item = proto_markers.pop(self.Index)
                proto_markers.insert(self.Index-1, item)
                Timeline_Marker_Function.recreate_timeline_markers(proto_markers, scn)
                scn.timeline_markers_index = timeline_markers_index

            Timeline_Marker_Function.index_up(scn)

        if self.Mode == "DOWN":
            if self.Index+1 < len(proto_markers):

                Timeline_Marker_Function.clear_timeline_markers(scn)
                item = proto_markers.pop(self.Index)
                proto_markers.insert(self.Index+1, item)
                # proto_markers = Utility_Function.list_swap_item(proto_markers, self.Index-1, self.Index)
                Timeline_Marker_Function.recreate_timeline_markers(proto_markers, scn)
                scn.timeline_markers_index = timeline_markers_index
            Timeline_Marker_Function.index_down(scn)


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_TMM_Reorder_Timeline_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
