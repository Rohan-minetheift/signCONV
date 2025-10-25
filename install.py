#!/usr/bin/env python3
"""
Automated installation script for Sign Language to Speech Converter
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main installation function"""
    print("=" * 60)
    print("Sign Language to Speech Converter - Installation Script")
    print("=" * 60)

    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required!")
        sys.exit(1)

    print(f"Python version: {sys.version}")

    # Required packages
    packages = [
        "opencv-python>=4.5.0",
        "numpy>=1.21.0", 
        "tensorflow>=2.10.0",
        "keras>=2.10.0",
        "pyttsx3>=2.90",
        "cvzone>=1.5.0",
        "Pillow>=8.0.0",
        "pyenchant>=3.2.0",
        "scipy>=1.7.0",
        "matplotlib>=3.5.0"
    ]

    print("\nInstalling required packages...")

    failed_packages = []
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✓ {package} installed successfully")
        else:
            print(f"✗ Failed to install {package}")
            failed_packages.append(package)

    print("\n" + "=" * 60)

    if failed_packages:
        print("⚠️  Some packages failed to install:")
        for package in failed_packages:
            print(f"  - {package}")
        print("\nPlease install them manually using:")
        print("pip install <package_name>")
    else:
        print("✅ All packages installed successfully!")

    # Check for model file
    print("\nChecking for required files...")

    if os.path.exists("cnn8grps_rad1_model.h5"):
        print("✓ Model file found: cnn8grps_rad1_model.h5")
    else:
        print("⚠️  Model file not found: cnn8grps_rad1_model.h5")
        print("Please ensure the model file is in the same directory")

    # Check camera
    print("\nTesting camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera access successful")
            cap.release()
        else:
            print("⚠️  Camera access failed - please check your webcam")
    except ImportError:
        print("⚠️  OpenCV not available for camera test")

    print("\n" + "=" * 60)
    print("Installation complete!")
    print("Run the application with: python sign_language_converter.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
