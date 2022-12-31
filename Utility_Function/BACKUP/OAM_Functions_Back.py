import bpy
from Frame_Ranger import Utility_Function
from bpy.types import Action
from bpy_extras import anim_utils

import itertools
import json



def sort_getSize(item):

    obj = item.id_data
    
    action_list_helper = Action_List_Helper(obj)
    
    range_size = action_list_helper.calculate_slot_range_size(item)
    
    return range_size




class Action_List_Helper:

    def __init__(self, obj):
        
        self.obj = obj


    ######

    def get_action_list(self):
        
        return self.obj.action_list

    ######

    def get_total_actions(self):
        
        return len(self.get_action_list())

    def check_index(self, index):

        if index >= 0:
            if self.get_total_actions() > index:
                return True
        #     else:
        #         print("Index Out of Bound")
        # else:
        #     print("Index Is Lower than 0")
                
        return False

    def clamp_index(self, index):
        
        new_index = Utility_Function.clamp(0, index, self.get_last_index())

        return new_index

    def set_active_index(self, index, sync=True):   
        
        self.obj.action_list_index = self.clamp_index(index)

        if sync:
            self.sync_active_slot(use_curve_range=False, sync_frame_range_set=True)


    def clamp_active_index(self, sync):
       
        index = self.get_active_index()
        self.set_active_index(index, sync=True)
        
    ######
    def get_active_slot_frame_range(self, use_curve_range=False):

        slot = self.get_active_slot()

        return self.get_slot_frame_range(slot, use_curve_range=use_curve_range)


    def get_slot_frame_range(self, slot, use_curve_range=False):

        if slot is not None:
            action = slot.action

            if action is not None:
                frame_range = self.get_action_frame_range(action, use_curve_range=use_curve_range)
                return frame_range







            else:
                print("Action Not Found")
                return [None, None]

        else:
            print("Slot Not Found")
            return [None, None]



    def get_slot_frame_range_by_index(self, index, use_curve_range=False):

        slot = self.get_slot(index)

        if slot is not None:
            frame_range = self.get_slot_frame_range(slot, use_curve_range=use_curve_range)
            return frame_range

        else:
            print("Slot not Found")
            return [None, None]

    def get_action_frame_range(self, action, use_curve_range=False):
        
        if action is not None:

            start = None
            end = None

            if use_curve_range:
                start = action.curve_frame_range[0]
                end = action.curve_frame_range[1]
            else:
                if action.use_frame_range:
                    start = action.frame_start    
                    end = action.frame_end
                else:
                    start = action.curve_frame_range[0]
                    end = action.curve_frame_range[1]


            preferences = Utility_Function.get_addon_preferences()

            if preferences.ENABLE_Pose_Markers_As_Range:

                fr_settings = action.fr_settings
                # if scn.FR_TU_Auto_Frame_Range_Settings.Use_Pose_Marker_As_Range:

                marker_a = None
                marker_b = None

                if fr_settings.use_pose_marker_as_range:

                    markers_frame_ranges = self.get_active_pose_marker_as_range()

                    marker_start = markers_frame_ranges[0]
                    marker_end = markers_frame_ranges[1]

                    if marker_start is not None and marker_end is not None:

                        start = marker_start
                        end = marker_end











            return [start, end]

        else:
            print("Action Not Found")
            return [None, None]

    ######


    def get_active_pose_marker_as_range(self):

        slot = self.get_active_slot()

        frame_ranges = [None, None]

        if slot is not None:

            frame_ranges = self.get_pose_marker_as_range_by_slot(slot) 

        return frame_ranges



    def get_pose_marker_as_range_by_index(self, index):
        
        slot = self.get_slot(index)
   
        frame_ranges = [None, None]

        if slot is not None:

            frame_ranges = self.get_pose_marker_as_range_by_slot(slot) 

        return frame_ranges

    def get_pose_marker_as_range_by_slot(self, slot):

        start = None
        end = None

        if slot is not None:

            action = slot.action

            if action is not None:

                marker_a = None
                marker_b = None

                fr_settings = action.fr_settings 

                if fr_settings.pose_marker_a:
                    marker_a = action.pose_markers.get(fr_settings.pose_marker_a)

                if fr_settings.pose_marker_b:
                    marker_b = action.pose_markers.get(fr_settings.pose_marker_b)

                if marker_a and marker_b:

                    start = min(marker_a.frame, marker_b.frame)
                    end = max(marker_a.frame , marker_b.frame) 
        
        return [start, end]



    ######

    def sync_scene_frame_range(self, start, end):

        if start is not None and end is not None:
            scn = bpy.context.scene
            scn.frame_start = int(start)
            scn.frame_end = int(end)
        else:
            print("Fail to Sync Frame Range")

    def sync_slot(self, slot, use_curve_range=False, sync_frame_range_set=True):
    
        preferences = Utility_Function.get_addon_preferences()


        scn = bpy.context.scene
      
        if slot is not None:
            self.set_actual_action(slot.action)
            frame_range = self.get_slot_frame_range(slot, use_curve_range=use_curve_range)

            start = frame_range[0]
            end = frame_range[1]


            action = slot.action

            if action is not None:
                fr_settings = action.fr_settings

                if sync_frame_range_set:
                    fr_settings.frame_range_set = action.fr_settings.frame_range_set



                # if preferences.ENABLE_Pose_Markers_As_Range:

                    # if scn.FR_TU_Auto_Frame_Range_Settings.Use_Pose_Marker_As_Range:

                   #  marker_a = None
                   #  marker_b = None
                   #
                   #  if fr_settings.use_pose_marker_as_range:
                   # 
                   #      markers_frame_ranges = self.get_active_pose_marker_as_range()
                   #
                   #      marker_start = markers_frame_ranges[0]
                   #      marker_end = markers_frame_ranges[1]
                   #
                   #      if marker_start is not None and marker_end is not None:
                   #
                   #          start = marker_start
                   #          end = marker_end





                        

            self.sync_scene_frame_range(start, end)


    def sync_slot_by_index(self, index, use_curve_range=False, sync_frame_range_set=True):

        slot = self.get_slot(index)
        self.sync_slot(slot, use_curve_range=use_curve_range, sync_frame_range_set=sync_frame_range_set) 


    def sync_active_slot(self, use_curve_range=False, sync_frame_range_set=True):

        index = self.get_active_index()
        self.sync_slot_by_index(index, use_curve_range=use_curve_range, sync_frame_range_set=sync_frame_range_set)

    ######

    def get_active_index(self):
        
        return self.obj.action_list_index

    def get_first_index(self):

        return 0

    def get_last_index(self):        

        amount = self.get_total_actions()
        last_index = amount -1

        return last_index 

    ######

    def get_actual_animation_data(self):

        animation_data = Utility_Function.get_animation_data(self.obj)

        if animation_data is None:
            print("Failed to Get Animation Data")

        return animation_data

    def get_actual_action(self):

        animation_data = self.get_actual_animation_data()

        if animation_data is not None:

            return animation_data.action    

    def set_actual_action(self, action):

        animation_data = self.get_actual_animation_data()
        if animation_data is not None:
            animation_data.action = action


    ######

    def get_slot(self, index):

        if self.check_index(index): 
            action_list = self.get_action_list()
            return action_list[index]
        # else:
        #     print("Failed to Get Slot")
        #     return None

    def get_active_slot(self):
        
        index = self.get_active_index()

        return self.get_slot(index)
   
    def get_action(self, index):

        slot = self.get_slot(index) 

        if slot is not None:
            return slot.action

    def get_active_action(self):

        slot = self.get_active_slot() 

        if slot is not None: 
            return slot.action
        # else:
        #     print("Slot not Found")

    def collect_action_list(self):

        collected_actions = [] 

        action_list = self.get_action_list()  

        if action_list is not None:
            for slot in action_list:

                if slot.action:
                    collected_actions.append(slot.action)
        else:
            print("Failed to get Action List")
                
        return collected_actions

    def has_action(self, action):
        
        actions = self.collect_action_list()

        if action in actions:
            return True
        else:
            return False

    def find_action_index(self, action):

        actions = self.collect_action_list() 

        if action in actions:
            return actions.index(action)

        return None

    def find_slot_index(self, slot):
        
        action_list = self.get_action_list()
        slots = list(action_list)
   
        if slot in slots:
            return slots.index(slot)
    
        return None

    def set_slot_from_action(self, action, sync=True):
        
        index = self.find_action_index(action)

        if index is not None:
            self.set_active_index(index, sync=sync)
        else:
            print("Action is not in Object's Action List")
    
    def set_slot_from_slot(self, slot, sync=True):
        
        index = self.find_slot_index(slot)

        if index is not None:
            self.set_active_index(index, sync=sync)

    ######

    def active_index_up(self, sync=True):
       
        index = self.get_action_list() - 1
        self.set_active_index(index, sync=sync)

    def active_index_down(self, sync=True):
       
        index = self.get_action_list() + 1
        self.set_active_index(index, sync=sync)

    def active_index_last(self, sync=True):
        
        index = self.get_last_index()
        self.set_active_index(index, sync=sync)


    def active_index_first(self, sync=True):
        
        index = self.get_first_index()
        self.set_active_index(index, sync=sync)

    ######

    def new_empty_slot(self):

        action_list = self.get_action_list()
        slot = action_list.add()
            

        return slot

    ######

    def load_new_action(self, name, use_fake_user=True, update_index=True):

        action = bpy.data.actions.new(name)

        slot = self.load_action(action, use_fake_user=use_fake_user, update_index=update_index)

        return slot 

    def load_action(self, action, use_fake_user=True, update_index=True, sync=True):

        if action is not None:
            if not self.has_action(action):

                action.use_fake_user = use_fake_user 

                slot = self.new_empty_slot() 
                slot.action = action
               
                if update_index:
                    self.active_index_last(sync=sync)

                return slot 

            else:
                print("Action Already Loaded, Skip Operation")

        else:
            print("No Action to Load")
    
    def load_active_action(self, use_fake_user=True, update_index=True):

        action = self.get_actual_action()

        if action is not None:

            if self.has_action(action):

                slot = self.load_action(self, action, use_fake_user=use_fake_user, update_index=True) 
                return slot


    def fix_active_action(self, use_fake_user=True, update_index=True, sync=True):
       
        action = self.get_actual_action()
        
        if self.has_action(action):

            self.set_slot_from_action(action, sync=sync)

        else:

            self.load_active_action(use_fake_user=use_fake_user, update_index=update_index)



    ######

    def duplicate_slot(self, slot, name, replace_slot=False, use_fake_user=True, update_index=True, below_slot=False):
        
        if slot is not None:
            new_slot = slot.duplicate(name, replace_slot=replace_slot, use_fake_user=use_fake_user, update_index=update_index, below_slot=below_slot) 
            return new_slot

    def duplicate_slot_by_index(self, index, name, replace_slot=False, use_fake_user=True, update_index=True, below_slot=False):
      
        slot = self.get_slot(index)
        new_slot = self.duplicate_slot(slot, name, replace_slot=replace_slot, use_fake_user=use_fake_user, update_index=update_index, below_slot=below_slot)

        return new_slot

    def duplicate_active_slot(self, name, replace_slot=False, use_fake_user=True, update_index=True, below_slot=False):

        slot = self.get_active_slot() 
        new_slot = self.duplicate_slot(slot, name, replace_slot=replace_slot, use_fake_user=use_fake_user, update_index=update_index, below_slot=below_slot)
        
        return new_slot

    ######

    def move_slot(self, slot, to_index, update_index=True, sync=True):

        from_index = self.find_slot_index(slot) 
        self.move_slot_by_index(from_index, to_index, update_index=update_index, sync=sync)

    def move_slot_by_index(self, from_index, to_index, update_index=True, sync=True):
        

        if from_index is not None and to_index is not None:

            from_index = self.clamp_index(from_index)
            to_index = self.clamp_index(to_index)


            action_list = self.get_action_list() 
            action_list.move(from_index, to_index)

            if update_index:
                self.set_active_index(to_index, sync=sync)

        else:
            print("Index Out of Bound")



    def move_active_up(self, update_index=True, sync=True):

        from_index = self.get_active_index()
        to_index =  from_index - 1

        self.move_slot_by_index(from_index, to_index, update_index=update_index, sync=sync)

        if update_index:
            self.set_active_index(to_index, sync=sync)


    def move_active_down(self, update_index=True, sync=True):

        from_index = self.get_active_index()
        to_index =  from_index + 1

        self.move_slot_by_index(from_index, to_index, update_index=update_index, sync=sync)

        if update_index:
            self.set_active_index(to_index, sync=sync)


    ######

    def remove_slot(self, index, remove_action=False, sync=True):


        total = self.get_total_actions()
        
        if total > 0:
            action_list = self.get_action_list() 

            action = self.get_action(index)

            if self.check_index(index):

                action_list.remove(index)

                active_index = self.get_active_index()

                if active_index >= index:
                    self.set_active_index(active_index-1, sync=sync)

                self.clamp_active_index(sync=True)

                if remove_action:
                    
                    self.remove_action(action, cleanup=True)


    def remove_action(self, action, cleanup=True):

        if action is not None:
            bpy.data.actions.remove(action)

        if cleanup:
            for obj in bpy.data.objects:
                action_list_helper = Action_List_Helper(obj) 
                action_list_helper.cleanup()



    def cleanup(self, sync=True):
        
        action_list = self.get_action_list() 
      

        for loop in action_list:

            for index, slot in enumerate(action_list):

                if slot.action == None:
                    self.remove_slot(index, remove_action=False, sync=True)
                    break


        self.clamp_active_index(sync=sync)

    def clear(self, remove_action=False):
        
        action_list = self.get_action_list()
       
        if remove_action:

            actions = self.collect_action_list()

            for action in actions:
                self.remove_action(action, cleanup=True) 


        action_list.clear()



    def duplicate_and_replace_all_slot(self, batch_rename_dict):
        
        action_list = self.get_action_list()

        action_pairs = []


        for slot in action_list:

            action = slot.action 
            action_name = action.name
            new_action = action.copy()

            settings = slot.get_settings_dict()

            if batch_rename_dict is not None:
                mode = batch_rename_dict["mode"]
                stirng_a = batch_rename_dict["string_a"]
                string_b = batch_rename_dict["string_b"]
                new_name = Utility_Function.rename_item(mode, action.name, string_a, string_b) 
                new_action.name = new_name

            action_pairs.append([new_action, settings])

        self.clear(remove_action=False)

        for action_pair in action_pairs:

            action = action_pair[0]
            settings = action_pair[1]

            slot = self.load_action(action)
            slot.use_settings_dict(settings)

    def calculate_slot_range_size(self, slot, use_curve_range=False):

        ranges = self.get_slot_frame_range(slot, use_curve_range=use_curve_range) 

        start = ranges[0]
        end = ranges[1]

        if start is not None and end is not None:
            return Utility_Function.calculate_range_size(start, end)

    def calculate_slot_range_size_by_index(self, index, use_curve_range=False):

        slot = self.get_slot(index)
        ranges = self.get_slot_frame_range(slot, use_curve_range=use_curve_range) 

        start = ranges[0]
        end = ranges[1]

        if start is not None and end is not None:
            return Utility_Function.calculate_range_size(start, end)

    def batch_rename(self, mode, string_a, string_b):
            
        actions = self.collect_action_list()
        Utility_Function.batch_rename(actions, mode, "name", string_a, string_b) 


    def push_to_nla(self, index):
        
        animation_data = self.get_actual_animation_data()
        action = self.get_action(index)

        if animation_data:
            
            track = animation_data.nla_tracks.new()
            strip = track.strips.new(action.name, 0, action)
            track.name = strip.name
            return strip

        else:
            print("Failed to get Animation Data")

    #-----------------

    def clear_all_nla_tracks(self):

        animation_data = self.get_actual_animation_data()

        if animation_data:
            while len(animation_data.nla_tracks) > 0:
                animation_data.nla_tracks.remove(animation_data.nla_tracks[0])

    #-----------------

    def collect_actions_from_nla(self):
        animation_data = self.get_actual_animation_data()
    
        actions = []

        for track in animation_data.nla_tracks:
            for strip in track.strips:
                actions.append(strip.action)

        return actions
        


    def push_all_to_nla(self, selected_only=False ,preclear="NONE"):
        
        strips = []

        action_list = self.get_action_list()

        nla_actions = self.collect_actions_from_nla()
       
        skipped = []
        # ALL / MATCH_TRACK_NAME / MATCH_STRIP_ACTION / EMPTY_MATCH_TRACK / NONE 
        # Remove Empty Track

        if preclear == "ALL":
            self.clear_all_nla_tracks() 



        for index, slot in enumerate(action_list): 

            check = True

            if selected_only:

                if slot.select:
                    check = True
                else:
                    check = False

            if check:
                
                second_check = True 

                if preclear == "PUSH_IF_NON_EXIST":

                    
                    if slot.action in nla_actions:
                        second_check = False

                    
                if second_check: 
                    strip = self.push_to_nla(index)
                else:
                    skipped.append(slot.action)

        return skipped 

    #Pre Clear Setup

    #-----------------

    

    def bake_slot_by_index(self, index, bake_settings, copy, name, replace, use_fake_user=True, update_index=True, move_to_bottom=False):

        f_range = self.get_slot_frame_range_by_index(index, use_curve_range=False)

        start = int(f_range[0])
        end = int(f_range[1])

        # end = int(f_range[1] + 1)
      
        obj = self.obj
        slot = self.get_slot(index)
        settings = slot.get_settings_dict()

        action = slot.action

        target_action = action

        if copy:

            new_action = action.copy()

            if replace:
                replace_action = bpy.data.actions.get(name)

                if replace_action:
                    Utility_Function.replace_action(replace_action, new_action)

            new_action.name = name
            target_action = new_action 


        baked_action = Utility_Function.bake_action(obj, action, target_action, start, end, bake_settings)
        baked_action.use_fake_user = True 

        if copy:
            baked_action.fr_settings.bake_name = ""

        new_slot = self.load_action(baked_action, use_fake_user=use_fake_user, update_index=update_index)

        final_slot = new_slot

        if new_slot is not None:
            new_slot.use_settings_dict(settings) 

            if copy:
                new_slot.select = False

        if copy:
       

            if new_slot is not None:

                if move_to_bottom:

                    final_index = self.get_last_index()
                    self.set_active_index(final_index)
                    final_slot = new_slot

                else:

                    from_index = self.get_last_index()
                    to_index = index + 1
                    self.move_slot_by_index(from_index, to_index, update_index=True, sync=True)
                    final_slot = self.get_slot(index)

            else:

                new_index = self.find_action_index(baked_action) 
                self.set_active_index(new_index)
                final_slot = self.get_slot(new_index)
        else:

            self.set_active_index(index)


        return final_slot 

    def bake_selected(self, bake_settings, batch_rename_dict, copy, replace, use_fake_user=True, update_index=True, move_to_bottom=True, use_bake_name_if_available=True):


        action_list = self.get_action_list()
        
        for slot in action_list:
            slot.bake_temp_bool = slot.select

        for loop in action_list:

            for index, slot in enumerate(action_list):

                if slot.bake_temp_bool:

                    slot.bake_temp_bool = False
                    action = slot.action

                    if action is not None:

                        new_name = self.get_bake_name(action.name, action.fr_settings.bake_name, batch_rename_dict, use_bake_name_if_available=use_bake_name_if_available)
                        slot = self.bake_slot_by_index(index, bake_settings=bake_settings, copy=copy, name=new_name, replace=replace, use_fake_user=use_fake_user, update_index=update_index, move_to_bottom=move_to_bottom)


                        break



    def get_bake_name(self, action_name, bake_name, batch_rename_dict, use_bake_name_if_available=True):


        mode = batch_rename_dict["mode"]
        string_a = batch_rename_dict["string_a"]
        string_b = batch_rename_dict["string_b"]


        new_name = Utility_Function.rename_item(mode, action_name, string_a, string_b) 

        if use_bake_name_if_available:

            if bake_name == "":
                pass

            else:
                new_name = bake_name


        return new_name

    def sort(self, sort_by="NAME", reverse=False):

        action_list = self.get_action_list()

        if sort_by == "NAME": 
            Utility_Function.sort_collection_property_by_name(action_list, "action.name", reverse=reverse)
        if sort_by == "SIZE":
            Utility_Function.sort_collection_property_by_getKey(action_list, sort_getSize, reverse=reverse)




def bake_deform_armature(control_armature, deform_armature, index, bake_settings, name, replace, load):

    f_range = get_slot_frame_range(control_armature, index)
    start = int(f_range[0])
    end = int(f_range[1] + 1)

    slot = get_slot(control_armature, index)
    action = slot.action


    new_action = bpy.data.actions.new("new_action_" + name)
    new_action.frame_start = action.frame_start
    new_action.frame_end = action.frame_end
    new_action.use_frame_range = action.use_frame_range

    if replace:
        replace_action = bpy.data.actions.get(name)
        if replace_action:
            replace_action.user_remap(new_action)
            bpy.data.actions.remove(replace_action)

        new_action.name = name

    target_action = new_action

    baked_action = bake_action(deform_armature, None, target_action, start, end, bake_settings)
    baked_action.use_fake_user = True 

    if load:
        new_slot = load_action(deform_armature, baked_action)
        final_slot = [new_slot, baked_action]
    else:
        final_slot = [None, baked_action] 

    return final_slot 



def offset_action(action, frame, start, end):

    scn = bpy.context.scene
    
    offset = frame - start

    for pose_marker in action.pose_markers:
        pose_marker.frame += int(offset)


    for fc in action.fcurves:

        for kf in fc.keyframe_points:
            kf.co.x += offset
            kf.handle_left[0] += offset
            kf.handle_right[0] += offset

    scn.frame_start += int(offset)
    scn.frame_end += int(offset)







#---------------------------------------

def property_range_limit(source_start, start, source_end, end, mode, limit_zero=True):

    start_value = getattr(source_start, start)
    end_value = getattr(source_end, end)
    

    if mode == "END":

        set_value = end_value - 1

        if start_value > end_value:

            set_value = end_value - 1

            if limit_zero:
                set_value = max(0, set_value)

            setattr(source_start, start, set_value)

    if mode == "START":

        set_value = start_value + 1

        if start_value > end_value:

            set_value = start_value + 1

            if limit_zero:
                set_value = max(0, set_value)
 
            setattr(source_end, end, set_value)
    
#---------------------------------------

def update_frame_range_start(self, context):

    obj = self.id_data
    preferences = Utility_Function.get_addon_preferences()
    index = "ACTIVE"
    property_range_limit(self, "start_frame", self, "end_frame", mode="START")

    sync_scene = preferences.action_list_FR_Update_Active_Action
    sync_frame_range(obj, index, sync_scene=sync_scene, mode="START")

def update_frame_range_end(self, context):

    obj = self.id_data
    preferences = Utility_Function.get_addon_preferences()
    index = "ACTIVE"
    property_range_limit(self, "start_frame", self, "end_frame", mode="END")

    sync_scene = preferences.action_list_FR_Update_Active_Action
    # sync_frame_range(obj, index, sync_scene=sync_scene, mode="END")

def update_frame_range(self, context):

    preferences = Utility_Function.get_addon_preferences()
    
    obj = self.id_data
        
    action_list_helper = Action_List_Helper(obj)
    action_list_helper.sync_active_slot(use_curve_range=False, sync_frame_range_set=True)

    
    # sync_scene = preferences.action_list_FR_Update_Active_Action
    # sync_frame_range(obj, "ACTIVE", sync_scene=sync_scene, mode="ALL", set_obj_active=True)












