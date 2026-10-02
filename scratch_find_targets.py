import re

with open(r'C:\ProgramData\Windhawk\ModsSource\windows-11-taskbar-styler.wh.cpp', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

targets = re.findall(r'ThemeTargetStyles\{L"([^"]+)"', text)
unique_targets = sorted(list(set(targets)))

print(f"Total targets: {len(unique_targets)}")
for t in unique_targets:
    if '@' in t and ('TaskList' in t or 'LaunchList' in t or 'Search' in t or 'Icon' in t or 'Button' in t):
        print("TARGET:", t)
