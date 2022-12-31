import bpy

from Frame_Ranger import Utility_Function

class FR_PT_BAKER_Base(bpy.types.Panel):
    bl_label = "Action Baker"

    def draw(self, context):
        
        scn = context.scene
        layout = self.layout

        Baker = scn.FR_BAKER
        Baker.draw(context,layout)

        preferences = Utility_Function.get_addon_preferences()

        row = layout.row()

