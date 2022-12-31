
import bpy

def RemapKeyframe(old, new, subframe):

    rate = old/new

    for action in bpy.data.actions:

        for fc in action.fcurves:
            for kf in fc.keyframe_points:

                if subframe:
                    kf.co.x = int(kf.co.x / rate)
                    kf.handle_left[0] = int(kf.handle_left[0] / rate)
                    kf.handle_right[0] = int(kf.handle_right [0] / rate)
                else:
                    kf.co.x = kf.co.x / rate
                    kf.handle_left[0] = kf.handle_left[0] / rate
                    kf.handle_right[0] = kf.handle_right [0] / rate

def RemapTimelineMarker(old, new, subframe):

    rate = old/new

    for scene in bpy.data.scenes:
        for tm in scene.timeline_markers:
            if subframe:
                tm.frame = int(tm.frame / rate)
            else:
                tm.frame = int(tm.frame / rate)

def RemapPoseMarker(old, new, subframe):
    
    rate = old/new

    for action in bpy.data.actions:
    
        for pm in action.pose_markers:
            if subframe:
                pm.frame = int(pm.frame / rate)
            else:
                pm.frame = int(pm.frame / rate)


def RemapManualFrameRange(old, new, subframe):
    
    rate = old/new

    for action in bpy.data.actions:
    
        if subframe:
            action.frame_start = int(action.frame_start / rate)
            action.frame_end = int(action.frame_end / rate)
        else:
            action.frame_start = int(action.frame_start / rate)
            action.frame_end = int(action.frame_end / rate)



def RemapFrameRange(context, old, new, subframe):

    rate = old/new
    if subframe:
        context.scene.frame_end = int(context.scene.frame_end / rate)
        context.scene.frame_start = int(context.scene.frame_start / rate)
    else:
        context.scene.frame_end =int(context.scene.frame_end / rate)
        context.scene.frame_start = int(context.scene.frame_start / rate)


def Nudge_Keyframe():

    for action in bpy.data.actions:

        for fc in action.fcurves:
            for kf in fc.keyframe_points:

                    kf.co.x = int(kf.co.x)
                    kf.handle_left[0] = int(kf.handle_left[0])
                    kf.handle_right[0] = int(kf.handle_right [0])


def Nudge_TimelineMarker():

    for scene in bpy.data.scenes:
        for tm in scene.timeline_markers:

            tm.frame = int(tm.frame)




def RemapFrameRangeManager(all, context, old, new, subframe):

    scn = context.scene
    rate = old/new
    FRM_Set = scn.FRM_Set


    current_frame_range_start = context.scene.frame_start
    current_frame_range_end = context.scene.frame_end

    if all:
        for Set in FRM_Set:
            for FR in Set.FRM:
                if subframe:
                    FR.End = int(FR.End / rate)
                    FR.Start = int(FR.Start / rate)
                else:
                    FR.End = int(FR.End / rate)
                    FR.Start = int(FR.Start / rate)
    else:
        if len(FRM_Set) > 0:
            Active_Set = FRM_Set[scn.FRM_Set_Index]
            for FR in Active_Set.FRM:
                if subframe:
                    FR.End = int(FR.End / rate)
                    FR.Start = int(FR.Start / rate)
                else:
                    FR.End = int(FR.End / rate)
                    FR.Start = int(FR.Start / rate)

    context.scene.frame_start = current_frame_range_start
    context.scene.frame_end = current_frame_range_end
