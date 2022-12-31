import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import FRM_Functions


class Action_Slot(bpy.types.PropertyGroup):

    action : bpy.props.PointerProperty(name="Action", type=bpy.types.Action, update=OAM_Functions.update_frame_range)
    select: bpy.props.BoolProperty()

    sorter_index: bpy.props.IntProperty()
    bake_temp_bool: bpy.props.BoolProperty(default=False)

    def duplicate(self, name, replace_slot=False ,use_fake_user=True, update_index=True, below_slot=False):

        obj = self.id_data
        action = self.action
        
        settings = self.get_settings_dict()

        if action is not None:

            action_helper = OAM_Functions.Action_List_Helper(obj)

            index = action_helper.find_slot_index(self)

            new_action = action.copy() 
            new_action.name = name

            slot = action_helper.load_action(new_action, use_fake_user=use_fake_user, update_index=True)


            if slot is not None:

                slot.use_settings_dict(settings)

                if below_slot:

                    from_index = action_helper.get_last_index()
                    to_index = index+1
                    
                    action_helper.move_slot_by_index(from_index, to_index, update_index=True)

                if replace_slot:

                    action_helper.remove_slot(index)

            return slot


    def get_settings_dict(self):
        
        settings = {}

        settings["select"] = self.select

        return settings

    def use_settings_dict(self, settings):
        
        self.select = settings["select"]


def update_match_range_to_curve(self, context):
    
    if self.match_range_to_curve:
        self.match_range_to_curve = False
        action = self.id_data
        action.frame_start = int(action.curve_frame_range[0])
        action.frame_end = int(action.curve_frame_range[1])


def switch_frame_range_set(self, context):
   
    scn = context.scene
    
    sets = scn.FRM_Set
        
    set_name = [set.name for set in sets]
    if self.frame_range_set in set_name:
        index = set_name.index(self.frame_range_set)

        FRM_Functions.set_active_set(index) 





class FR_Settings(bpy.types.PropertyGroup):

    bake_name: bpy.props.StringProperty()
    match_range_to_curve: bpy.props.BoolProperty(default=False, update=update_match_range_to_curve)

    show_extra_settings: bpy.props.BoolProperty(default=False)

    frame_range_set: bpy.props.StringProperty(update=switch_frame_range_set)

    use_pose_marker_as_range: bpy.props.BoolProperty(default=False)

    pose_marker_a: bpy.props.StringProperty(options={'TEXTEDIT_UPDATE'})
    pose_marker_b: bpy.props.StringProperty(options={'TEXTEDIT_UPDATE'})
    pose_marker_by_name: bpy.props.BoolProperty() 


    def copy_settings(self, settings):
    
        self.bake_name = settings.bake_name




classes = [Action_Slot, FR_Settings]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.action_list = bpy.props.CollectionProperty(type=Action_Slot)
    bpy.types.Object.action_list_index = bpy.props.IntProperty(update=OAM_Functions.update_frame_range)
    
    bpy.types.Action.fr_settings = bpy.props.PointerProperty(type=FR_Settings)
    bpy.types.Action.pose_markers_index = bpy.props.IntProperty()



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.action_list
    del bpy.types.Object.action_list_index

    del bpy.types.Action.fr_settings






if __name__ == "__main__":

    register()

