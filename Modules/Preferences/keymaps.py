import bpy

import rna_keymap_ui

addon_keymaps = []

def set_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name = "Dopesheet", space_type="DOPESHEET_EDITOR")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="F", value="PRESS", shift=True)
        kmi.properties.name = "FR_TU_MT_Frame_Modal_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "Graph Editor", space_type="GRAPH_EDITOR")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="F", value="PRESS", shift=True)
        kmi.properties.name = "FR_TU_MT_Frame_Modal_Pie"
        addon_keymaps.append([km, kmi])

        km = kc.keymaps.new(name = "Sequencer", space_type="SEQUENCE_EDITOR")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="F", value="PRESS", shift=True)
        kmi.properties.name = "FR_TU_MT_Frame_Modal_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "NLA Editor", space_type="NLA_EDITOR")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="F", value="PRESS", shift=True)
        kmi.properties.name = "FR_TU_MT_Frame_Modal_Pie"
        addon_keymaps.append([km, kmi])

def unset_keymaps():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()



def get_pie_menu(km, operator, menu):
    for idx, kmi in enumerate(km.keymap_items):
        if km.keymap_items.keys()[idx] == operator:
            if km.keymap_items[idx].properties.name == menu:
                return kmi
    return None

def draw_keymaps(self, context, layout):
    col = layout.column()
    col.label(text="Keymap")
    col = layout.column()


    col.label(text="Dopesheet & Timeline")
    kc = context.window_manager.keyconfigs.user # addon
    km = kc.keymaps['Dopesheet'] #
    keymap_items = km.keymap_items
    #km = km.active()


    kmi = get_pie_menu(km, 'wm.call_menu_pie', 'FR_TU_MT_Frame_Modal_Pie')
    kmi.show_expanded = False
    #col.context_pointer_set("keymap", km)
    rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
    col.separator(factor=0.5)

    col.label(text="Graph Editor")
    km = kc.keymaps['Graph Editor'] #
    keymap_items = km.keymap_items
    #km = km.active()


    kmi = get_pie_menu(km, 'wm.call_menu_pie', 'FR_TU_MT_Frame_Modal_Pie')
    kmi.show_expanded = False
    #col.context_pointer_set("keymap", km)
    rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
    col.separator(factor=0.5)


    col.label(text="Sequencer")
    km = kc.keymaps['Sequencer'] #
    keymap_items = km.keymap_items
    #km = km.active()


    kmi = get_pie_menu(km, 'wm.call_menu_pie', 'FR_TU_MT_Frame_Modal_Pie')
    kmi.show_expanded = False
    #col.context_pointer_set("keymap", km)
    rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
    col.separator(factor=0.5)

    col.label(text="NLA Editor")
    km = kc.keymaps['NLA Editor'] #
    keymap_items = km.keymap_items
    #km = km.active()

    kmi = get_pie_menu(km, 'wm.call_menu_pie', 'FR_TU_MT_Frame_Modal_Pie')
    kmi.show_expanded = False
    #col.context_pointer_set("keymap", km)
    rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
    col.separator(factor=0.5)

