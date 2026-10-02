"""
OS26 Liquid Glass Theme - Master Automated Build & Packaging Pipeline
Compiles the desktop application into standalone binaries and builds the
self-contained Windows installer (dist/windows/OS26-Liquid-Glass-Setup.exe).
"""

import os
import sys
import shutil
import subprocess
import time

ROOT = r"c:\Users\bhara\OneDrive\Documents\llll"
PYINSTALLER_EXE = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\Scripts\pyinstaller.exe"
ISCC_EXE = r"C:\Users\bhara\AppData\Local\Programs\Inno Setup 6\ISCC.exe"

def run_step(step_name, func):
    print(f"\n=======================================================")
    print(f"[*] STEP: {step_name}")
    print(f"=======================================================")
    t0 = time.time()
    res = func()
    elapsed = time.time() - t0
    print(f"[+] Completed: {step_name} in {elapsed:.1f}s\n")
    return res

def step_prepare_assets():
    # Run init_build_structure.py
    init_script = os.path.join(ROOT, "init_build_structure.py")
    subprocess.check_call([sys.executable, init_script], cwd=ROOT)
    # Ensure src has all engine scripts
    engines = [
        "desktop_zoom_dock.py",
        "desktop_icon_vibrator.py",
        "mac_brightness_engine.py",
        "apply_full_system_customization.py",
        "apply_fe_styles_elevated.py",
        "install_and_style_all_mods.py",
        "rebuild_icon_cache.py",
        "start_desktop_icon_vibrator.py",
        "stop_desktop_icon_vibrator.py"
    ]
    for eng in engines:
        src_path = os.path.join(ROOT, eng)
        dst_path = os.path.join(ROOT, "src", eng)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)

def step_compile_pyinstaller():
    app_script = os.path.join(ROOT, "src", "os26_app.py")
    icon_file = os.path.join(ROOT, "assets", "icons", "start_menu.ico")
    dist_bin = os.path.join(ROOT, "dist", "bin")
    work_dir = os.path.join(ROOT, "build", "pyinstaller")
    spec_dir = os.path.join(ROOT, "build")

    os.makedirs(dist_bin, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)

    cmd = [
        PYINSTALLER_EXE,
        "--noconsole",
        "--onedir",
        "--name=OS26-Liquid-Glass",
        f"--icon={icon_file}",
        f"--distpath={dist_bin}",
        f"--workpath={work_dir}",
        f"--specpath={spec_dir}",
        "--clean",
        "-y",
        app_script
    ]
    print("Running PyInstaller:", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)

    # Copy src engines next to the executable in dist/bin/OS26-Liquid-Glass so relative imports/spawns work
    app_bundle_dir = os.path.join(dist_bin, "OS26-Liquid-Glass")
    for item in os.listdir(os.path.join(ROOT, "src")):
        src_f = os.path.join(ROOT, "src", item)
        dst_f = os.path.join(app_bundle_dir, item)
        if os.path.isfile(src_f) and not os.path.exists(dst_f):
            shutil.copy2(src_f, dst_f)

def step_build_installer():
    iss_file = os.path.join(ROOT, "installer", "setup.iss")
    if not os.path.exists(ISCC_EXE):
        raise FileNotFoundError(f"Inno Setup Compiler not found at: {ISCC_EXE}")

    cmd = [ISCC_EXE, iss_file]
    print("Running Inno Setup Compiler:", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)

    installer_output = os.path.join(ROOT, "dist", "windows", "OS26-Liquid-Glass-Setup.exe")
    if os.path.exists(installer_output):
        size_mb = os.path.getsize(installer_output) / (1024 * 1024)
        print(f"\n[SUCCESS] Windows Installer created: {installer_output} ({size_mb:.2f} MB)")
        return installer_output
    else:
        raise FileNotFoundError(f"Installer was not found at {installer_output}")

def main():
    print("*******************************************************************")
    print("   OS26 LIQUID GLASS THEME: REPRODUCIBLE MASTER BUILD PIPELINE    ")
    print("*******************************************************************")
    run_step("1. Preparing Assets and Build Structure", step_prepare_assets)
    run_step("2. Compiling Desktop App with PyInstaller", step_compile_pyinstaller)
    installer_path = run_step("3. Generating Windows Installer with Inno Setup", step_build_installer)
    print("*******************************************************************")
    print(f" BUILD COMPLETED SUCCESSFULLY!")
    print(f" Shareable Installer: {installer_path}")
    print("*******************************************************************")

if __name__ == "__main__":
    main()
