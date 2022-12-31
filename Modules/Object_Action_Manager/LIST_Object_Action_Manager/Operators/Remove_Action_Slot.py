import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

def Update_Range_Start(self, context):

    if self.Start > self.End:
        self.End = self.Start

def Update_Range_End(self, context):

    if self.End < self.Start:
        self.Start = self.End


Range_Mode = [(("KEYFRAME"),("Keyframe"),("Keyframe")),(("ACTION"),("Action"),("Action")), (("MARKERS"),("Pose Marker"),("Marker")), (("NONE"),("None"),("None"))]

class FR_OT_OAM_Remove_Action_Slot(bpy.types.Operator):
    """Click to Remove Slot (Shift Click to Remove Action)"""
    bl_idname = "fr_oam.remove_action_slot"
    bl_label = "Remove Action Slot"
    bl_options = {"REGISTER", "UNDO"}

    remove_action: bpy.props.BoolProperty()
    cleanup: bpy.props.BoolProperty(default=False)

    index: bpy.props.IntProperty()
    
    target_object: bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout
        if self.cleanup:
            box = layout.box()
            box.label(text="This Affect All Objects in this File", icon="INFO")
            box.label(text="This will Check All Objects")
            box.label(text="And Remove Any Action Slot with Missing Actions")

        layout.prop(self, "cleanup", text="Clean Up")

    def invoke(self, context, event):

        if event.shift:
            self.remove_action = True
            return context.window_manager.invoke_props_dialog(self)
        else:
            self.remove_action = False
            return self.execute(context)


    def execute(self, context):


        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 



        if obj:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list_helper.remove_slot(self.index, self.remove_action, cleanup=self.cleanup)


            total = action_list_helper.get_total_actions()


            if total == 0:
                if obj.animation_data:
                    if obj.animation_data.action:
                        obj.animation_data.action = None


        Utility_Function.update_UI()

        return {'FINISHED'}

classes = [FR_OT_OAM_Remove_Action_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
