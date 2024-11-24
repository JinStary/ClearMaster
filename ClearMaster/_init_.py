bl_info = {
    "name": "ClearMaster",
    "author": "StarStudio",  # 修改作者为 StarStudio
    "version": (1, 6),
    "blender": (3, 0, 0),
    "location": "View3D > Tool > ClearMaster",
    "description": "Tools to clean materials, vertex groups, shape keys and reset view color of selected objects independently",
    "category": "Object",
}

import bpy


# 清除选中模型的材质球
class OBJECT_OT_clear_materials(bpy.types.Operator):
    bl_idname = "object.clear_materials"
    bl_label = "Clear Materials"
    bl_description = "Clear all materials from selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        cleared_count = 0
        empty_material_count = 0  # 用于统计删除的空材质球
        non_empty_material_count = 0  # 用于统计删除的有信息材质球

        for obj in selected_objects:
            if obj.type == 'MESH' and obj.material_slots:
                # 清除材质球
                for slot in obj.material_slots:
                    if slot.material:
                        if slot.material.name == "":  # 如果材质为空，则计数
                            empty_material_count += 1
                        else:
                            non_empty_material_count += 1
                        slot.material = None  # 移除材质球
                        cleared_count += 1

                # 删除所有材质槽
                while len(obj.material_slots) > 0:
                    bpy.context.view_layer.objects.active = obj  # 确保obj是活动对象
                    bpy.ops.object.material_slot_remove()  # 使用操作移除材质槽

        # 输出清除日志
        if cleared_count > 0:
            self.report({'INFO'}, f"Total materials cleared: {cleared_count}")
            print(f"[ClearMaster] Cleared {cleared_count} materials from selected objects.")
        
        if empty_material_count > 0:
            self.report({'INFO'}, f"Total empty materials cleared: {empty_material_count}")
            print(f"[ClearMaster] Cleared {empty_material_count} empty materials.")
        
        if non_empty_material_count > 0:
            self.report({'INFO'}, f"Total materials with data cleared: {non_empty_material_count}")
            print(f"[ClearMaster] Cleared {non_empty_material_count} materials with data.")

        if cleared_count == 0:
            self.report({'INFO'}, "No materials to clear.")

        return {'FINISHED'}



# 清除选中模型的顶点组
class OBJECT_OT_clear_vertex_groups(bpy.types.Operator):
    bl_idname = "object.clear_vertex_groups"
    bl_label = "Clear Vertex Groups"
    bl_description = "Clear vertex groups from selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        cleared_count = 0

        for obj in selected_objects:
            if obj.type == 'MESH' and obj.vertex_groups:
                cleared_count += len(obj.vertex_groups)
                obj.vertex_groups.clear()
                self.report({'INFO'}, f"Cleared vertex groups on {obj.name}")

        if cleared_count > 0:
            self.report({'INFO'}, f"Total vertex groups cleared: {cleared_count}")
            print(f"[ClearMaster] Cleared {cleared_count} vertex groups from selected objects.")
        else:
            self.report({'INFO'}, "No vertex groups to clear.")

        return {'FINISHED'}


# 清除选中模型的形状键
class OBJECT_OT_clear_shape_keys(bpy.types.Operator):
    bl_idname = "object.clear_shape_keys"
    bl_label = "Clear Shape Keys"
    bl_description = "Clear all shape keys from selected objects, including the Basis shape"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        cleared_count = 0

        for obj in selected_objects:
            if obj.type == 'MESH' and obj.data.shape_keys:
                key_blocks = obj.data.shape_keys.key_blocks

                # Remove all shape keys, including Basis
                while key_blocks:
                    obj.shape_key_remove(key_blocks[0])
                    cleared_count += 1

                self.report({'INFO'}, f"Cleared shape keys on {obj.name}")

        if cleared_count > 0:
            self.report({'INFO'}, f"Total shape keys cleared: {cleared_count}")
            print(f"[ClearMaster] Cleared {cleared_count} shape keys from selected objects.")
        else:
            self.report({'INFO'}, "No shape keys to clear.")

        return {'FINISHED'}


# 将选定模型的视图显示颜色重置为白色
class OBJECT_OT_reset_view_color(bpy.types.Operator):
    bl_idname = "object.reset_view_color"
    bl_label = "Reset View Color"
    bl_description = "Set the viewport display color of selected objects to white (#FFFFFF)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        color_reset_count = 0

        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.display_type = 'SOLID'  # 设置为实体模式
                obj.color = (1.0, 1.0, 1.0, 1.0)  # 将颜色设置为白色 (1.0, 1.0, 1.0)
                color_reset_count += 1

        if color_reset_count > 0:
            self.report({'INFO'}, f"Total objects' view color reset to white: {color_reset_count}")
            print(f"[ClearMaster] Reset viewport color to white for {color_reset_count} objects.")
        else:
            self.report({'INFO'}, "No objects to reset color.")

        return {'FINISHED'}


# 自定义面板
class VIEW3D_PT_clear_master_panel(bpy.types.Panel):
    bl_label = "ClearMaster"
    bl_idname = "VIEW3D_PT_clear_master"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ClearMaster"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Cleanup Tools for Selected Objects")
        layout.operator("object.clear_materials", icon='MATERIAL')
        layout.operator("object.clear_vertex_groups", icon='X')
        layout.operator("object.clear_shape_keys", icon='SHAPEKEY_DATA')
        layout.operator("object.reset_view_color", icon='COLOR')


# 注册和卸载插件
def register():
    bpy.utils.register_class(OBJECT_OT_clear_materials)
    bpy.utils.register_class(OBJECT_OT_clear_vertex_groups)
    bpy.utils.register_class(OBJECT_OT_clear_shape_keys)
    bpy.utils.register_class(OBJECT_OT_reset_view_color)
    bpy.utils.register_class(VIEW3D_PT_clear_master_panel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_clear_materials)
    bpy.utils.unregister_class(OBJECT_OT_clear_vertex_groups)
    bpy.utils.unregister_class(OBJECT_OT_clear_shape_keys)
    bpy.utils.unregister_class(OBJECT_OT_reset_view_color)
    bpy.utils.unregister_class(VIEW3D_PT_clear_master_panel)


if __name__ == "__main__":
    register()
