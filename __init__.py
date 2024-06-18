bl_info = {
    "name": "L-System Addon",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from .lsystem import LSystem

class OBJECT_OT_generate_lsystem(bpy.types.Operator):
    bl_idname = "object.generate_lsystem"
    bl_label = "Generate L-System"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.lsystem_settings
        numIters = settings.numIters
        startStr = settings.startStr
        rules = eval(settings.rules)  # Convert string to dictionary
        step_length = settings.step_length
        default_angle = settings.default_angle

        # Load predefined meshes and store them in a dictionary
        flower_mesh = bpy.data.objects.get(settings.flower_mesh_name)
        leaf_mesh = bpy.data.objects.get(settings.leaf_mesh_name)

        mesh_dict = {
            'P': flower_mesh,
            'L': leaf_mesh
        }

        # Create LSystem instance
        ls = LSystem(numIters, startStr, rules, step_length, default_angle, mesh_dict)
        
        # Draw the LSystem
        ls.draw()

        return {'FINISHED'}

class LSystemPanel(bpy.types.Panel):
    bl_label = "L-System Generator"
    bl_idname = "OBJECT_PT_lsystem"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'L-System'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        lsystem_settings = scene.lsystem_settings

        layout.prop(lsystem_settings, "numIters")
        layout.prop(lsystem_settings, "startStr")
        layout.prop(lsystem_settings, "rules")
        layout.prop(lsystem_settings, "step_length")
        layout.prop(lsystem_settings, "default_angle")
        layout.prop(lsystem_settings, "flower_mesh_name")
        layout.prop(lsystem_settings, "leaf_mesh_name")
        layout.operator("object.generate_lsystem")

class LSystemSettings(bpy.types.PropertyGroup):
    numIters: bpy.props.IntProperty(name="Iterations", default=3)
    startStr: bpy.props.StringProperty(name="Start String", default='A')
    rules: bpy.props.StringProperty(name="Rules", default="{'A':'>F+(120)F[+FLFLLFLP][-FFAFA][+++FFAFA]'}")
    step_length: bpy.props.FloatProperty(name="Step Length", default=1.0)
    default_angle: bpy.props.FloatProperty(name="Default Angle", default=45.0)
    flower_mesh_name: bpy.props.StringProperty(name="Flower Mesh Name", default='FlowerMesh')
    leaf_mesh_name: bpy.props.StringProperty(name="Leaf Mesh Name", default='LeafMesh')

def register():
    bpy.utils.register_class(OBJECT_OT_generate_lsystem)
    bpy.utils.register_class(LSystemPanel)
    bpy.utils.register_class(LSystemSettings)
    bpy.types.Scene.lsystem_settings = bpy.props.PointerProperty(type=LSystemSettings)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_generate_lsystem)
    bpy.utils.unregister_class(LSystemPanel)
    bpy.utils.unregister_class(LSystemSettings)
    del bpy.types.Scene.lsystem_settings

if __name__ == "__main__":
    register()