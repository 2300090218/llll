import re

with open(r'C:\ProgramData\Windhawk\ModsSource\windows-11-taskbar-styler.wh.cpp', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Match ThemeTargetStyles
matches = re.findall(r'ThemeTargetStyles\{L"([^"]+)",\s*\{([^}]+)\}\}', text)
print(f"Total ThemeTargetStyles matched: {len(matches)}")
for target, styles in matches:
    if 'ScaleTransform' in styles:
        print("\n=== TARGET ===")
        print(target)
        print("--- STYLES ---")
        for s in styles.strip().splitlines():
            s = s.strip()
            if s:
                print("  ", s)
