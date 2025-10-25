#!/usr/bin/env python3
"""
Sign Language Converter - Easy Launcher
Double-click this file to run the application
"""

import sys
import os
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'cv2', 'numpy', 'tensorflow', 'keras', 
        'pyttsx3', 'cvzone', 'PIL', 'enchant'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)

    return missing_packages

def main():
    print("🤟 Sign Language to Speech Converter")
    print("=" * 50)

    # Check if model file exists
    if not os.path.exists("cnn8grps_rad1_model.h5"):
        print("❌ Error: Model file 'cnn8grps_rad1_model.h5' not found!")
        print("Please make sure the model file is in the same directory.")
        input("Press Enter to exit...")
        return

    # Check requirements
    print("Checking requirements...")
    missing = check_requirements()

    if missing:
        print("❌ Missing packages detected:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nWould you like to install them? (y/n): ", end="")

        choice = input().lower()
        if choice == 'y' or choice == 'yes':
            print("Installing packages...")
            try:
                subprocess.check_call([sys.executable, "install.py"])
            except Exception as e:
                print(f"Installation failed: {e}")
                input("Press Enter to exit...")
                return
        else:
            print("Please install the required packages first.")
            input("Press Enter to exit...")
            return

    # Launch the main application
    print("✅ All requirements satisfied!")
    print("🚀 Launching Sign Language Converter...")

    try:
        import sign_language_converter
        sign_language_converter.main()
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure all files are in the same directory")
        print("2. Check that your webcam is connected")
        print("3. Try running 'python install.py' first")
        input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...")
