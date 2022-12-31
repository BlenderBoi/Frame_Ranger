import bpy
from Frame_Ranger import Utility_Function



class FR_UL_Action_Bin(bpy.types.UIList):

    # def filter_items(self, context, data, propname):
    #
    #     filtered = []
    #     ordered = []
    #     items = getattr(data, propname)
    #
    #     filtered = [self.bitflag_filter_item] * len(items)
    #
    #     for i, item in enumerate(items):
    #         if not self.filter_name == "":
    #             if not self.filter_name in item.name:
    #                 filtered[i] &= ~self.bitflag_filter_item
    #
    #     return filtered, ordered

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        preferences = Utility_Function.get_addon_preferences()

        scn = context.scene
        ob = data
        row = layout.row(align=True)


        # obj = context.object
        obj = context.active_object
        
        if obj is not None:
            obj_name = obj.name
        else:
            obj_name = ""


        row.alignment = "LEFT"

        if preferences.AB_ICON_Select_Object:
            row.operator("fr_ab.select_object_with_action", text="", icon = "OBJECT_DATA").index = index
        #
        if preferences.AB_ICON_Load_Action_To_Object:

            add = row.operator("fr_oam.load_action_slot", text="", icon = "ACTION_TWEAK")
            add.load_action_name = item.name
            add.target_object = obj_name 



        if preferences.AB_ICON_Fake_User:
            row.prop(item, "use_fake_user", text="")

        if preferences.AB_ICON_Duplicate:
            row.operator("fr_ab.duplicate_action", text="", icon = "DUPLICATE").index = index

        if preferences.AB_ICON_Users:
            row.label(text=str(item.users), icon="USER")

        row = layout.row(align=True)
        row.prop(item, "name", text="", emboss=False)
        row = layout.row(align=True)

        row.alignment = "RIGHT"

        if preferences.AB_ICON_Remove:
            row.operator("fr_ab.remove_action", text="", icon = "TRASH").index = index




classes = [FR_UL_Action_Bin]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
