import os
import shutil
import win32com.client

workspace = r"c:\Users\bhara\OneDrive\Documents\llll"
tools_dir = os.path.join(os.path.expanduser(r"~\OneDrive\Desktop"), "OS26 Tools")
if not os.path.exists(tools_dir):
    tools_dir = os.path.join(os.path.expanduser(r"~\Desktop"), "OS26 Tools")

wsh = win32com.client.Dispatch("WScript.Shell")

# 1. Copy batch files to OS26 Tools
for bat in ["ENROLL_MY_FACE.bat", "TEST_FACE_UNLOCK.bat"]:
    src = os.path.join(workspace, bat)
    dst = os.path.join(tools_dir, bat)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {bat} to {tools_dir}")

# 2. Create nice shortcuts in OS26 Tools
sc_enroll = wsh.CreateShortcut(os.path.join(tools_dir, "1_Enroll_My_Face_ID.lnk"))
sc_enroll.TargetPath = os.path.join(tools_dir, "ENROLL_MY_FACE.bat")
sc_enroll.WorkingDirectory = workspace
sc_enroll.IconLocation = r"C:\Windows\System32\shell32.dll,266" # camera / biometric icon
sc_enroll.Description = "Scan and register your face with OS26 Face ID"
sc_enroll.Save()
print("Created shortcut: 1_Enroll_My_Face_ID.lnk")

sc_test = wsh.CreateShortcut(os.path.join(tools_dir, "2_Test_Face_Unlock.lnk"))
sc_test.TargetPath = os.path.join(tools_dir, "TEST_FACE_UNLOCK.bat")
sc_test.WorkingDirectory = workspace
sc_test.IconLocation = r"C:\Windows\System32\shell32.dll,47" # padlock / key icon
sc_test.Description = "Activate OS26 Face ID Lock Screen"
sc_test.Save()
print("Created shortcut: 2_Test_Face_Unlock.lnk")

# 3. Create Windows Startup shortcut so it guards on boot
startup = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
sc_boot = wsh.CreateShortcut(os.path.join(startup, "OS26FaceLockStartup.lnk"))
pyw = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\pythonw.exe"
lock_script = os.path.join(workspace, "src", "os26_face_lock.py")
sc_boot.TargetPath = pyw
sc_boot.Arguments = f'"{lock_script}"'
sc_boot.WorkingDirectory = workspace
sc_boot.IconLocation = r"C:\Windows\System32\shell32.dll,47"
sc_boot.Description = "OS26 Face ID Lock Screen on Boot"
sc_boot.Save()
print("Created Windows Startup shortcut for Face Lock on Boot:", sc_boot.FullName)
