import maya.cmds as cmds

# 用于存储变换属性的全局列表
clipboard = []
language = '简体中文'

# 文本字典，用于支持多语言
texts = {
    '简体中文': {
        'title': '剪贴板插件',
        'copy': '复制变换属性',
        'paste': '粘贴变换属性',
        'clear': '清理剪贴板',
        'help': '帮助',
        'language': '语言',
        'help_text': '这是一个剪贴板插件，允许您复制和粘贴选定对象的变换属性。',
        'select_warning': '请选择一个物体',
        'record_warning': '请选择剪贴板中的记录',
        'no_valid_transform': '所选剪贴板条目中没有有效的变换属性',
        'copied': '变换属性已复制到剪贴板',
        'pasted': '变换属性已从剪贴板粘贴',
        'cleared': '剪贴板已清空'
    },
    '繁體中文': {
        'title': '剪貼板插件',
        'copy': '複製變換屬性',
        'paste': '粘貼變換屬性',
        'clear': '清理剪貼板',
        'help': '幫助',
        'language': '語言',
        'help_text': '這是一個剪貼板插件，允許您複製和粘貼選定對象的變換屬性。',
        'select_warning': '請選擇一個物體',
        'record_warning': '請選擇剪貼板中的記錄',
        'no_valid_transform': '所選剪貼板條目中沒有有效的變換屬性',
        'copied': '變換屬性已複製到剪貼板',
        'pasted': '變換屬性已從剪貼板粘貼',
        'cleared': '剪貼板已清空'
    },
    '日本語': {
        'title': 'クリップボードプラグイン',
        'copy': '変換属性をコピー',
        'paste': '変換属性を貼り付け',
        'clear': 'クリップボードをクリア',
        'help': 'ヘルプ',
        'language': '言語',
        'help_text': 'これはクリップボードプラグインで、選択したオブジェクトの変換属性をコピーおよび貼り付けできます。',
        'select_warning': 'オブジェクトを選択してください',
        'record_warning': 'クリップボードの記録を選択してください',
        'no_valid_transform': '選択されたクリップボードエントリに有効な変換属性がありません',
        'copied': '変換属性がクリップボードにコピーされました',
        'pasted': '変換属性がクリップボードから貼り付けられました',
        'cleared': 'クリップボードがクリアされました'
    },
    'English': {
        'title': 'Clipboard Plugin',
        'copy': 'Copy Transform Attributes',
        'paste': 'Paste Transform Attributes',
        'clear': 'Clear Clipboard',
        'help': 'Help',
        'language': 'Language',
        'help_text': 'This is a clipboard plugin that allows you to copy and paste the transform attributes of selected objects.',
        'select_warning': 'Please select an object',
        'record_warning': 'Please select records from the clipboard',
        'no_valid_transform': 'No valid transform attributes in selected clipboard entries',
        'copied': 'Transform attributes copied to clipboard',
        'pasted': 'Transform attributes pasted from clipboard',
        'cleared': 'Clipboard cleared'
    }
}

# 复制选中物体的变换属性
def copy_transform():
    global language
    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning(texts[language]['select_warning'])
        return
    
    obj = selected[0]
    transform = cmds.xform(obj, query=True, matrix=True)
    clipboard_entry = {
        'name': obj,
        'transform': transform
    }
    clipboard.append(clipboard_entry)
    display_text = f"{obj}: {transform}"
    cmds.textScrollList('clipboardList', edit=True, append=display_text)
    cmds.inViewMessage(amg=texts[language]['copied'], pos='topCenter', fade=True)

# 粘贴变换属性到选中物体
def paste_transform():
    global language
    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning(texts[language]['select_warning'])
        return
    
    selected_clipboard_items = cmds.textScrollList('clipboardList', query=True, selectItem=True)
    if not selected_clipboard_items:
        cmds.warning(texts[language]['record_warning'])
        return

    selected_transforms = [item.split(": ")[1] for item in selected_clipboard_items]
    
    if len(selected_transforms) == 1:
        transform = eval(selected_transforms[0])
        for obj in selected:
            cmds.xform(obj, matrix=transform)
            cmds.inViewMessage(amg=texts[language]['pasted'], pos='topCenter', fade=True)
    else:
        matrices = [eval(transform) for transform in selected_transforms]
        if not matrices:
            cmds.warning(texts[language]['no_valid_transform'])
            return

        avg_matrix = [sum(x) / len(matrices) for x in zip(*matrices)]
        
        for obj in selected:
            cmds.xform(obj, matrix=avg_matrix)
            cmds.inViewMessage(amg=texts[language]['pasted'], pos='topCenter', fade=True)

# 清理剪贴板
def clear_clipboard():
    global clipboard
    global language
    clipboard = []
    cmds.textScrollList('clipboardList', edit=True, removeAll=True)
    cmds.inViewMessage(amg=texts[language]['cleared'], pos='topCenter', fade=True)

# 显示帮助窗口
def show_help():
    global language
    help_text = texts[language]['help_text']
    cmds.confirmDialog(title=texts[language]['help'], message=help_text)

# 切换语言
def switch_language(lang):
    global language
    language = lang
    cmds.workspaceControl('clipboardUIWorkspaceControl', edit=True, label=texts[language]['title'])
    cmds.button('copyBtn', edit=True, label=texts[language]['copy'])
    cmds.button('pasteBtn', edit=True, label=texts[language]['paste'])
    cmds.button('clearBtn', edit=True, label=texts[language]['clear'])

# 创建UI
def create_ui():
    # 如果已经存在窗口和控制，请删除
    if cmds.workspaceControl('clipboardUIWorkspaceControl', exists=True):
        cmds.deleteUI('clipboardUIWorkspaceControl', control=True)

    # 创建窗口
    window = cmds.window("clipboardUI", title=texts[language]['title'], widthHeight=(500, 300), sizeable=True)
    
    cmds.menuBarLayout()
    cmds.menu(label=texts[language]['language'], tearOff=True)
    cmds.menuItem(label='简体中文', command=lambda x: switch_language('简体中文'))
    cmds.menuItem(label='繁體中文', command=lambda x: switch_language('繁體中文'))
    cmds.menuItem(label='日本語', command=lambda x: switch_language('日本語'))
    cmds.menuItem(label='English', command=lambda x: switch_language('English'))
    cmds.menu(label=texts[language]['help'], tearOff=True)
    cmds.menuItem(label=texts[language]['help'], command=lambda x: show_help())
    
    form = cmds.formLayout()
    copy_btn = cmds.button('copyBtn', label=texts[language]['copy'], command=lambda x: copy_transform())
    paste_btn = cmds.button('pasteBtn', label=texts[language]['paste'], command=lambda x: paste_transform())
    clear_btn = cmds.button('clearBtn', label=texts[language]['clear'], command=lambda x: clear_clipboard())
    clipboard_list = cmds.textScrollList('clipboardList', numberOfRows=8, allowMultiSelection=True)
    
    cmds.formLayout(form, edit=True, attachForm=[
        (copy_btn, 'top', 5),
        (copy_btn, 'left', 5),
        (copy_btn, 'right', 5),
        (paste_btn, 'left', 5),
        (paste_btn, 'right', 5),
        (clear_btn, 'left', 5),
        (clear_btn, 'right', 5),
        (clipboard_list, 'left', 5),
        (clipboard_list, 'right', 5),
        (clipboard_list, 'bottom', 5)
    ], attachControl=[
        (paste_btn, 'top', 5, copy_btn),
        (clear_btn, 'top', 5, paste_btn),
        (clipboard_list, 'top', 5, clear_btn)
    ])

    cmds.showWindow(window)

    # 创建可吸附的 workspaceControl 并将窗口嵌入其中
    cmds.workspaceControl('clipboardUIWorkspaceControl', label=texts[language]['title'], tabToControl=('MayaWindow', -1), retain=True)
    cmds.control(window, edit=True, parent='clipboardUIWorkspaceControl')

# 加载插件时创建UI
create_ui()
