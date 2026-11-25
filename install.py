import sys
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(command, **kwargs):
    print(f"\n> {' '.join(map(str, command))}")
    subprocess.run(command, check=True, **kwargs)

def main():
    # Locate Android Debug Bridge
    adb = shutil.which("adb")

    if not adb:
        print("ERROR: ADB not found.")
        print("Please install Android SDK Platform Tools and add adb to PATH.")
        sys.exit(1)

    # Select the correct Gradle wrapper
    if sys.platform == "win32":
        wrapper = ROOT / "gradlew.bat"
        command = ["cmd", "/c", str(wrapper)]
    else:
        wrapper = ROOT / "gradlew"
        command = ["bash", str(wrapper)]

    if not wrapper.exists():
        print("ERROR: Gradle wrapper not found.")
        sys.exit(1)

    try:
        # Build the debug APK
        run(command + ["assembleDebug"], cwd=ROOT)

        apk = ROOT / "app/build/outputs/apk/debug/app-debug.apk"

        if not apk.exists():
            raise FileNotFoundError(f"APK not found: {apk}")

        # Check connected devices
        result = subprocess.run(
            [adb, "devices"],
            capture_output=True,
            text=True,
            check=True
        )

        devices = [
            line.split()[0]
            for line in result.stdout.splitlines()[1:]
            if "\tdevice" in line
        ]

        if not devices:
            print("ERROR: No authorized Android device found.")
            sys.exit(1)

        # Install APK
        run([adb, "install", str(apk)])

        print("\nSUCCESS! Module installed.")

    except subprocess.CalledProcessError:
        print("\nERROR: Build or installation failed.")
        sys.exit(1)

    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
