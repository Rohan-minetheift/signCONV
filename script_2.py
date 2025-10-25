# Create an enhanced requirements.txt with specific versions

enhanced_requirements = '''# Sign Language to Speech Converter - Requirements
# Core dependencies for the application

# Computer vision and image processing
opencv-python==4.8.1.78
cvzone==1.6.1

# Machine learning and neural networks  
tensorflow==2.13.0
keras==2.13.1
numpy==1.24.3

# GUI and image handling
tkinter  # Usually comes with Python
Pillow==10.0.1
matplotlib==3.7.2

# Text to speech
pyttsx3==2.90

# Language processing and spell checking
pyenchant==3.2.2

# Utility libraries
scipy==1.11.2
scikit-learn==1.3.0

# Optional: For better performance
numba==0.57.1

# Development and debugging (optional)
# jupyter==1.0.0
# ipywidgets==8.1.1
'''

# Save enhanced requirements
with open('requirements_enhanced.txt', 'w') as f:
    f.write(enhanced_requirements)

# Create a simple installation script
install_script = '''#!/usr/bin/env python3
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
    
    print("\\nInstalling required packages...")
    
    failed_packages = []
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✓ {package} installed successfully")
        else:
            print(f"✗ Failed to install {package}")
            failed_packages.append(package)
    
    print("\\n" + "=" * 60)
    
    if failed_packages:
        print("⚠️  Some packages failed to install:")
        for package in failed_packages:
            print(f"  - {package}")
        print("\\nPlease install them manually using:")
        print("pip install <package_name>")
    else:
        print("✅ All packages installed successfully!")
    
    # Check for model file
    print("\\nChecking for required files...")
    
    if os.path.exists("cnn8grps_rad1_model.h5"):
        print("✓ Model file found: cnn8grps_rad1_model.h5")
    else:
        print("⚠️  Model file not found: cnn8grps_rad1_model.h5")
        print("Please ensure the model file is in the same directory")
    
    # Check camera
    print("\\nTesting camera access...")
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
    
    print("\\n" + "=" * 60)
    print("Installation complete!")
    print("Run the application with: python sign_language_converter.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
'''

# Save installation script
with open('install.py', 'w') as f:
    f.write(install_script)

print("Created: requirements_enhanced.txt")
print("Created: install.py")
print("Installation files created successfully!")