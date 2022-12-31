import bpy
from Frame_Ranger import Utility_Function

import itertools
import json

def use_frame(frame):
    if frame == None:
        return bpy.context.scene.frame_current
    else:
        return frame

def get_index(scn):
    
    if scn:
        index = scn.timeline_markers_index
        return index

    return None

def add_timeline_marker(scn, name=None, frame=None):
  
    if scn:
        frame = use_frame(frame)

        if name and frame is not None:

            marker = scn.timeline_markers.new(name)
            
            if marker:
                marker.frame = frame
                scn.timeline_markers_index = len(scn.timeline_markers) - 1
                return marker

    return None

def check_index(index, scn):

    if scn: 
        if len(scn.timeline_markers) > index:
            return True

    return False

def check_not_empty(scn):

    if scn:
        if len(scn.timeline_markers) == 0:
            return False 
        else:
            return True 
   
    return None


def get_max(scn):

    if scn:
        return len(scn.timeline_markers)
    
    return None

def get_last_index(scn):

    if scn:
        return get_max(scn) - 1

    return None

def index_up(scn):

    if scn.timeline_markers_index == 0:
        scn.timeline_markers_index = 0
    if scn.timeline_markers_index > 0:
        scn.timeline_markers_index -= 1

def index_down(scn):

    new_index = scn.timeline_markers_index + 1

    if check_index(new_index, scn):
        scn.timeline_markers_index = new_index

def index_bottom(scn):
    
    if check_not_empty(scn):
        scn.timeline_markers_index = get_last_index(scn) 

def remove_timeline_marker(index, scn):

    if scn: 
        markers = scn.timeline_markers

        if check_index(index, scn):
            markers.remove(markers[index]) 
            index_up(scn)

def get_timeline_marker_by_index(index, scn):

    if scn: 
        if check_index(index, scn): 
            marker = scn.timeline_markers[index]

            return marker
    
    return None

def get_active_timeline_marker(scn):
     
    active_index = get_index(scn) 
   
    if active_index:
        return get_timeline_marker_by_index(active_index, scn)

    return None

def move_frame_to_timeline_marker(marker, view):

    if marker:
        bpy.context.scene.frame_current = marker.frame

        type = ["SEQUENCE_EDITOR", "NLA_EDITOR","DOPESHEET_EDITOR", "GRAPH_EDITOR"]

        if view:

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

















def move_frame_to_timeline_marker_by_index(index, scn, view):

    if scn: 

        marker = get_timeline_marker_by_index(index, scn)

        if marker:
            return move_frame_to_timeline_marker(marker, view)

def clear_timeline_markers(scn):

    if scn: 
        markers = scn.timeline_markers

        while get_max(scn) > 0:
            remove_timeline_marker(0, scn) 

def batch_rename_timeline_markers(scn, mode, string_a, string_b, check_select):

    if scn: 

        if check_select:
            items = [marker for marker in scn.timeline_markers if marker.select]
        else:
            items = scn.timeline_markers

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
        marker.frame = self.frame
        marker.select = self.select
        marker.camera = self.camera
        marker.notes = self.notes

    def create_timeline_marker(self, scene):
        marker = scene.timeline_markers.new(self.name)
        marker.frame = self.frame
        marker.select = self.select
        marker.camera = self.camera
        marker.notes = self.notes

    def create_pose_marker(self, action):
        marker = action.pose_markers.new(self.name)
        marker.frame = self.frame
        marker.select = self.select
        marker.camera = self.camera
        marker.notes = self.notes
        
        
def collect_marker_data(marker, type="TIMELINEMARKER"):

    if marker:
        proto_marker = Proto_Marker(marker, type)
        return proto_marker



def recreate_timeline_markers(items, scn):

    timeline_markers = scn.timeline_markers
    
    for item in items:
        item.create_timeline_marker(scn)


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

def import_markers(filepath, find_bind):

    scn = bpy.context.scene

    markers = scn.timeline_markers

    Import_Markers = read_json(filepath)

    missing_camera = []

    for marker in Import_Markers:
        New_Marker = add_timeline_marker(scn, name=marker["Name"], frame=marker["Frame"])
        New_Marker.notes = marker["Notes"]

        if find_bind:

            if marker["Camera"]:
                if bpy.context.scene.objects.get(marker["Camera"]):
                    New_Marker.camera = bpy.context.scene.objects.get(marker["Camera"])
                else:
                    missing_camera.append(marker["Camera"])

        New_Marker.select = marker["Selection"]

    return missing_camera

def remove_overlapped_markers():

    context = bpy.context
    scn = context.scene
    markers = scn.timeline_markers

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


