import glob, re

for log in glob.glob(r'C:\ProgramData\Windhawk\UIData\user-data\logs\**\*.log', recursive=True):
    try:
        data = open(log, 'r', encoding='utf-8', errors='ignore').read()
        urls = re.findall(r'https?://[^\s\"\'<>]+', data)
        if urls:
            print(log)
            for u in set(urls):
                print(' ', u)
    except: pass
