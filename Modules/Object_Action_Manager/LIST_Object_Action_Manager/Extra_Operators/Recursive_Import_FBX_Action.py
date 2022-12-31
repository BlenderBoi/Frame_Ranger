

import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
import bpy_extras
from bpy_extras.io_utils import orientation_helper

import os
import pathlib
import webbrowser


ENUM_fbx_manual_orientation_up=[("","",""),("","",""),("","",""),("","",""),("","",""),("","","")]
ENUM_fbx_manual_orientation_forward=[("","",""),("","",""),("","",""),("","",""),("","",""),("","","")]
ENUM_bone_axis=[("X","X Axis",""),("Y","Y Axis",""),("Z","Z Axis",""),("-X","-X Axis",""),("-Y","-Y Axis",""),("-Z","-Z Axis","")]

ENUM_FBX_Importer=[("BUILTIN","Built In","Built In"),("BETTER_FBX","Better FBX (Experimental)","Better FBX")]
# ENUM_Load_To=[("ACTIVE","Active Object","Active Object"),("DETECT_NAME","Detect Object Name","Detect Object Name"), ("NONE", "None", "None")]
# ENUM_Load_To=[("ACTIVE","Active Object","Active Object"), ("NONE", "None", "None")]


def recursive_collect_file_by_format(root_directory, format):

    collected_files = []
    items = os.walk(root_directory)

    for (path, directories, files) in items:
        for file in files:
            if file.endswith(format):
                collected_files.append(path+"/"+file)

    return collected_files


def update_open_url(self, context):
    url = "https://blendermarket.com/products/better-fbx-importer--exporter"

    if self.open_url:
        self.open_url = False
    
    webbrowser.open(url)

@orientation_helper(axis_forward='-Z', axis_up='Y')
class FR_OT_OAM_Recursive_Import_FBX_Action(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Recursive Import FBX Action (Experimental)"""
    bl_idname = "fr_oam.recursive_import_fbx_action"
    bl_label = "Recursive Add FBX Action to Slot (Experimental)"
    bl_options = {'UNDO', 'REGISTER', 'PRESET'}

    target_object: bpy.props.StringProperty()

    directory: bpy.props.StringProperty()

    open_url: bpy.props.BoolProperty(default=False, name="Visit Website", update=update_open_url)

    # filename_ext = ".fbx"
    filter_glob: bpy.props.StringProperty(
        default="*.fbx", 
        options={'HIDDEN'}
    )

    # files: bpy.props.CollectionProperty(
    #     name="File Path", 
    #     type=bpy.types.OperatorFileListElement
    # )
    
    use_file_name_as_action_name: bpy.props.BoolProperty(
        default=False, 
        name="Use File Name as Action Name"
    )


    importer: bpy.props.EnumProperty(
        items=ENUM_FBX_Importer
    )

    
    fbx_transform_scale: bpy.props.FloatProperty(
        default=1.0, 
        min=0
    )

    fbx_transform_apply_transform: bpy.props.BoolProperty(
        default=False,
        description="Bake space transform into object data, avoids getting unwanted rotations to objects when "
                    "target space is not aligned with Blender's space "
                    "(WARNING! experimental option, use at own risks, known broken with armatures/animations)",
    )

    fbx_transform_pre_post_rotation: bpy.props.BoolProperty(
        default=True,
        description="Use pre/post rotation from FBX transform (you may have to disable that in some cases)",
    ) 
    
    fbx_manual_orientation: bpy.props.BoolProperty(
        default=False,
        description="Specify orientation and scale, instead of using embedded data in FBX file",
    )
    # fbx_manual_orientation_forward: bpy.props.EnumProperty(items=ENUM_fbx_manual_orientation_forward)
    # fbx_manual_orientation_up: bpy.props.EnumProperty(items=ENUM_fbx_manual_orientation_up)

    fbx_animation_offset: bpy.props.FloatProperty(
        default=1.0, 
        description="Offset to apply to animation during import, in frames",
    )

    fbx_armature_ignore_leaf_bone: bpy.props.BoolProperty(
        default=False,
        description="Ignore the last bone at the end of each chain (used to mark the length of the previous bone)",
    )

    fbx_armature_force_connect_child: bpy.props.BoolProperty(
        default=False,
        description="Force connection of children bones to their parent, even if their computed head/tail "
                    "positions do not match (can be useful with pure-joints-type armatures)",
    )

    fbx_armature_automatic_bone_orientation: bpy.props.BoolProperty(
        default=False,
        description="Try to align the major bone axis with the bone children",
    )

    fbx_armature_primary_bone_axis: bpy.props.EnumProperty(
        items=ENUM_bone_axis, 
        default="Y"
    )

    fbx_armature_secondary_bone_axis: bpy.props.EnumProperty(
        items=ENUM_bone_axis,                           
        default="X"
    )






    better_fbx_use_auto_bone_orientation: bpy.props.BoolProperty(
            name="Automatic Bone Orientation",
            description="Automatically sort bones orientations, if you want to preserve the original armature, please disable the option",
            default=True,
            )

    better_fbx_my_calculate_roll: bpy.props.EnumProperty(
            name="Calculate Roll",
            description="Automatically fix alignment of imported bones’ axes when 'Automatic Bone Orientation' is enabled",
            items=(('POS_X', "POS_X", "POS_X"),
                   ('POS_Z', "POS_Z", "POS_Z"),
                   ('GLOBAL_POS_X', "GLOBAL_POS_X", "GLOBAL_POS_X"),
                   ('GLOBAL_POS_Y', "GLOBAL_POS_Y", "GLOBAL_POS_Y"),
                   ('GLOBAL_POS_Z', "GLOBAL_POS_Z", "GLOBAL_POS_Z"),
                   ('NEG_X', "NEG_X", "NEG_X"),
                   ('NEG_Z', "NEG_Z", "NEG_Z"),
                   ('GLOBAL_NEG_X', "GLOBAL_NEG_X", "GLOBAL_NEG_X"),
                   ('GLOBAL_NEG_Y', "GLOBAL_NEG_Y", "GLOBAL_NEG_Y"),
                   ('GLOBAL_NEG_Z', "GLOBAL_NEG_Z", "GLOBAL_NEG_Z"),
                   ('ACTIVE', "ACTIVE", "ACTIVE"),
                   ('VIEW', "VIEW", "VIEW"),
                   ('CURSOR', "CURSOR", "CURSOR"),
                   ('None', "None", "Does not fix alignment of imported bones’ axes")),
            default='None',
            )

    better_fbx_my_bone_length: bpy.props.FloatProperty(
        name = "Bone Length",
        description = "Bone length when 'Automatic Bone Orientation' is disabled",
        default = 10.0,
        min = 0.0001,
        max = 10000.0)

    better_fbx_my_leaf_bone: bpy.props.EnumProperty(
            name="Leaf Bone",
            description="The length of leaf bone",
            items=(('Long', "Long", "1/1 length of its parent"),
                   ('Short', "Short", "1/10 length of its parent")),
            default='Long',
            )

    better_fbx_use_fix_bone_poses: bpy.props.BoolProperty(
            name="Fix Bone Poses",
            description="Try fixing bone poses with default poses whenever bind poses are not equal to default poses",
            default=False,
            )

    better_fbx_use_fix_attributes: bpy.props.BoolProperty(
            name="Fix Attributes For Unity & C4D",
            description="Try fixing null attributes for Unity's FBX exporter & C4D's FBX exporter, but it may bring extra fake bones",
            default=False,
            )

    better_fbx_use_only_deform_bones: bpy.props.BoolProperty(
            name="Only Deform Bones",
            description="Import only deform bones",
            default=False,
            )

    better_fbx_use_vertex_animation: bpy.props.BoolProperty(
            name="Vertex Animation",
            description="Import vertex animation",
            default=True,
            )

    better_fbx_my_animation_offset: bpy.props.IntProperty(
        name = "Animation Offset",
        description = "Add an offset to all keyframes",
        default = 0,
        min = -1000000,
        max = 1000000)

    better_fbx_my_scale: bpy.props.FloatProperty(
        name = "Scale",
        description = "Scale all data",
        default = 0.01,
        min = 0.0001,
        max = 10000.0)

    better_fbx_use_optimize_for_blender: bpy.props.BoolProperty(
            name="Optimize For Blender",
            description="Make Blender friendly rotation and scale. This is an experimental feature, which may has bugs, use at your own risk",
            default=False,
            )

    better_fbx_my_rotation_mode: bpy.props.EnumProperty(
            name="Rotation Mode",
            description="Rotation mode of all objects",
            items=(('QUATERNION', "Quaternion (WXYZ)", "Quaternion (WXYZ), No Gimbal Lock"),
                   ('XYZ', "XYZ Euler", "XYZ Rotation Order - prone to Gimbal Lock"),
                   ('XZY', "XZY Euler", "XZY Rotation Order - prone to Gimbal Lock"),
                   ('YXZ', "YXZ Euler", "YXZ Rotation Order - prone to Gimbal Lock"),
                   ('YZX', "YZX Euler", "YZX Rotation Order - prone to Gimbal Lock"),
                   ('ZXY', "ZXY Euler", "ZXY Rotation Order - prone to Gimbal Lock"),
                   ('ZYX', "ZYX Euler", "ZYX Rotation Order - prone to Gimbal Lock"),
                   ('AXIS_ANGLE', "Axis Angle", "Axis Angle (W+XYZ), defines a rotation around some axis defined by 3D-Vector")),
            default='QUATERNION',
            )

    # load_action_to_object_action_manager: bpy.props.BoolProperty(default=True)
    # load_to: bpy.props.EnumProperty(items=ENUM_Load_To)
    load_to_object: bpy.props.BoolProperty(default=True)
    purge_orphan_data: bpy.props.BoolProperty(default=True)

    def draw_better_fbx_options(self, context, layout):

        if Utility_Function.addon_exists("better_fbx"):
            layout.label(text="Basic Options:")
            box = layout.box()
            box.prop(self, 'better_fbx_my_rotation_mode')
            box.prop(self, 'better_fbx_my_scale')

            layout.label(text="Blender Options: (Experimental)")
            box = layout.box()
            box.prop(self, 'better_fbx_use_optimize_for_blender')

            layout.label(text="Bone Options:")
            box = layout.box()
            box.prop(self, 'better_fbx_use_auto_bone_orientation')
            box.prop(self, 'better_fbx_my_calculate_roll')
            box.prop(self, 'better_fbx_my_bone_length')
            box.prop(self, 'better_fbx_my_leaf_bone')
            box.prop(self, 'better_fbx_use_fix_bone_poses')
            box.prop(self, 'better_fbx_use_fix_attributes')
            box.prop(self, 'better_fbx_use_only_deform_bones')

            layout.label(text="Animation Options:")
            box = layout.box()
            box.prop(self, 'better_fbx_my_animation_offset')

            layout.label(text="Vertex Animation Options:")
            box = layout.box()
            box.prop(self, 'better_fbx_use_vertex_animation')

        else:

            layout.label(text="Better FBX Addon Not Found", icon="ERROR")
            layout.separator()
            box = layout.box()
            box.label(text="Better FBX is an Paid Addon", icon="INFO")
            box.label(text="Made By meshonline", icon="USER")
            box.separator()
            box.label(text="Get this addon in:", icon="TRIA_DOWN_BAR")
            box.label(text="https://blendermarket.com/products/better-fbx-importer--exporter")
            box.prop(self, "open_url", text="Visit Website", icon="LINKED")
            # Open Website In Browser
            # Copy Link
            layout.label(text="Fallback to Builtin Import FBX", icon="INFO")

    def draw_builtin_fbx_options(self, context, layout):

        layout.label(text="Transform") 
        box = layout.box()
        box.prop(self, "fbx_transform_scale", text="Scale")
        row = box.row()
        row.prop(self, "fbx_transform_apply_transform", text="Apply Transform")
        row.label(text="Experimental", icon="ERROR")

        box.prop(self, "fbx_transform_pre_post_rotation", text="Use Pre/Post Rotation")
        
        box.prop(self, "fbx_manual_orientation", text="Manual Orientation")

        sub_box = box.box()
        sub_box.enabled = self.fbx_manual_orientation
        sub_box.prop(self, "axis_forward", text="Forward")

        sub_box.prop(self, "axis_up", text="Up")


        layout.label(text="Animation")
        box = layout.box()
        box.prop(self, "fbx_animation_offset", text="Animation Offset")


        layout.label(text="Armature")
        box = layout.box()

        box.label(text="Primary Bone Axis:")
        box.prop(self, "fbx_armature_primary_bone_axis", text="")

        box.label(text="Secondary Bone Axis:")
        box.prop(self, "fbx_armature_secondary_bone_axis", text="")


        box.prop(self, "fbx_armature_ignore_leaf_bone", text="Ignore Leaf Bone")
        box.prop(self, "fbx_armature_force_connect_child", text="Force Connect Child")
        box.prop(self, "fbx_armature_automatic_bone_orientation", text="Automatic Bone Orientation")


    def draw(self, context):
        layout = self.layout

        

        layout.label(text="Frame Ranger")
        box = layout.box()
        # box.prop(self, "load_action_to_object_action_manager", text="Load Action to Object Action Manager")
        box.prop(self, "load_to_object", text="Load To Object")
        box.prop(self, "purge_orphan_data", text="Purge Orphan Data")

        if self.purge_orphan_data:
            layout.label(text="Warning", icon="INFO")
            box = layout.box()
            box.label(text="This Will Purge Orphan Data", icon="ORPHAN_DATA")
            box.label(text="Make Sure to Apply Fake User", icon="FAKE_USER_ON")
    


        layout.label(text="Action Rename")
        box = layout.box()
        box.prop(self, "use_file_name_as_action_name", text="Use File Name As Action Name")

        layout.label(text="FBX Importer")
        layout.prop(self, "importer",expand=True)

        if self.importer == "BUILTIN":
            self.draw_builtin_fbx_options(context, layout)

        if self.importer == "BETTER_FBX":
            self.draw_better_fbx_options(context, layout)


    def execute(self, context):

        obj = bpy.data.objects.get(self.target_object) 
        dirname = os.path.dirname(self.filepath)
        # filepaths = Utility_Function.get_filepath_from_files(self.files, dirname)

        filepaths = recursive_collect_file_by_format(self.directory, ".fbx")

        actions = [action for action in bpy.data.actions]


        original_objects = [object for object in bpy.data.objects]


        action_to_load = []

        if context.object:
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


        if self.importer == "BETTER_FBX":
            if not Utility_Function.addon_exists("better_fbx"):
                self.importer = "BUILTIN"

        for selected_obj in context.selected_objects:
            selected_obj.select_set(False)


        for filepath in filepaths:

            if self.importer == "BUILTIN":
                bpy.ops.import_scene.fbx(
                    filepath=filepath, 
                    use_custom_normals=False,
                    use_subsurf=False,
                    use_custom_props=False,
                    use_custom_props_enum_as_string=False,
                    use_image_search=False,
                    global_scale=self.fbx_transform_scale,
                    decal_offset=0.0,
                    bake_space_transform=self.fbx_transform_apply_transform,
                    use_prepost_rot=self.fbx_transform_pre_post_rotation,
                    use_manual_orientation=self.fbx_manual_orientation,
                    axis_forward=self.axis_forward,
                    axis_up=self.axis_up,
                    use_anim=True, 
                    anim_offset=self.fbx_animation_offset,
                    ignore_leaf_bones=self.fbx_armature_ignore_leaf_bone,
                    force_connect_children=self.fbx_armature_force_connect_child,
                    automatic_bone_orientation=self.fbx_armature_automatic_bone_orientation,
                    primary_bone_axis=self.fbx_armature_primary_bone_axis,
                    secondary_bone_axis=self.fbx_armature_secondary_bone_axis
                ) 

                for selected in context.selected_objects:
                    bpy.data.objects.remove(selected, do_unlink=True)



            if self.importer == "BETTER_FBX":
                if Utility_Function.addon_exists("better_fbx"):
                    bpy.ops.better_import.fbx(
                    filepath=filepath,
                    use_auto_bone_orientation=self.better_fbx_use_auto_bone_orientation,
                    my_calculate_roll=self.better_fbx_my_calculate_roll,
                    my_bone_length=self.better_fbx_my_bone_length,
                    my_leaf_bone=self.better_fbx_my_leaf_bone,
                    use_fix_bone_poses=self.better_fbx_use_fix_bone_poses,
                    use_fix_attributes=self.better_fbx_use_fix_attributes,
                    use_only_deform_bones=self.better_fbx_use_only_deform_bones,
                    use_vertex_animation=self.better_fbx_use_vertex_animation,
                    use_animation=True,
                    my_animation_offset=self.better_fbx_my_animation_offset,
                    use_triangulate=False,
                    my_import_normal="Import",
                    use_auto_smooth=True,
                    my_angle=60.0, 
                    my_shade_mode="Smooth",
                    my_scale=self.better_fbx_my_scale,
                    use_optimize_for_blender=self.better_fbx_use_optimize_for_blender,
                    use_reset_mesh_origin=True,
                    use_edge_crease=True,
                    my_edge_crease_scale=1.0, 
                    my_edge_smoothing="FBXSDK",
                    use_import_materials=False,
                    use_rename_by_filename=False,
                    my_rotation_mode=self.better_fbx_my_rotation_mode,
                    )
                     
                    for object in bpy.data.objects:
                        if not object in original_objects:
                            bpy.data.objects.remove(object)

            # for selected in context.selected_objects:
            #     bpy.data.objects.remove(selected, do_unlink=True)


            for action in bpy.data.actions:
        
                if not action in actions:

                    if not action in action_to_load:

                        action_to_load.append(action)

                        if self.use_file_name_as_action_name:
                            action.name = pathlib.Path(filepath).stem

        if self.load_to_object:

            for action in action_to_load:
            
                action.use_fake_user = True
                action_list_helper = OAM_Functions.Action_List_Helper(obj)
                action_list_helper.load_action(action, use_fake_user=True, update_index=True, sync=True)


                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj




        if self.purge_orphan_data:
            bpy.ops.outliner.orphans_purge() 



        Utility_Function.update_UI()
        return {'FINISHED'}


classes = [FR_OT_OAM_Recursive_Import_FBX_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
