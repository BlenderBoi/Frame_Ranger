from typing import Set
import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions


def sync_active_frame_range(self):

    scn = bpy.context.scene
    preferences = Utility_Function.get_addon_preferences()

    if self == FRM_Functions.get_active_fr():

    # Check ACtive
    # if preferences.FRM_Update_Active_Frame_Range and preferences.FRM_Sync_Active_Frame_Range:
        scn.FR_TU_Autofit_Keyframe = False 
        scn.frame_end = self.End
        scn.frame_start = self.Start

def update_frame_range(self, context):

    scn = bpy.context.scene
    active_fr = FRM_Functions.get_active_fr()
    scn.FR_TU_Autofit_Keyframe = False 
    scn.frame_end = active_fr.End
    scn.frame_start = active_fr.Start

def Limit_Frame_End(self, context):

    scn = context.scene

    sync_active_frame_range(self)

    if self.Start > self.End:
        self.Start = self.End-2

def Limit_Frame_Start(self, context):

    scn = context.scene

    sync_active_frame_range(self)

    if self.End < self.Start:
        self.End = self.Start+2





def update_frame_set_name(self, context):
    scn = self.id_data

    Frame_Range_Set = scn.FRM_Set
    sets_name = [slot.name for slot in Frame_Range_Set]

    sets_name.remove(self.name)
    

    if self.name in sets_name:
        duplicate_renamer = Utility_Function.Duplicates_Renamer()

        new_name = duplicate_renamer.check_and_rename_duplicates(self.name, sets_name)
        self.name = new_name   


def update_frame_range_name(self, context):

    scn = self.id_data
    Frame_Range_Sets = scn.FRM_Set


    my_set = None


    for set in Frame_Range_Sets:
        
        frame_ranges = [slot for slot in set.FRM]

        if self in frame_ranges:
            my_set = set
            break

    
    if my_set is not None: 

        ranges_name = [slot.name for slot in my_set.FRM]
        ranges_name.remove(self.name)


        if self.name in ranges_name:
            duplicate_renamer = Utility_Function.Duplicates_Renamer()

            new_name = duplicate_renamer.check_and_rename_duplicates(self.name, ranges_name)
            self.name = new_name  







class Frame_Range_Manager_Property_Group(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(update=update_frame_range_name)
    Start : bpy.props.IntProperty(min = 0, update = Limit_Frame_Start)
    End : bpy.props.IntProperty(min = 0, update = Limit_Frame_End)
    sorter_index: bpy.props.IntProperty()


class Frame_Range_Set_Property_Group(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(update=update_frame_set_name)
    FRM : bpy.props.CollectionProperty(type=Frame_Range_Manager_Property_Group)
    FRM_Index : bpy.props.IntProperty(update=update_frame_range)
    sorter_index: bpy.props.IntProperty()

classes = [Frame_Range_Manager_Property_Group, Frame_Range_Set_Property_Group]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.FRM_Set = bpy.props.CollectionProperty(type=Frame_Range_Set_Property_Group)
    bpy.types.Scene.FRM_Set_Index = bpy.props.IntProperty()
    bpy.types.Scene.FRM_Set_Show = bpy.props.BoolProperty(default=False)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.FRM_Set
    del bpy.types.Scene.FRM_Set_Index
    del bpy.types.Scene.FRM_Set_Show





if __name__ == "__main__":

    register()

