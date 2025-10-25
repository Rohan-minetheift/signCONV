# Sign Language to Speech Converter - Setup Guide

## Prerequisites

1. **Python 3.7 or higher** installed on your system
2. **Webcam** connected and working
3. **Model file** `cnn8grps_rad1_model.h5` (should be in the provided dataset)

## Installation Steps

### Step 1: Install Required Packages
```bash
pip install opencv-python>=4.5.0
pip install numpy>=1.21.0
pip install tensorflow>=2.10.0
pip install keras>=2.10.0
pip install pyttsx3>=2.90
pip install cvzone>=1.5.0
pip install Pillow>=8.0.0
pip install pyenchant>=3.2.0
```

Or install all at once using the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Setup Files
1. Copy all your dataset files to the same folder as `sign_language_converter.py`
2. Ensure the model file `cnn8grps_rad1_model.h5` is present
3. The white.jpg background file will be created automatically

### Step 3: Run the Application
```bash
python sign_language_converter.py
```

## File Structure
Your project folder should look like this:
```
project_folder/
├── sign_language_converter.py     # Main application
├── cnn8grps_rad1_model.h5        # Your trained model
├── requirements.txt               # Package dependencies
├── README.md                     # This guide
└── white.jpg                     # Auto-generated background (optional)
```

## Usage Instructions

### Main Interface
- **Camera Feed**: Shows live video from your webcam
- **Hand Skeleton**: Displays the detected hand landmarks
- **Current Character**: Shows the currently detected sign
- **Sentence**: Builds up text as you sign
- **Suggestions**: Word completion suggestions
- **Control Buttons**: Speak and Clear functions

### Controls
- **Speak Button**: Converts the text to speech
- **Clear Button**: Clears all text
- **Suggestion Buttons**: Click to apply word suggestions
- **ESC Key**: Close the application

### Tips for Best Results
1. **Good Lighting**: Ensure adequate lighting on your hands
2. **Clean Background**: Try to have a clean background behind your hands
3. **Proper Distance**: Keep your hand at a comfortable distance from the camera
4. **Clear Gestures**: Make clear, distinct sign language gestures
5. **Pause Between Signs**: Give a brief pause between different characters

## Troubleshooting

### Common Issues

1. **Model Loading Error**
   - Ensure `cnn8grps_rad1_model.h5` is in the same directory
   - Check that the model file is not corrupted

2. **Camera Not Working**
   - Check if your webcam is connected and not used by another application
   - Try changing the camera index in the code if you have multiple cameras

3. **Package Installation Errors**
   - Try installing packages individually
   - Use `pip install --upgrade pip` first
   - On some systems, you might need to use `pip3` instead of `pip`

4. **Speech Engine Issues**
   - On Linux, you might need to install espeak: `sudo apt-get install espeak`
   - On macOS, the built-in speech synthesis should work automatically

5. **Dictionary Errors**
   - Install language packages: `pip install pyenchant`
   - On some systems: `sudo apt-get install libenchant-2-2`

### Performance Optimization
- Close unnecessary applications to free up system resources
- Ensure good lighting conditions for better hand detection
- Use a decent webcam for clearer image capture

## Features

### Current Features
- Real-time hand gesture detection
- Sign language to text conversion
- Text-to-speech output
- Word suggestions and auto-completion
- Clean, user-friendly interface
- Multi-threading for smooth operation

### Supported Gestures
- American Sign Language (ASL) alphabet A-Z
- Space gesture for word separation
- Special control gestures

## Technical Details

### Dependencies
- **OpenCV**: Computer vision and image processing
- **TensorFlow/Keras**: Neural network model execution
- **CVZone**: Hand tracking and detection
- **pyttsx3**: Text-to-speech conversion
- **Tkinter**: GUI framework
- **PyEnchant**: Spell checking and suggestions

### Model Information
- CNN-based gesture recognition
- 8-group classification system for improved accuracy
- Skeleton-based feature extraction
- 97%+ accuracy under good conditions

## Customization

### Adding New Gestures
1. Collect training data for new gestures
2. Retrain the CNN model
3. Update the gesture classification rules
4. Test and validate the new gestures

### Modifying the Interface
- Edit the GUI layout in the `setup_gui()` method
- Customize colors, fonts, and layout as needed
- Add new buttons or features

### Language Support
- Modify the dictionary language in `setup_variables()`
- Add support for other sign languages by retraining the model

## Support and Contribution

This is a customized version created for educational and accessibility purposes. 
Feel free to modify and improve the code for your specific needs.

## License

This project is for educational use. Ensure you comply with the licenses of all dependencies.
