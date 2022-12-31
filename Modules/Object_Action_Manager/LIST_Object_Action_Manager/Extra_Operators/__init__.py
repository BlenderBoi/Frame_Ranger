
import bpy

from . import Batch_Rename_Object_Actions
from . import Set_Fake_User
from . import Sort_Action_Slot
from . import Clear_Action_Slot
from . import Clean_Action_List
from . import Load_All_Action
from . import Import_FBX_Action
from . import Append_BlendFile_Action
from . import Remove_By_Condition
from . import Push_All_To_NLA
from . import Bake_Selected_Action
from . import Find_And_Set_All_Actions_Range_Marker
from . import Recursive_Import_FBX_Action

# modules = [Bake_Selected_Action, Push_To_NLA, Remove_By_Condition, Append_BlendFile_Action, Import_FBX_Action, Clean_Action_List, Load_All_Action, Clear_Action_Slot, Sort_Action_Slot, Batch_Rename_Object_Actions, Set_Fake_User]
# modules = [Bake_Selected_Action, Remove_By_Condition, Append_BlendFile_Action, Import_FBX_Action, Clean_Action_List, Load_All_Action, Clear_Action_Slot, Sort_Action_Slot, Batch_Rename_Object_Actions, Set_Fake_User]

modules = [
    Append_BlendFile_Action,
    Import_FBX_Action,
    Bake_Selected_Action, 
    Load_All_Action, 
    Push_All_To_NLA, 
    Set_Fake_User, 
    Batch_Rename_Object_Actions, 
    Clear_Action_Slot, 
    Sort_Action_Slot, 
    Clean_Action_List, 
    Remove_By_Condition,
    Find_And_Set_All_Actions_Range_Marker,
    Recursive_Import_FBX_Action,
]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
