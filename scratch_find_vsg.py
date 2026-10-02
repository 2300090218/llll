import re

with open(r'C:\ProgramData\Windhawk\ModsSource\windows-11-taskbar-styler.wh.cpp', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

chunks = re.findall(r'ThemeTargetStyles\{L"([^"]+@CommonStates[^"]*)",\s*\{([^}]+)\}\}', text)
states = set()
for t, s in chunks:
    matches = re.findall(r'(\w+)@(\w+)', s)
    for prop, state in matches:
        states.add(state)

print('States for @CommonStates targets:', sorted(list(states)))

# Also check without @CommonStates, what other visual state groups exist
vsg_groups = set(re.findall(r'@([A-Za-z0-9_]+)', text))
print('All VSG groups:', sorted(list(vsg_groups)))
