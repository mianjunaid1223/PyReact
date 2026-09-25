import os
import sys
import subprocess
import argparse
import platform
import shutil

def run_command(command):
    print(f"Running: {command}")
    subprocess.check_call(command, shell=True)

def build_desktop():
    print("Building for Desktop (Windows/Mac/Linux)...")
    run_command(f"{sys.executable} -m pip install pyinstaller pywebview")
    
    bootstrapper_code = """
import os
import sys
import threading
import time
import webview
import uvicorn
from app import app

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=3000, log_level="warning")

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    time.sleep(2)
    
    webview.create_window("PyReact App", "http://127.0.0.1:3000")
    webview.start()
"""
    with open("desktop_bootstrapper.py", "w") as f:
        f.write(bootstrapper_code)

    separator = ";" if platform.system() == "Windows" else ":"
    build_cmd = (
        f"{sys.executable} -m PyInstaller "
        f"--noconfirm --onedir --windowed "
        f"--add-data \"static{separator}static\" "
        f"--add-data \"index.html{separator}.\" "
        f"--add-data \"components{separator}components\" "
        f"desktop_bootstrapper.py"
    )
    
    run_command(build_cmd)
    
    print("\\nDesktop Build Complete! Check the 'dist' folder.")
    os.remove("desktop_bootstrapper.py")

def build_mobile(target="android"):
    print(f"Building for Mobile ({target})...")
    run_command(f"{sys.executable} -m pip install briefcase")
    
    print("Initializing Briefcase project...")
    app_name = "pyreact_mobile"
    toml_content = f"""
[tool.briefcase]
project_name = "PyReact Mobile"
bundle = "com.pyreact.app"
version = "0.1.0"
url = "https://pyreact.dev"
license = "MIT"
author = "PyReact"

[tool.briefcase.app.{app_name}]
formal_name = "PyReact Mobile"
description = "A fast, compiled mobile app built on PyReact"
icon = "briefcase_icon"
sources = ["static", "components", "app.py", "pyreact.py"]
requires = ["fastapi", "uvicorn", "websockets"]
"""
    with open("pyproject.toml", "w") as f:
        f.write(toml_content)
        
    print(f"To compile for mobile natively, run: `briefcase create {target}` followed by `briefcase build {target}`")
    try:
        run_command(f"{sys.executable} -m briefcase create {target}")
        run_command(f"{sys.executable} -m briefcase build {target}")
        print(f"\\nMobile Build ({target}) Complete! Check the platform folders.")
    except Exception as e:
        print(f"Note: compiling mobile requires native SDKs (e.g. Android Studio or Xcode). Ensure they are configured. Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyReact Universal Compiler")
    parser.add_argument("target", choices=["desktop", "android", "ios"], help="Target platform to build")
    
    args = parser.parse_args()
    
    if args.target == "desktop":
        build_desktop()
    elif args.target in ["android", "ios"]:
        build_mobile(args.target)
