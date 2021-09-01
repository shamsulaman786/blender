import bpy

from bpy.types import Panel

class OTB_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Hall making operations"
    bl_category = "OTB_Hall_Maker_Utility"

    def draw(self,context):
        layout = self.layout
        #2 columns with buttons
        row = layout.row()
        col = row.column()
        col.operator("object.apply_all_mods", text = "Apply")

        # col = row.column()
        # col.operator("object.cancel_all_mods", text = "Cancel all")