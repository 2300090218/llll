import re

with open(r'C:\ProgramData\Windhawk\ModsSource\windows-11-taskbar-styler.wh.cpp', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

chunks = re.findall(r'ThemeTargetStyles\{L"(Taskbar\.TaskListButton[^"]*)",\s*\{([^}]+)\}\}', text)
print(f"Found {len(chunks)} TaskListButton styles:")
for t, s in chunks[:20]:
    print("TARGET:", t)
    for line in s.strip().splitlines()[:5]:
        print("  ", line.strip())
