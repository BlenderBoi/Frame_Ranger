import bpy
from Frame_Ranger import Utility_Function

class FR_MT_AB_Extra_Menu(bpy.types.Menu):
    bl_label = "Action Bin Extras Menu"
    bl_idname = "OBJECT_MT_fr_ab_extra"

    def draw(self, context):

        layout = self.layout
        scn = context.scene




        preferences = Utility_Function.get_addon_preferences()
        operator = layout.operator("fr_oam.import_fbx_action", text="Import FBX Actions" ,icon="IMPORT")
        operator.load_to_object = False
        operator.target_object = "" 

        operator = layout.operator("fr_oam.choose_and_append_blendfile_action", text="Choose and Append Blend File Action" ,icon="FILE_BLEND")
        operator.load_to_object= False
        operator.target_object = "" 

        operator = layout.operator("fr_oam.append_all_actions_from_blendfiles", text="Append All Actions from Multiple Blend Files" ,icon="FILE_BLEND")
        operator.load_to_object= False
        operator.target_object = ""

        layout.separator()
        layout.operator("fr_ab.toogle_fake_users", text="Fake User On" ,icon="FAKE_USER_ON").fake_user = True
        layout.operator("fr_ab.toogle_fake_users", text="Fake User Off" ,icon="FAKE_USER_OFF").fake_user = False
        layout.separator()
        operator = layout.operator("fr_ab.remove_zero_user_actions", text="Remove Zero User Actions" ,icon="USER")
        operator = layout.operator("fr_ab.clear_action", text="Clear Action" ,icon="TRASH")
        layout.separator()
        operator = layout.operator("fr_ab.batch_rename_actions", text="Batch Rename Actions" ,icon="SORTALPHA")


class FR_MT_AB_Icon_Expose_Menu(bpy.types.Menu):
    bl_label = "Action Bin Icon Expose Menu"
    bl_idname = "OBJECT_MT_fr_ab_icon_expose"

    def draw(self, context):


        scn = context.scene
        obj = context.object
        layout = self.layout

        preferences = Utility_Function.get_addon_preferences()


        options = [
            ("AB_ICON_Select_Object", "Select Object", "OBJECT_DATA"),
            ("AB_ICON_Load_Action_To_Object", "Load Action To Object", "ACTION_TWEAK"),
            ("AB_ICON_Fake_User", "Fake User", "FAKE_USER_ON"),
            ("AB_ICON_Duplicate", "Duplicate", "DUPLICATE"),
            ("AB_ICON_Users", "Users", "USER"),
            ("AB_ICON_Remove", "Remove", "TRASH"),
        ]

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








classes = [FR_MT_AB_Extra_Menu, FR_MT_AB_Icon_Expose_Menu]



def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
