import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

class FR_UL_BAKER_List(bpy.types.UIList):



    def filter_items(self, context, data, propname):

        filtered = []
        ordered = []
        items = getattr(data, propname)

        filtered = [self.bitflag_filter_item] * len(items)

        for i, item in enumerate(items):
            if not self.filter_name == "":
                if not self.filter_name in item.action.name:
                    filtered[i] &= ~self.bitflag_filter_item

        return filtered, ordered

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        scn = context.scene
        ob = data
        row = layout.row(align=True)
        obj = context.object
        row.alignment="LEFT"


        Baker = scn.FR_BAKER
        deform = Baker.bake_to 
        control = Baker.bake_from


        action = item.action

        preferences = Utility_Function.get_addon_preferences()

        if action:
            row = layout.row(align=True)
            row.prop(item, "select", text="")
                

        if preferences.BAKER_ICON_Set_Active_Slot:

            if item.id_data == deform:
                operator = row.operator("fr_oam.set_active_slot", text="", icon = "ACTION_TWEAK")
                operator.Index = index
                operator.target_object = "DEFORM"

            if item.id_data == control:
                operator = row.operator("fr_oam.set_active_slot", text="", icon = "ACTION_TWEAK")
                operator.Index = index
                operator.target_object = "CONTROL"


        if preferences.BAKER_ICON_Duplicate:

            if item.id_data == deform:
                operator = row.operator("fr_oam.duplicate_action_slot", text="", icon = "DUPLICATE")
                operator.Index = index
                operator.target_object = "DEFORM"

            if item.id_data == control:
                operator = row.operator("fr_oam.duplicate_action_slot", text="", icon = "DUPLICATE")
                operator.Index = index
                operator.target_object = "CONTROL"




        row.prop(action, "name", text="", emboss=False, icon="ACTION")

        row = layout.row(align=True)
        row.alignment = "RIGHT"
            
        if preferences.BAKER_ICON_Bake_Name:
            row.prop(item, "bake_name", text="",icon="KEYFRAME")

        if preferences.BAKER_ICON_Frame_Range:

             if item.range_mode == "RANGE":
                if item.action:
                    if item.action.use_frame_range:
                        # row.label(text=str(int(item.action.frame_start))+ " - " +str(int(item.action.frame_end)), icon="PREVIEW_RANGE")
                        # row.label(text="", icon="PREVIEW_RANGE")
                        row.prop(item.action, "use_frame_range", text="", icon="PREVIEW_RANGE")
                        row.prop(item.action, "frame_start", text="")
                        row.prop(item.action, "frame_end", text="")
                    
                    
                    else:
                        # row.label(text=str(int(item.action.curve_frame_range[0]))+ " - " +str(int(item.action.curve_frame_range[1])), icon="TIME")
                        # row.label(text="", icon="TIME")
                        row.prop(item.action, "use_frame_range", text="", icon="PREVIEW_RANGE")
                        row.prop(item.action, "curve_frame_range", index=0, text="")
                        row.prop(item.action, "curve_frame_range", index=1, text="")
    
             if item.range_mode == "POSE_MARKERS":
                markers = OAM_Functions.get_pose_markers(obj, index)
                
                marker_a = markers[0]
                marker_b = markers[1]


                if marker_a and marker_b:
                    
                    start_range = min(marker_a.frame, marker_b.frame)
                    end_range = max(marker_a.frame, marker_b.frame)

                    # row.label(text=str(int(start_range)) + " - " + str(int(end_range)), icon="PMARKER_ACT")

                    row.label(text="", icon="PMARKER_ACT")
                    if marker_a.frame <= marker_b.frame:

                        row.prop(marker_a, "frame", text="")
                        row.prop(marker_b, "frame", text="")
                    else:
                        row.prop(marker_b, "frame", text="")
                        row.prop(marker_a, "frame", text="")  

                else:
                    row.label(text="", icon="PMARKER")
 

        if preferences.BAKER_ICON_Fake_User:

            row.prop(item.action, "use_fake_user", text="")


        if preferences.BAKER_ICON_Users:

            row.label(text=str(item.action.users), icon="USER")


        if preferences.BAKER_ICON_REMOVE:

            if item.id_data == deform:
                operator = row.operator("fr_oam.remove_action_slot", text="", icon = "X")
                operator.Index = index
                operator.target_object = "DEFORM"

            if item.id_data == control:
                operator = row.operator("fr_oam.remove_action_slot", text="", icon = "X")
                operator.Index = index
                operator.target_object = "CONTROL"



classes = [FR_UL_BAKER_List]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
