
import bpy
from . import Add_Action_Slot
from . import Remove_Action_Slot
from . import Reorder_Action_Slot
from . import Select_Action_Slot_Object
from . import Set_Active_Slot
from . import Duplicate_Action_Slot
from . import Play_Action_Slot
from . import Bake_Action
from . import Push_To_NLA
from . import Load_Action_Slot
from . import Duplicate_And_Replace_All_Slot
from . import On_Auto_Frame_Range

modules = [On_Auto_Frame_Range, Duplicate_And_Replace_All_Slot, Load_Action_Slot, Push_To_NLA, Bake_Action, Play_Action_Slot, Duplicate_Action_Slot, Set_Active_Slot, Select_Action_Slot_Object, Add_Action_Slot, Remove_Action_Slot, Reorder_Action_Slot]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
