import bpy

#Editing bone


class FR_OT_BAKER_Constraint_Toogle(bpy.types.Operator):
    """Constraint Toogle"""
    bl_idname = "fr_baker.toogle_constraint"
    bl_label = "Toogle Constraints"
    bl_options = {'REGISTER', 'UNDO'}

    mute : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        if context.mode in ["OBJECT", "POSE"]:
            return True
        else:
            return False

    def execute(self, context):
        scn = context.scene
        baker = scn.FR_BAKER
        obj = baker.bake_to

        if obj:

            if obj.type == "ARMATURE":
                # object = context.object
                Pose_Bone = obj.pose.bones

                for bone in Pose_Bone:

                    for constraint in bone.constraints:
                        constraint.mute = self.mute


        return {'FINISHED'}

classes = [FR_OT_BAKER_Constraint_Toogle]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
