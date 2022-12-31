
import bpy
from . import Clear_Actions
from . import Batch_Rename_Actions
from . import Toogle_Fake_Users
from . import Remove_Zero_User

modules = [Remove_Zero_User, Toogle_Fake_Users, Batch_Rename_Actions, Clear_Actions]


def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
