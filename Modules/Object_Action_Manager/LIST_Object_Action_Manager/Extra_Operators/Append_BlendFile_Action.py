

import bpy
from Frame_Ranger import Utility_Function
from bpy.props import EnumProperty
from Frame_Ranger.Utility_Function import OAM_Functions
import os


ENUM_filter_mode = [("INCLUDE","Include","Include"),("EXCLUDE","Exclude","Exclude")]


class FR_OT_OAM_Append_This_Action(bpy.types.Operator):
    """Append This Action"""
    bl_idname = "fr_oam.append_this_action"
    bl_label = "Append This"
    bl_options = {'UNDO', 'REGISTER'}

    filepath: bpy.props.StringProperty()
    filename: bpy.props.StringProperty()
    action: bpy.props.StringProperty()

    load_to_object: bpy.props.BoolProperty()

    target_object: bpy.props.StringProperty()

    def execute(self, context):
        
        obj = bpy.data.objects.get(self.target_object) 

        directory=self.filepath + "/Action"
        filename = self.action
        filepath = self.filename

        current_actions = [action for action in bpy.data.actions]

        bpy.ops.wm.append(filename=filename, filepath=filepath, directory=directory)

        appended_action = None 

        for action in bpy.data.actions:
            if not action in current_actions: 
                appended_action = action
                break 


        if appended_action:
            if self.load_to_object:

                action_list_helper = OAM_Functions.Action_List_Helper(obj)
                action_list_helper.load_action(appended_action, use_fake_user=True, update_index=True, sync=True)

            
            appended_action.use_fake_user = True
            scn = context.scene
            scn.AB_Index = len(bpy.data.actions) - 1

        Utility_Function.update_UI()
        return {"FINISHED"}


class FR_OT_OAM_Append_All_Actions(bpy.types.Operator):
    """Append All Action"""
    bl_idname = "fr_oam.append_all_actions"
    bl_label = "Append All Actions"
    bl_options = {'UNDO', 'REGISTER'}
    
    filepath: bpy.props.StringProperty()

    filter: bpy.props.StringProperty()
    filter_mode: bpy.props.EnumProperty(items=ENUM_filter_mode)
    use_filter: bpy.props.BoolProperty()

    load_to_object: bpy.props.BoolProperty()

    target_object: bpy.props.StringProperty()

    def invoke(self, context, event):

        if self.filepath == bpy.data.filepath:

            self.report({"INFO"}, "Cannot Append From Self")

            
            return {'FINISHED'}
        
        else:

            return self.execute(context)

    



    def execute(self, context):

        scn = context.scene


        obj = bpy.data.objects.get(self.target_object) 



        blend_file = self.filepath
        current_actions = [action for action in bpy.data.actions]

        # Imported_Actions_Name = []

        with bpy.data.libraries.load(blend_file) as (data_from, data_to):

            # data_to.actions = data_from.actions

            for action in data_from.actions:

                if self.use_filter:
                    show = Utility_Function.filter_action(self.filter, self.filter_mode, action)
                else:
                    show = True

                if show:
                    data_to.actions.append(action)
                    # Imported_Actions_Name.append(action)

        Imported_Actions = [action for action in bpy.data.actions if action not in current_actions]
        
        for action in Imported_Actions:

            action.use_fake_user = True
            scn.AB_Index = len(bpy.data.actions) - 1

            if self.load_to_object:

                action_list_helper = OAM_Functions.Action_List_Helper(obj)
                action_list_helper.load_action(action, use_fake_user=True, update_index=True, sync=True)

        Utility_Function.update_UI()
        #
        return {'FINISHED'}




def update_filter_clear(self, context):

    if self.filter_clear== True:
        self.filter_clear= False 
        self.filter = ""


class FR_OT_OAM_Append_Action_List(bpy.types.Operator):
    """Append Action List"""
    bl_idname = "fr_oam.append_action_list"
    bl_label = "Append Action List"

    bl_options = {'UNDO', 'REGISTER'}

    filepath: bpy.props.StringProperty()
    filename: bpy.props.StringProperty()
   
    filter_clear: bpy.props.BoolProperty(default=False, update=update_filter_clear)

    filter: bpy.props.StringProperty()
    filter_mode: bpy.props.EnumProperty(items=ENUM_filter_mode)

    actions = []
    
    load_to_object: bpy.props.BoolProperty()

    target_object: bpy.props.StringProperty()

    def invoke(self, context, event):

        if self.filepath == bpy.data.filepath:

            self.report({"INFO"}, "Cannot Append From Self")

            
            return {'FINISHED'}
        
        else:

            return context.window_manager.invoke_props_dialog(self)

    


    def execute(self, context):
        return {"FINISHED"}


    def draw(self, context):

        layout = self.layout
        obj = bpy.data.objects.get(self.target_object) 
        size = 0
        blend_file = self.filepath
      

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, "filter", text="", icon="VIEWZOOM")
        row.prop(self, "filter_clear", text="", icon="X")
        row = col.row()
        col.separator()
        row.prop(self, "filter_mode",expand=True) 

        layout_top = col.row()

        with bpy.data.libraries.load(blend_file) as (data_from, data_to):

            for action in data_from.actions:

                show = Utility_Function.filter_action(self.filter, self.filter_mode, action)

                if show:
                    row = layout.row(align=True)
                    row.alignment = "LEFT"

                    op = row.operator("fr_oam.append_this_action", text="Append", icon="IMPORT")
                    op.target_object = self.target_object
                    op.filepath = self.filepath
                    op.action = action
                    op.filename = self.filename
                    op.load_to_object = self.load_to_object
                    size += 1

                    row.label(text=action)

        if size > 0:
            Import = layout_top.operator("fr_oam.append_all_actions", text="Append All", icon="IMPORT")
            Import.target_object = self.target_object
            Import.filepath = self.filepath
            Import.filter = self.filter
            Import.use_filter = True
            Import.filter_mode = self.filter_mode
            Import.load_to_object = self.load_to_object

        else:
            layout.label(text="No Action Found")


class FR_OT_OAM_Choose_And_Append_BlendFile_Action(bpy.types.Operator):
    """Choose and Append Actions From Blend File"""
    bl_idname = "fr_oam.choose_and_append_blendfile_action"
    bl_label = "Choose and Append BlendFile Action"
    bl_options = {'UNDO', 'REGISTER'}

    filepath: bpy.props.StringProperty()
    filename: bpy.props.StringProperty()

    filter_glob : bpy.props.StringProperty(
        default="*.blend",
        options={'HIDDEN'},
    )

    load_to_object: bpy.props.BoolProperty()


    target_object: bpy.props.StringProperty()

    def invoke(self, context, event):

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):


        if self.filepath == bpy.data.filepath:

            self.report({"INFO"}, "Cannot Append From Self")

            
            return {'FINISHED'}
        


        obj = bpy.data.objects.get(self.target_object) 

        blend_file = self.filepath

        bpy.ops.fr_oam.append_action_list("INVOKE_DEFAULT" ,filepath=self.filepath, filename=self.filename, load_to_object=self.load_to_object, target_object=self.target_object)


        Utility_Function.update_UI()

        return {'FINISHED'}





class FR_OT_OAM_Append_All_Actions_From_BlendFiles(bpy.types.Operator):
    """Append All Actions from Multiple Blend Files"""
    bl_idname = "fr_oam.append_all_actions_from_blendfiles"
    bl_label = "Append All Actions From Blend Files"
    bl_options = {'UNDO', 'REGISTER'}

    filepath: bpy.props.StringProperty()
    filename: bpy.props.StringProperty()

    filter_glob : bpy.props.StringProperty(
        default="*.blend",
        options={'HIDDEN'},
    )


    files: bpy.props.CollectionProperty(
        name="File Path", 
        type=bpy.types.OperatorFileListElement
    )

    use_filter: bpy.props.BoolProperty(default=False)
    filter: bpy.props.StringProperty()
    filter_mode: bpy.props.EnumProperty(items=ENUM_filter_mode)

    load_to_object: bpy.props.BoolProperty()



    target_object: bpy.props.StringProperty()




    def draw(self, context):
        layout = self.layout

        layout.prop(self, "use_filter", text="Use Filter")
        if self.use_filter:
            layout.prop(self, "filter", text="Filter")
            layout.prop(self, "filter_mode", expand=True)

    def invoke(self, context, event):

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):


        if self.filepath == bpy.data.filepath:

            self.report({"INFO"}, "Cannot Append From Self")

            
            return {'FINISHED'}



        obj = bpy.data.objects.get(self.target_object) 


        dirname = os.path.dirname(self.filepath)
        filepaths = Utility_Function.get_filepath_from_files(self.files, dirname)

        for filepath in filepaths:


            bpy.ops.fr_oam.append_all_actions(filepath=filepath, use_filter=self.use_filter, filter=self.filter, filter_mode=self.filter_mode, load_to_object=self.load_to_object, target_object=self.target_object)



        Utility_Function.update_UI()

        return {'FINISHED'}



classes = [FR_OT_OAM_Append_All_Actions_From_BlendFiles, FR_OT_OAM_Choose_And_Append_BlendFile_Action, FR_OT_OAM_Append_Action_List, FR_OT_OAM_Append_This_Action, FR_OT_OAM_Append_All_Actions]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
