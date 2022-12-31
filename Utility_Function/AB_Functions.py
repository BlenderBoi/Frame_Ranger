import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


def index_up():
    context = bpy.context
    scn = bpy.context.scene
    actions = bpy.data.actions

    if len(actions) > 0:
        if scn.AB_Index == 0:
            scn.AB_Index = 0
        if scn.AB_Index > 0:
            scn.AB_Index -= 1
    pass


def add_action(name):
    context = bpy.context
    scn = context.scene
    actions = bpy.data.actions

    new_action = actions.new(name)
    new_action.use_fake_user = True
    
    if new_action is not None:
       
        actions = list(actions)

        if new_action in actions:
            index = list(actions).index(new_action)
            scn.AB_Index = index 

    return new_action

def remove_action(index):

    context = bpy.context
    scn = context.scene
    objects = bpy.data.objects
    actions = bpy.data.actions

    if len(actions) > index:

        action = actions[index]

        for obj in objects:
            OAM = OAM_Functions.get_list(obj)

            for loop in OAM:
                for slot_index, slot in enumerate(OAM):
                    if slot.action == action:
                        OAM_Functions.remove_slot(obj, slot_index)


        actions.remove(action)

        index_up()

def duplicate_action(index, name):

    scn = bpy.context.scene

    Actions = bpy.data.actions
    if len(Actions) > index:
        Action = Actions[index]
        Duplicate_Action = Action.copy()
        Duplicate_Action.name = name
        Duplicate_Action.use_fake_user = True


        if Duplicate_Action is not None:
           
            actions = list(Actions)

            if Duplicate_Action in actions:
                index = list(actions).index(Duplicate_Action)
                scn.AB_Index = index 



        return Duplicate_Action

    return None


def batch_rename_actions(mode, string_a, string_b):
    
    actions = [action for action in bpy.data.actions] 
    Utility_Function.batch_rename(actions, mode, "name", string_a, string_b) 

