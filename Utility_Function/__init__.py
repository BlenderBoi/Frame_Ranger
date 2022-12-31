import bpy
import operator
import os
import addon_utils
import re
from bpy_extras import anim_utils
from Frame_Ranger.Utility_Function import OAM_Functions


def recursive_collect_file_by_format(root_directory, format):

    collected_files = []
    items = os.walk(root_directory)

    for (path, directories, files) in items:
        for file in files:
            if file.endswith("format"):
                collected_files.append(path+"/"+file)

    return collected_files

def get_addon_preferences():
    addon_name = __package__.split(".")[0]
    addon_preferences = bpy.context.preferences.addons[addon_name].preferences 
    return addon_preferences

def draw_subpanel(layout, label, source, property):

    state = getattr(source, property)
    
    if state:
        icon = "TRIA_DOWN"    
    else:
        icon = "TRIA_RIGHT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(source, property, text=label, icon=icon, emboss=False)

    return state 

def update_UI():
    for screen in bpy.data.screens:
        for area in screen.areas:
            area.tag_redraw()

def get_animation_data(obj):

    animation_data = obj.animation_data

    if animation_data:
        return animation_data
    else:
        animation_data = obj.animation_data_create()
        return animation_data

def get_action(obj):

    animation_data = get_animation_data(obj)

    if animation_data:
        return animation_data.action
    
    return None

#-----------------------

def add_prefix(string, prefix):

    return prefix + string

def add_suffix(string, suffix):

    return string + suffix

def batch_rename(items, mode, prop_name, string_a=None, string_b=None):

    for item in items:

        string = getattr(item, prop_name)
        new_string = string 

        if mode == "PREFIX":
            if string_a:
                new_string = add_prefix(string, string_a)

        if mode == "SUFFIX":
            if string_a:
                new_string = add_suffix(string, string_a)

        if mode == "REMOVE":
            if string_a:
                new_string = string.replace(string_a, "")

        if mode == "REPLACE":
            if string_a:
                new_string = string.replace(string_a, string_b)

        setattr(item, prop_name, new_string)


def sort_getKey(item, property_name):
    return operator.attrgetter(property_name)(item)

def sort_collection_property_by_name(collection_property, property_name, reverse=False):

    sorts = sorted(collection_property, key=lambda item: sort_getKey(item, property_name), reverse=reverse)

    for sort_index, sort in enumerate(sorts):
        for item_index, item in enumerate(collection_property):
            if item == sort:
                item.sorter_index = sort_index

    for loop in collection_property:
        for index, item in enumerate(collection_property):

            collection_property.move(index, item.sorter_index)

def sort_collection_property_by_getKey(collection_property, function, reverse=False):

    sorts = sorted(collection_property, key=function, reverse=reverse)

    for sort_index, sort in enumerate(sorts):
        for item_index, item in enumerate(collection_property):
            if item == sort:
                item.sorter_index = sort_index

    for loop in collection_property:
        for index, item in enumerate(collection_property):

            collection_property.move(index, item.sorter_index)

def get_filepath_from_files(files, dirname):

    filepaths = []

    if files:

        for file in files:

            path = os.path.join(dirname, file.name)

            if os.path.exists(path):
                filepaths.append(path)

    return filepaths

def filter_action(filter, filter_mode, action_name):

    show = False 

    if filter_mode == "NONE":
        show = True

    if filter_mode == "INCLUDE":
        if filter == "":
            show = True
        else:
            if filter.lower() in action_name.lower():
                show = True
            else:
                show = False

    if filter_mode == "EXCLUDE":
        if filter == "":
            show = True
        else:
            if not filter.lower() in action_name.lower():
                show = True
            else:
                show = False

    return show

def addon_exists(addon_name):
    return addon_name in bpy.context.preferences.addons


def list_swap_item(items, index_a, index_b):

    if index_a >= 0 and index_b >= 0: 
        if len(items) > index_a and len(items) > index_b:
            item_a = items[index_a]
            item_b = items[index_b]

            items[index_a] = item_b
            items[index_b] = item_a

    return items

def recreate_pose_markers(items, action):

    pose_markers = action.pose_markers
    
    for item in items:
        item.create_pose_marker(action)

#CAMERA -------------------------


def create_Camera(name):
    context = bpy.context

    camera = bpy.data.cameras.new(name)
    camera_obj = bpy.data.objects.new(name, camera)

    context.collection.objects.link(camera_obj)
    return camera_obj



def get_viewport_camera():
    context = bpy.context
    matrix = None

    area = context.area
    if area.type == "VIEW_3D":
        for space in area.spaces:
            if space.type == "VIEW_3D":
                viewport_camera = space.region_3d
    else:

        screen = context.screen

        for area in screen.areas:
            if area.type == "VIEW_3D":

                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        viewport_camera = space.region_3d
                        break
                break

    return [viewport_camera,space]






def view_camera(camera):

    context = bpy.context
    scn = context.scene

    area = context.area
    if area.type == "VIEW_3D":
        for space in area.spaces:
            if space.type == "VIEW_3D":
                scn.camera = camera
                space.region_3d.view_perspective = "CAMERA"

                break
    else:

        screen = context.screen

        for area in screen.areas:
            if area.type == "VIEW_3D":

                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        scn.camera = camera
                        space.region_3d.view_perspective = "CAMERA"

                        break
                break




def create_camera_from_view(name):

    context = bpy.context

    viewport_camera = get_viewport_camera()[0]
    space_data = get_viewport_camera()[1]
    camera = create_Camera(name)

    camera.matrix_world = viewport_camera.view_matrix.inverted()
    camera.data.lens = space_data.lens
    viewport_camera.view_camera_zoom = 0
    viewport_camera.view_camera_offset = (0,0)
    return camera


def bake_action(obj, action, start, end, bake_settings):

    frames = [i for i in range(start, end)]
    obj_act = [[obj, action]]

    only_selected = bake_settings["only_selected"]
    do_pose= bake_settings["do_pose"]
    do_object= bake_settings["do_object"]
    do_visual_keying= bake_settings["do_visual_keying"]
    do_constraint_clear= bake_settings["do_constraint_clear"]
    do_parents_clear= bake_settings["do_parents_clear"]
    do_clean= bake_settings["do_clean"]


    baked_actions = anim_utils.bake_action_objects(
        obj_act,
        frames=frames,
        only_selected=only_selected,
        do_pose=do_pose,
        do_object=do_object,
        do_visual_keying=do_visual_keying,
        do_constraint_clear=do_constraint_clear,
        do_parents_clear=do_parents_clear,
        do_clean=do_clean,
    )
    
    baked_action = baked_actions[0]

    return baked_action
    


def set_renamer(mode, string, string_a=None, string_b=None):

    new_string = string 

    if mode == "PREFIX":
        if string_a:
            new_string = add_prefix(string, string_a)

    if mode == "SUFFIX":
        if string_a:
            new_string = add_suffix(string, string_a)

    if mode == "REMOVE":
        if string_a:
            new_string = string.replace(string_a, "")

    if mode == "REPLACE":
        if string_a:
            new_string = string.replace(string_a, string_b)

    return new_string



    

def rename_item(mode, string, string_a=None, string_b=None):

    new_string = string 

    if mode == "PREFIX":
        if string_a:
            new_string = add_prefix(string, string_a)

    if mode == "SUFFIX":
        if string_a:
            new_string = add_suffix(string, string_a)

    if mode == "REMOVE":
        if string_a:
            new_string = string.replace(string_a, "")

    if mode == "REPLACE":
        if string_a:
            new_string = string.replace(string_a, string_b)

    return new_string






def calculate_range_size(start, end):
    return end - start 


def get_object(self):

    obj = bpy.data.objects.get(self.target_object)
    return obj



def filter_items(self, context, data, propname, filter_prop):

    filtered = []
    ordered = []
    items = getattr(data, propname)

    filtered = [self.bitflag_filter_item] * len(items)

    for i, item in enumerate(items):
        if not self.filter_name == "":
            if not self.filter_name in operator.attrgetter(filter_prop)(item):
                filtered[i] &= ~self.bitflag_filter_item

    return filtered, ordered

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def draw_show_pose_markers(context, layout):

    if context.area.ui_type == "DOPESHEET":
        if context.space_data.ui_mode == "ACTION":
            layout.prop(context.space_data, "show_pose_markers")



def bake_action(obj, action, target_action, start, end, bake_settings):

    animation_data = get_animation_data(obj)

    if animation_data:
        animation_data.action = action



    frames = [i for i in range(start, end)]

    obj_act = [[obj, target_action]]

    only_selected = bake_settings["only_selected"]
    do_pose= bake_settings["do_pose"]
    do_object= bake_settings["do_object"]
    do_visual_keying= bake_settings["do_visual_keying"]
    do_constraint_clear= bake_settings["do_constraint_clear"]
    do_parents_clear= bake_settings["do_parents_clear"]
    do_clean= bake_settings["do_clean"]


    baked_actions = anim_utils.bake_action_objects(
        obj_act,
        frames=frames,
        only_selected=only_selected,
        do_pose=do_pose,
        do_object=do_object,
        do_visual_keying=do_visual_keying,
        do_constraint_clear=do_constraint_clear,
        do_parents_clear=do_parents_clear,
        do_clean=do_clean,
    )
    
    baked_action = baked_actions[0]

    return baked_action
  


def replace_action(action, new_action):

    action.user_remap(new_action)
    bpy.data.actions.remove(action)


class Duplicates_Renamer:
    
    def __init__(self):
        self.original_name = None
        self.base_name = None
        self.suffix = None
        
        self.final_name = None

    def parse_name(self, name):
        
        pattern = re.compile(r'(.)(\.\d+$)')
        
        self.original_name = name
        self.base_name = pattern.sub(r'\1', self.original_name)
        self.suffix_number = pattern.sub(r'\2', self.original_name)

    def get_number_suffix(self, count, padding=3, separator="."):
        padded_number = str(count).zfill(padding)
        number_suffix = separator + str(padded_number)
        return number_suffix

    def check_number(self, count, list):
        
        number_suffix = self.get_number_suffix(count)
        
        final_name = self.base_name + number_suffix
        
        if final_name in list:
            self.check_number(count+1, list)
            
        else:
            self.final_name = final_name
            
            
    def check_and_rename_duplicates(self, name, list):
        
        self.parse_name(name)
        
        if name in list:
            self.check_number(1, list)
            return self.final_name
        
        else:
            return name
    
        return name


def remove_action_from_file(action, cleanup=True):

    if action is not None:
        bpy.data.actions.remove(action)

    if cleanup:
        for obj in bpy.data.objects:
            action_list_helper = OAM_Functions.Action_List_Helper(obj) 
            action_list_helper.cleanup()

def mid_point(value1, value2):

    return (value1+value2)/2



