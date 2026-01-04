#!/usr/bin/env python3
"""
Installer for lockstr command
"""

import os
import sys
import platform
import shutil


def check_dependencies():
    """Check for required packages"""
    required_packages = ['cryptography', 'pyperclip']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\nMissing dependencies:")
        for package in missing:
            print(f"  ✗ {package}")
        
        print(f"\nInstall with: {sys.executable} -m pip install {' '.join(missing)}")
        
        if platform.system() == "Linux":
            print("\n📋 Linux clipboard support (optional but recommended):")
            print("  For X11:      sudo apt install xclip")
            print("  For Wayland:  sudo apt install wl-clipboard")
        
        return False
    
    return True


def get_install_dir():
    """Get appropriate installation directory"""
    system = platform.system()
    
    if system == "Windows":
        python_dir = os.path.dirname(sys.executable)
        scripts_dir = os.path.join(python_dir, "Scripts")
        if os.path.exists(scripts_dir):
            return scripts_dir
        
        home = os.path.expanduser("~")
        user_bin = os.path.join(home, "bin")
        os.makedirs(user_bin, exist_ok=True)
        return user_bin
    
    else:
        if os.geteuid() == 0:
            return "/usr/local/bin"
        
        if os.access("/usr/local/bin", os.W_OK):
            return "/usr/local/bin"
        
        home = os.path.expanduser("~")
        local_bin = os.path.join(home, ".local", "bin")
        os.makedirs(local_bin, exist_ok=True)
        return local_bin


def check_in_path(directory):
    """Check if directory is in PATH"""
    path_env = os.environ.get("PATH", "")
    path_dirs = path_env.split(os.pathsep)
    return directory in path_dirs


def create_wrapper(install_dir, script_path):
    """Create platform-specific wrapper"""
    system = platform.system()
    
    if system == "Windows":
        wrapper = os.path.join(install_dir, "lockstr.bat")
        content = f'''@echo off
"{sys.executable}" "{script_path}" %*
'''
        with open(wrapper, "w", encoding="utf-8") as f:
            f.write(content)
        return wrapper
    
    else:
        wrapper = os.path.join(install_dir, "lockstr")
        content = f'''#!/bin/sh
"{sys.executable}" "{script_path}" "$@"
'''
        with open(wrapper, "w", encoding="utf-8") as f:
            f.write(content)
        os.chmod(wrapper, 0o755)
        return wrapper


def add_to_path(install_dir):
    """Instructions for adding directory to PATH"""
    system = platform.system()
    
    print(f"\n⚠️  {install_dir} is not in your PATH")
    
    if system == "Windows":
        print(f"\nTo add to PATH permanently:")
        print(f"1. Press Win + X, select 'System'")
        print(f"2. Click 'Advanced system settings'")
        print(f"3. Click 'Environment Variables'")
        print(f"4. Under 'User variables', select 'Path'")
        print(f"5. Click 'Edit' and add: {install_dir}")
        print(f"6. Restart your terminal")
    
    elif system == "Darwin":
        shell = os.environ.get("SHELL", "").split("/")[-1]
        rc_file = "~/.zshrc" if shell == "zsh" else "~/.bash_profile"
        
        print(f"\nAdd to {rc_file}:")
        print(f'  echo \'export PATH="{install_dir}:$PATH"\' >> {rc_file}')
        print(f"  source {rc_file}")
    
    else:
        shell = os.environ.get("SHELL", "").split("/")[-1]
        rc_file = "~/.bashrc" if shell == "bash" else "~/.zshrc"
        
        print(f"\nAdd to {rc_file}:")
        print(f'  echo \'export PATH="{install_dir}:$PATH"\' >> {rc_file}')
        print(f"  source {rc_file}")


def main():
    print("🔐 Installing lockstr - File Encryption Tool")
    print("=" * 50)
    print("Features:")
    print("  ✓ Magic header prevents double-encryption")
    print("  ✓ Keys never displayed (clipboard only)")
    print("  ✓ Recursive directory processing")
    print("  ✓ Dry-run mode for safety")
    print("=" * 50)
    
    if sys.version_info < (3, 6):
        print("Error: Python 3.6+ required")
        sys.exit(1)
    
    if not check_dependencies():
        print("\nPlease install dependencies first")
        response = input("Install now? [Y/n]: ").strip().lower()
        if response in ('', 'y', 'yes'):
            for package in ['cryptography', 'pyperclip']:
                os.system(f"{sys.executable} -m pip install {package}")
        else:
            sys.exit(1)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "lockstr.py")
    
    if not os.path.exists(main_script):
        print(f"Error: lockstr.py not found in {script_dir}")
        sys.exit(1)
    
    install_dir = get_install_dir()
    print(f"\n📁 Installation directory: {install_dir}")
    
    os.makedirs(install_dir, exist_ok=True)
    
    dest_script = os.path.join(install_dir, "lockstr.py")
    try:
        shutil.copy2(main_script, dest_script)
        print(f"✓ Script copied to {dest_script}")
    except PermissionError:
        print(f"\nPermission denied: {install_dir}")
        print("Try: sudo python install_lockstr.py")
        sys.exit(1)
    
    wrapper = create_wrapper(install_dir, dest_script)
    print(f"✓ Wrapper created: {wrapper}")
    
    if check_in_path(install_dir):
        print(f"\n✅ Installation complete!")
        print(f"\n📖 Usage examples:")
        print(f"  lockstr encrypt secret.txt")
        print(f"  lockstr decrypt secret.txt --confirm")
        print(f"  lockstr encrypt ./folder/ --dry-run --include-hidden")
        print(f"  lockstr decrypt ./encrypted/ --continue-on-error")
        print(f"  lockstr (shows help with banner)")
    else:
        add_to_path(install_dir)
        print(f"\n✅ Installation complete after PATH setup")
    
    print("\n" + "=" * 50)
    print("⚠️  IMPORTANT: Test with --dry-run first!")
    print("   Always backup important files before encryption.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled")
        sys.exit(1)
