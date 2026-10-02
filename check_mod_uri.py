import urllib.request, re

url = 'https://windhawk.net/mods/windows-11-notification-center-styler'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8', errors='ignore')
        uris = re.findall(r'windhawk://[^\s"\'<>]+', html)
        print('URIs found:', uris)
except Exception as e:
    print(e)
