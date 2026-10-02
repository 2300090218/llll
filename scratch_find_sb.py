import re

with open(r'C:\ProgramData\Windhawk\ModsSource\windows-11-taskbar-styler.wh.cpp', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

chunks = re.findall(r'ThemeTargetStyles\{L"([^"]*StartButton[^"]*)",\s*\{([^}]+)\}\}', text)
print(f"Total StartButton matches: {len(chunks)}")
for t, s in chunks[:15]:
    print("TARGET:", t)
    for line in s.strip().splitlines()[:3]:
        print("  ", line.strip())
