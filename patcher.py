#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CRACK_PACKAGE = SCRIPT_DIR / "crack_package"

VST_INSTALLED = Path(r"C:\Program Files\Common Files\VST3\Bass Bully VST\Bass Bully Premium.vst3")
ROM_INSTALLED = Path(r"C:\ProgramData\Bass Bully VST\Bass Bully Premium\Bass Bully Premium.rom")

VST3_DEST = Path(r"C:\Program Files\Common Files\VST3\Bass Bully VST")
ROM_DEST = Path(r"C:\ProgramData\Bass Bully VST\Bass Bully Premium")

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def extract_files():
    print("[*] extracting files from installed location...")

    if not VST_INSTALLED.exists():
        print(f"[!] vst not found at: {VST_INSTALLED}")
        print("[*] run the installer first, then run this script again")
        return False

    if not ROM_INSTALLED.exists():
        print(f"[!] rom not found at: {ROM_INSTALLED}")
        return False

    CRACK_PACKAGE.mkdir(exist_ok=True)

    vst_dest = CRACK_PACKAGE / "Bass Bully Premium.vst3"
    if vst_dest.exists():
        shutil.rmtree(vst_dest)
    shutil.copytree(VST_INSTALLED, vst_dest)
    print(f"[+] copied vst3 -> {vst_dest}")

    rom_dest = CRACK_PACKAGE / "Bass Bully Premium.rom"
    shutil.copy2(ROM_INSTALLED, rom_dest)
    print(f"[+] copied rom  -> {rom_dest}")

    dll = vst_dest / "Contents" / "x86_64-win" / "Bass Bully Premium.vst3"
    if dll.exists():
        print(f"\n[+] extraction successful!")
        print(f"[*] vst dll: {dll.stat().st_size:,} bytes")
        print(f"[*] rom:     {rom_dest.stat().st_size:,} bytes")
        return True
    else:
        print("[!] extraction failed - dll not found in bundle")
        return False

def deploy_files():
    print("[*] deploying cracked files...")

    vst_src = CRACK_PACKAGE / "Bass Bully Premium.vst3"
    rom_src = CRACK_PACKAGE / "Bass Bully Premium.rom"

    if not vst_src.exists():
        print(f"[!] crack_package not found")
        print("[*] run --extract first to grab files from an installation")
        return False

    if not rom_src.exists():
        print(f"[!] rom not in crack_package")
        return False

    VST3_DEST.mkdir(parents=True, exist_ok=True)
    ROM_DEST.mkdir(parents=True, exist_ok=True)

    vst_target = VST3_DEST / "Bass Bully Premium.vst3"
    if vst_target.exists():
        shutil.rmtree(vst_target)
    shutil.copytree(vst_src, vst_target)
    print(f"[+] vst3 -> {vst_target}")

    rom_target = ROM_DEST / "Bass Bully Premium.rom"
    shutil.copy2(rom_src, rom_target)
    print(f"[+] rom  -> {rom_target}")

    return True

def verify():
    dll = VST3_DEST / "Bass Bully Premium.vst3" / "Contents" / "x86_64-win" / "Bass Bully Premium.vst3"
    rom = ROM_DEST / "Bass Bully Premium.rom"

    if dll.exists() and rom.exists():
        print("\n[+] installation verified")
        return True
    else:
        print("\n[!] verification failed")
        return False

def main():
    parser = argparse.ArgumentParser(description="Bass Bully Premium Crack")
    parser.add_argument('--extract', action='store_true', help='extract files from installed location')
    parser.add_argument('--deploy', action='store_true', help='deploy crack_package to vst directories')
    args = parser.parse_args()

    if not args.extract and not args.deploy:
        parser.print_help()
        return 0

    print("=" * 50)
    print("bass bully premium - crack")
    print("=" * 50)
    print()

    if args.extract:
        if not extract_files():
            return 1

    if args.deploy:
        if not is_admin():
            print("\n[!] --deploy requires administrator privileges")
            print("[*] right-click -> run as administrator")
            return 1

        if not deploy_files():
            return 1

        if not verify():
            return 1

    print()
    print("=" * 50)
    print("[+] COMPLETE")
    print("=" * 50)
    print()
    if args.extract and not args.deploy:
        print("files extracted to crack_package/")
        print("run with --deploy (as admin) to install")
    else:
        print("load bass bully premium in your daw.")
        print("no registration required.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
