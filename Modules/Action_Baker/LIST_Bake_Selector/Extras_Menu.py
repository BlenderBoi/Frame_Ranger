import bpy
from Frame_Ranger import Utility_Function


class FR_MT_BAKER_Icon_Expose_Menu(bpy.types.Menu):
    bl_label = "Action Baker Icon Expose Menu"
    bl_idname = "OBJECT_MT_fr_baker_icon_expose"

    def draw(self, context):

        scn = context.scene
        obj = context.object
        layout = self.layout

        preferences = Utility_Function.get_addon_preferences()

        options = [
            ("BAKER_ICON_Set_Active_Slot", "Set Active Slot", "ACTION_TWEAK"),                      #
            ("BAKER_ICON_Duplicate", "Duplicate", "DUPLICATE"),                      #
            ("BAKER_ICON_Bake_Name", "Bake Name", None),                      #
            ("BAKER_ICON_Frame_Range", "Frame Range", None),                      #
            ("BAKER_ICON_Fake_User", "Fake User", "FAKE_USER_ON"),                      #
            ("BAKER_ICON_Users", "Users", "USER"),                      #
            ("BAKER_ICON_REMOVE", "Remove", "X"),                      #
        ]

        # row.prop(preferences, "OAM_ICON_Bake", text="Bake Action")
        # row.prop(preferences, "OAM_ICON_Timescale", text="Timescale")
        # row.prop(preferences, "OAM_ICON_Trim", text="Trim")
        # row.prop(preferences, "OAM_ICON_Offset", text="Offset")
        # row.prop(preferences, "OAM_ICON_Set_Action", text="Set Action")



        for option in options:
            
            if option[2]:

                row = layout.row(align=True)
                row.label(text="", icon=option[2])
                row.prop(preferences, option[0], text=option[1], icon=option[2])
                row.separator()
            else:
                row = layout.row(align=True)
                row.label(text="", icon="DOT")
                row.prop(preferences, option[0], text=option[1])
                row.separator()



classes = [FR_MT_BAKER_Icon_Expose_Menu]



def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
