import bpy
import itertools
import json
from Frame_Ranger import Utility_Function

def get_set_index():
    scn = bpy.context.scene
    return scn.FRM_Set_Index

def get_set_list():
    scn = bpy.context.scene
    return scn.FRM_Set

def get_set_size():

    set_list = get_set_list()
    return len(set_list)

def get_set_last():

    set_list = get_set_list()
    return len(set_list) - 1

def set_move_up():

    set_list = get_set_list()

    index = get_set_index()
    
    if index > 0:
        set_list.move(index, index-1)
        set_active_set(index-1)    

def set_move_down():

    set_list = get_set_list()

    index = get_set_index()
    
    if get_set_last() > index:
        set_list.move(index, index+1)
        set_active_set(index+1)    

def check_set_index(index):

    if index >= 0:
        if get_set_size() > index:
            return True 

    return False 
    
def get_set(index):

    set_list = get_set_list()
    
    if check_set_index(index):
        set = set_list[index]
        return set 

    return None

def get_active_set():

    active_index = get_set_index()
    active_set = get_set(active_index)
        
    return active_set 

def set_active_set(index):
    
    scn = bpy.context.scene

    if check_set_index(index):
        scn.FRM_Set_Index = index

def get_set_fr(index):
    
    set = get_set(index)
    if set:
        return set.FRM


def clear_set():
    
    set_list = get_set_list()
    while len(set_list) > 0:
        remove_set(0)

def clear_empty_set():
    
    set_list = get_set_list()
        
    for loop in set_list:
        for index, set in enumerate(set_list):
            if len(set.FRM) == 0:
                remove_set(index)

def sort_set(reverse):

    Utility_Function.sort_collection_property_by_name(get_set_list(), "name", reverse=reverse)



def batch_rename_set(mode, string_a, string_b):
    
    set_list = get_set_list()
    Utility_Function.batch_rename(set_list, mode, "name", string_a, string_b) 



#-------------------------------------------

def get_fr_list():
    
    active_set = get_active_set()
    return active_set.FRM

def get_fr_index():

    active_set = get_active_set()
    active_index = active_set.FRM_Index
    return active_index


def get_fr_size():

    set_fr = get_fr_list()
    return len(set_fr)

def get_fr_last():

    set_fr = get_fr_list()
    return len(set_fr) - 1

def check_fr_index(index):
    
    if index >= 0:
        if get_fr_size() > index:
            return True

    return False


def get_fr(index):

    fr_list = get_fr_list()

    if check_fr_index(index):
        fr = fr_list[index]
        return fr

    return None 

def get_active_fr():
    
    active_index = get_fr_index()
    return get_fr(active_index)    

def set_active_fr(index):

    if check_fr_index(index):
        active_set = get_active_set()
        active_set.FRM_Index = index



def fr_move_up():

    fr_list = get_fr_list()

    index = get_fr_index()
    
    if index > 0:
        fr_list.move(index, index-1)
        set_active_fr(index-1)    

def fr_move_down():

    fr_list = get_fr_list()

    index = get_fr_index()
    
    if get_fr_last() > index:
        fr_list.move(index, index+1)
        set_active_fr(index+1)    





#-------

def add_set(name):
    set_list = get_set_list()

    new_set = set_list.add()
    new_set.name = name
    
    last_index = get_set_last()
    set_active_set(last_index)

    return new_set


def set_index_up():

    if get_set_size() > 0:
        if get_set_index() == 0:
            set_active_set(0)

        if get_set_index() > 0:
            set_active_set(get_set_index() - 1)

def set_index_last():
   
    set_active_set(get_set_last())

def remove_set(index):
    set_list = get_set_list() 

    if check_set_index(index):
        set_list.remove(index)

        if index <= get_set_index():
            set_index_up() 

#-----------------



def fr_index_up():

    if get_fr_size() > 0:
        if get_fr_index() == 0:
            set_active_fr(0)

        if get_fr_index() > 0:
            set_active_fr(get_fr_index() - 1)

def fr_index_last():
   
    set_active_fr(get_fr_last())


def add_fr(name, start, end):

    fr_list = get_fr_list()


    fr = fr_list.add()
    fr.name = name
    fr.Start = start
    fr.End = end

    fr_index_last()

    return fr

def remove_fr(index):
    
    fr_list = get_fr_list()

    if check_fr_index(index):
        fr_list.remove(index)        


        if index <= get_fr_index():
            fr_index_up() 
    # fr_index_last()


def clear_fr():
    
    fr_list = get_fr_list()

    while len(fr_list) > 0:
        remove_fr(0)


def calculate_range_size(start, end):
    return end - start 


def sort_getSize(item):

    return Utility_Function.calculate_range_size(item.Start, item.End)



def sort_fr(mode, reverse):

    if mode == "NAME":
        Utility_Function.sort_collection_property_by_name(get_fr_list(), "name", reverse=reverse)

    if mode == "SIZE":
        Utility_Function.sort_collection_property_by_getKey(get_fr_list(), sort_getSize, reverse=reverse)

def batch_rename_fr(mode, string_a, string_b):
   
    set_list = get_fr_list()
    Utility_Function.batch_rename(set_list, mode, "name", string_a, string_b) 

def set_frame_range(index):
    fr = get_fr(index)
    scn = bpy.context.scene

    scn.frame_start = fr.Start
    scn.frame_end = fr.End


#--------------------------------------

def remove_suffix(string, suffix):

    if string.endswith(suffix):

        return string[:-len(suffix)]

    else:
        return string


def remove_prefix(string, prefix):

    if string.startswith(prefix):

        return string[len(prefix):]

    else:
        return string

def sort_get_item_names(item):
    return item.name


def sort_get_item_frames(item):
    return item.frame


def get_filter_items(items, mode, filter):

    if mode == "PREFIX":
        filtered_item = [item for item in items if item.name.startswith(filter)]


    if mode == "SUFFIX":
        filtered_item = [item for item in items if item.name.endswith(filter)]


    if mode == "PAIR":
        pass


    return filtered_item


def get_marker_pairs(mode, filter_start, filter_end):

    scn = bpy.context.scene
    markers = scn.timeline_markers



    if mode == "PAIR":
        filter_start = ""
        filter_end = ""

    if filter_start == "" or filter_end == "":

        if filter_start == "":
            filter_start = filter_end
        if filter_end == "":
            filter_end = filter_start

        marker_groups = [list(g) for k, g in itertools.groupby(sorted(markers, key=sort_get_item_names), sort_get_item_names)]
        marker_pairs = []

        for group in marker_groups:

            Start = True
            New_Pair = []

            group.sort(key=sort_get_item_frames)

            for pair in group:
                New_Pair.append(pair)

                if Start == False:
                    New_Pair.append(pair.name)
                    marker_pairs.append(New_Pair)

                    New_Pair = []

                Start = not Start

    else:


        start_filter_group = get_filter_items(markers, mode, filter_start)
        end_filter_group = get_filter_items(markers, mode, filter_end)

        marker_pairs = []

        start_filter_group.sort(key=sort_get_item_frames)
        end_filter_group.sort(key=sort_get_item_frames)


        for start_marker in start_filter_group:

            for end_marker in end_filter_group:

                if not start_marker == end_marker:

                    if not start_marker.frame == end_marker.frame:

                        if not start_marker.frame > end_marker.frame:


                            if mode == "PREFIX":

                                start_basename = remove_prefix(start_marker.name, filter_start)
                                end_basename = remove_prefix(end_marker.name, filter_end)

                            if mode == "SUFFIX":
                                start_basename = remove_suffix(start_marker.name, filter_start)
                                end_basename = remove_suffix(end_marker.name, filter_end)


                            if start_basename == end_basename:

                                marker_pairs.append([start_marker, end_marker, start_basename])
                                end_filter_group.remove(end_marker)
                                break


    return marker_pairs





def encode_Frame_Range(FR):
    return {"Name": FR.name, "Start": FR.Start, "End": FR.End}

def write_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def read_json(filepath):

    with open(filepath) as f:
        data = json.load(f)
        return data

def export_frm(filepath, fr_list):

    frame_ranges = []
    for fr in fr_list:
        frame_ranges.append(encode_Frame_Range(fr))

    write_json(filepath, frame_ranges)


def import_frm(filepath):


    frame_ranges = read_json(filepath)

    for fr in frame_ranges:

        add_fr(fr["Name"], fr["Start"], fr["End"])





def markers_from_frame_range(mode, pair_extension_start, pair_extension_end):

    fr_list = get_fr_list()
    scn = bpy.context.scene

    markers = []

    for FR in fr_list:
        if mode == "PAIR":
            start_name = FR.name
            end_name = FR.name

        if mode == "SUFFIX":
            start_name = FR.name + pair_extension_start
            end_name = FR.name + pair_extension_end

        if mode == "PREFIX":
            start_name =  pair_extension_start + FR.name
            end_name = pair_extension_end + FR.name

        start_marker = scn.timeline_markers.new(start_name, frame=FR.Start)
        end_marker = scn.timeline_markers.new(end_name, frame=FR.End)
        markers.append(start_marker)
        markers.append(end_marker)

    return markers

def frame_ranges_from_markers(mode, pair_extension_start, pair_extension_end):

    marker_pairs = get_marker_pairs(mode, pair_extension_start, pair_extension_end)
    
    frame_ranges = []

    for pair in marker_pairs:
        fr = add_fr(pair[2], pair[0].frame, pair[1].frame)
    
        frame_ranges.append(fr)


    return frame_ranges
