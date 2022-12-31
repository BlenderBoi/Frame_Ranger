import bpy
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger import Utility_Function

import itertools
import json

MENU_ACTION = None
MENU_OBJ = None



def default_name(action):

    default_name = "PoseMarker"

    if action: 
        name = "{}_{}".format(default_name, len(action.pose_markers))
        return name
    
    return None

def use_frame(frame):
    if frame:
        return frame
    else:
        return bpy.context.scene.frame_current

def use_name(name, action):

    if action:
        if name:
            return name
        else:
            return default_name(action)

    return None

def get_index(action):
    
    if action:
        index = action.pose_markers_index
        return index

    return None

def add_pose_marker(action, name=None, frame=None):
  
    if action:
        frame = use_frame(frame)
        name = use_name(name, action)

        if name and frame is not None:

            marker = action.pose_markers.new(name)
            
            if marker:
                marker.frame = frame
                action.pose_markers_index = len(action.pose_markers) - 1
                return marker



    return None

def check_index(index, action):

    if action: 
        if len(action.pose_markers) > index:
            return True

    return False

def check_not_empty(action):

    if action:
        if len(action.pose_markers) == 0:
            return False 
        else:
            return True 
   
    return None


def get_max(action):

    if action:
        return len(action.pose_markers)
    
    return None

def get_last_index(action):

    if action:
        return get_max(action) - 1

    return None

def index_up(action):

    if action.pose_markers_index == 0:
        action.pose_markers_index = 0
    if action.pose_markers_index > 0:
        action.pose_markers_index -= 1

def index_down(action):

    new_index = action.pose_markers_index + 1

    if check_index(new_index, action):
        action.pose_markers_index = new_index

def index_bottom(action):
    
    if check_not_empty(action):
        action.pose_markers_index = get_last_index(action) 

def remove_pose_marker(index, action):

    if action: 
        markers = action.pose_markers

        if check_index(index, action):
            markers.remove(markers[index]) 
            index_up(action)

def get_pose_marker_by_index(index, action):

    if action: 
        if check_index(index, action): 
            marker = action.pose_markers[index]

            return marker
    
    return None

def get_active_pose_marker(action):
     
    active_index = get_index(action) 
   
    if active_index:
        return get_pose_marker_by_index(active_index, action)

    return None

def move_frame_to_pose_marker(marker, view):

    if marker:
        bpy.context.scene.frame_current = marker.frame

        # type = ["TIMELINE", "DOPESHEET", "FCURVES"]
        type = ["SEQUENCE_EDITOR", "NLA_EDITOR","DOPESHEET_EDITOR", "GRAPH_EDITOR"]

        if view:
            # if bpy.context.area.ui_type in type:
            #     bpy.ops.action.view_frame()
            #
            # if bpy.context.area.ui_type == "SEQUENCE_EDITOR":
            #     bpy.ops.sequencer.view_frame()

            for area in bpy.context.screen.areas:
                if area.type in type:
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            ctx = bpy.context.copy()
                            ctx['area'] = area
                            ctx['region'] = region

                            if area.type == "NLA_EDITOR":
                                bpy.ops.nla.view_frame(ctx)

                            if area.type == "SEQUENCE_EDITOR":
                                bpy.ops.sequencer.view_frame(ctx)

                            if area.type == "GRAPH_EDITOR":
                                bpy.ops.graph.view_frame(ctx)

                            if area.type == "DOPESHEET_EDITOR":
                                bpy.ops.action.view_frame(ctx)


                            # else:
                            #     bpy.ops.action.view_frame(ctx)



def move_frame_to_pose_marker_by_index(index, action, view):

    if action: 

        marker = get_pose_marker_by_index(index, action)

        if marker:
            return move_frame_to_pose_marker(marker, view)

def clear_pose_markers(action):

    if action: 
        markers = action.pose_markers

        while get_max(action) > 0:
            remove_pose_marker(0, action) 

def batch_rename_pose_markers(action, mode, string_a, string_b, check_select):

    if action: 

        if check_select:
            items = [marker for marker in action.pose_markers if marker.select]
        else:
            items = action.pose_markers

        prop_name = "name"

        Utility_Function.batch_rename(items, mode, prop_name, string_a, string_b) 


class Proto_Marker:

    def __init__(self, marker, type):

        self.select = marker.select
        self.name = marker.name
        self.frame = marker.frame
        self.camera = marker.camera
        self.type = type
        self.notes = marker.notes
        
    def create_marker(self, source):
        marker = source.new(self.name)
        marker.frame= self.frame
        marker.select = self.select
        marker.camera = self.camera
        marker.notes = self.notes

    def create_timeline_marker(self, scene):
        marker = scene.timeline_markers.new(self.name)
        marker.frame= self.frame
        marker.select = self.select
        marker.camera = self.camera
        marker.notes = self.notes

    def create_pose_marker(self, action):
        marker = action.pose_markers.new(self.name)
        marker.frame = self.frame
        marker.select = self.select
        marker.camera = self.camera
        marker.notes = self.notes
        bpy.context.view_layer.update()
        
        
def collect_marker_data(marker, type="POSEMARKER"):

    if marker:
        proto_marker = Proto_Marker(marker, type)
        return proto_marker


def recreate_pose_markers(items, action):

    pose_markers = action.pose_markers
    
    for item in items:
        item.create_pose_marker(action)

    bpy.context.view_layer.update()


def remove_overlapped_markers(action):
    

    context = bpy.context
    scn = context.scene
    markers = action.pose_markers

    if len(markers) > 0:
        counter = 0
        for marker in markers:
            isDuplicate =False

            for marker_check in markers:

                if marker.name == marker_check.name:
                    if marker.frame == marker_check.frame:
                        if isDuplicate == False:
                            isDuplicate=True
                        else:
                            counter += 1
                            markers.remove(marker_check)



#----IO Markers

def encode_Marker(marker):

    if marker.camera:
        camera = marker.camera.name
    else:
        camera = None

    return {"Name": marker.name, "Frame": marker.frame, "Selection": marker.select, "Camera" : camera, "Notes" : marker.notes}

def write_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def read_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
        return data

def export_markers(filepath, markers):

    Encoded_Markers = []

    if len(markers) > 0:
        for marker in markers:

            Encoded_Markers.append(encode_Marker(marker))


        write_json(filepath, Encoded_Markers)

def import_markers(action, filepath, find_bind):


    markers = action.pose_markers

    Import_Markers = read_json(filepath)

    missing_camera = []

    for marker in Import_Markers:
        New_Marker = add_pose_marker(action, name=marker["Name"], frame=marker["Frame"])
        New_Marker.notes = marker["Notes"]

        if find_bind:

            if marker["Camera"]:
                if bpy.context.scene.objects.get(marker["Camera"]):
                    New_Marker.camera = bpy.context.scene.objects.get(marker["Camera"])
                else:
                    missing_camera.append(marker["Camera"])

        New_Marker.select = marker["Selection"]

    return missing_camera




def find_and_set_range_markers(action, find_mode, find_a, marker_a_find, find_b, marker_b_find):

    marker_a = None
    marker_b = None

    if action is not None:

        if find_a:

            for marker in action.pose_markers:


                if find_mode == "SUFFIX":

                    if marker.name.lower().endswith(marker_a_find.lower()):
                        marker_a = marker
                        break

                if find_mode == "PREFIX":

                    if marker.name.lower().startswith(marker_a_find.lower()):
                        marker_a = marker
                        break


                if find_mode == "INCLUDE":

                    if marker_a_find.lower() in marker.name.lower():
                            marker_a = marker
                            break



        if find_b:

            for marker in action.pose_markers:

                if find_mode == "SUFFIX":


                    if marker.name.lower().endswith(marker_b_find.lower()):
                        marker_b = marker
                        break

                if find_mode == "PREFIX":


                    if marker.name.lower().startswith(marker_b_find.lower()):
                        marker_b = marker
                        break

                if find_mode == "INCLUDE":


                    if marker_b_find.lower() in marker.name.lower():
                        marker_b = marker
                        break


    if marker_a is not None:
        action.fr_settings.use_pose_marker_as_range = True
        action.fr_settings.pose_marker_a = marker_a.name

    if marker_b is not None:
        action.fr_settings.use_pose_marker_as_range = True
        action.fr_settings.pose_marker_b = marker_b.name

    return [marker_a, marker_b]

