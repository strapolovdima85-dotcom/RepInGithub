import os

def generate_tree(startpath):
    tree_str = "## Структура проекта\n```text\n"
    for root, dirs, files in os.walk(startpath):
        # Игнорируем скрытые папки (типа .git) и venv
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree_str += f"{subindent}{f}\n"
    tree_str += "```"
    return tree_str

with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Название проекта\n\n Описание проекта.\n\n")
    f.write(generate_tree("."))