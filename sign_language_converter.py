
"""
Real-Time Sign Language to Speech Converter
A comprehensive system for converting American Sign Language to text and speech
"""

import numpy as np
import math
import cv2
import os
import traceback
import pyttsx3
from keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
from string import ascii_uppercase
import enchant
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time

class SignLanguageConverter:
    def __init__(self):
        # Initialize core components
        self.setup_model()
        self.setup_detectors()
        self.setup_speech_engine()
        self.setup_variables()
        self.create_white_background()
        self.setup_gui()

    def setup_model(self):
        """Load the trained CNN model"""
        try:
            self.model = load_model('cnn8grps_rad1_model.h5')
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            messagebox.showerror("Error", "Failed to load model. Please ensure 'cnn8grps_rad1_model.h5' is in the directory.")

    def setup_detectors(self):
        """Initialize hand detection modules"""
        self.hd = HandDetector(maxHands=1)
        self.hd2 = HandDetector(maxHands=1)
        self.offset = 29

    def setup_speech_engine(self):
        """Initialize text-to-speech engine"""
        try:
            self.speak_engine = pyttsx3.init()
            self.speak_engine.setProperty("rate", 120)
            voices = self.speak_engine.getProperty("voices")
            if voices:
                self.speak_engine.setProperty("voice", voices[0].id)
        except Exception as e:
            print(f"Speech engine error: {e}")

    def setup_variables(self):
        """Initialize tracking variables"""
        # Character tracking
        self.ct = {}
        self.ct['blank'] = 0
        for i in ascii_uppercase:
            self.ct[i] = 0

        # Prediction variables
        self.blank_flag = 0
        self.space_flag = False
        self.next_flag = True
        self.prev_char = ""
        self.count = -1
        self.ten_prev_char = [" " for _ in range(10)]

        # Display variables
        self.text_sentence = ""
        self.current_symbol = "Ready"
        self.word_suggestions = ["", "", "", ""]
        self.current_word = ""

        # Dictionary for spell check
        try:
            self.dictionary = enchant.Dict("en-US")
        except:
            print("Warning: Dictionary not available for spell checking")
            self.dictionary = None

    def create_white_background(self):
        """Create white background image for skeleton drawing"""
        white = np.ones((400, 400, 3), np.uint8) * 255
        cv2.imwrite("white.jpg", white)

    def setup_gui(self):
        """Create the main GUI interface"""
        self.root = tk.Tk()
        self.root.title("Sign Language to Speech Converter")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')

        # Title
        title_label = tk.Label(
            self.root,
            text="Sign Language to Speech Converter",
            font=("Arial", 24, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)

        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left panel - Camera feed
        left_panel = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, padx=(0, 10), pady=10)

        # Camera display
        self.camera_label = tk.Label(left_panel, text="Camera Feed", bg='white')
        self.camera_label.pack(pady=10)

        # Right panel - Results and skeleton
        right_panel = tk.Frame(main_frame, bg='#f0f0f0')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Skeleton display
        skeleton_frame = tk.Frame(right_panel, bg='white', relief=tk.RAISED, bd=2)
        skeleton_frame.pack(pady=(0, 10))

        sk_title = tk.Label(skeleton_frame, text="Hand Skeleton", font=("Arial", 14, "bold"), bg='white')
        sk_title.pack(pady=5)

        self.skeleton_label = tk.Label(skeleton_frame, text="Skeleton View", bg='white')
        self.skeleton_label.pack(pady=10)

        # Results frame
        results_frame = tk.Frame(right_panel, bg='#e8f4fd', relief=tk.RAISED, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Current character
        char_frame = tk.Frame(results_frame, bg='#e8f4fd')
        char_frame.pack(pady=10)

        tk.Label(char_frame, text="Current Character:", font=("Arial", 14, "bold"), bg='#e8f4fd').pack(side=tk.LEFT)
        self.char_display = tk.Label(
            char_frame, 
            text=self.current_symbol, 
            font=("Arial", 18, "bold"), 
            bg='#e8f4fd',
            fg='#e74c3c'
        )
        self.char_display.pack(side=tk.LEFT, padx=10)

        # Sentence display
        sentence_frame = tk.Frame(results_frame, bg='#e8f4fd')
        sentence_frame.pack(pady=10, fill=tk.X)

        tk.Label(sentence_frame, text="Sentence:", font=("Arial", 14, "bold"), bg='#e8f4fd').pack(anchor=tk.W)
        self.sentence_display = tk.Text(
            sentence_frame,
            height=3,
            font=("Arial", 14),
            wrap=tk.WORD,
            bg='white',
            fg='#2c3e50'
        )
        self.sentence_display.pack(fill=tk.X, pady=5)

        # Word suggestions
        suggestions_frame = tk.Frame(results_frame, bg='#e8f4fd')
        suggestions_frame.pack(pady=10, fill=tk.X)

        tk.Label(suggestions_frame, text="Suggestions:", font=("Arial", 12, "bold"), bg='#e8f4fd', fg='#e67e22').pack(anchor=tk.W)

        self.suggestion_buttons = []
        for i in range(4):
            btn = tk.Button(
                suggestions_frame,
                text="",
                font=("Arial", 10),
                bg='#3498db',
                fg='white',
                command=lambda idx=i: self.apply_suggestion(idx)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.suggestion_buttons.append(btn)

        # Control buttons
        control_frame = tk.Frame(results_frame, bg='#e8f4fd')
        control_frame.pack(pady=20)

        self.speak_btn = tk.Button(
            control_frame,
            text="🔊 Speak",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            command=self.speak_text,
            width=10
        )
        self.speak_btn.pack(side=tk.LEFT, padx=10)

        self.clear_btn = tk.Button(
            control_frame,
            text="🗑️ Clear",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            command=self.clear_text,
            width=10
        )
        self.clear_btn.pack(side=tk.LEFT, padx=10)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Position your hand in front of the camera")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 10),
            bg='#34495e',
            fg='white'
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize camera
        self.vs = cv2.VideoCapture(0)
        self.current_image = None

        # Start video processing
        self.video_loop()

        # Handle window close
        self.root.protocol('WM_DELETE_WINDOW', self.cleanup)

    def distance(self, x, y):
        """Calculate Euclidean distance between two points"""
        return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

    def video_loop(self):
        """Main video processing loop"""
        try:
            ret, frame = self.vs.read()
            if ret:
                frame = cv2.flip(frame, 1)

                # Process frame
                self.process_frame(frame)

                # Update camera display
                self.update_camera_display(frame)

        except Exception as e:
            print(f"Video loop error: {e}")
            self.status_var.set(f"Error: {str(e)}")

        # Schedule next frame
        self.root.after(30, self.video_loop)

    def process_frame(self, frame):
        """Process video frame for hand detection and prediction"""
        hands = self.hd.findHands(frame, draw=False, flipType=True)

        if hands and hands[0]:
            hand = hands[0]
            bbox = hand['bbox']
            x, y, w, h = bbox

            # Extract hand region
            hand_region = frame[y - self.offset:y + h + self.offset, 
                             x - self.offset:x + w + self.offset]

            if hand_region.size > 0:
                # Create skeleton
                skeleton = self.create_skeleton(hand_region, w, h)
                if skeleton is not None:
                    # Make prediction
                    self.predict_gesture(skeleton)

                    # Update skeleton display
                    self.update_skeleton_display(skeleton)
        else:
            self.current_symbol = "No Hand Detected"
            self.char_display.config(text=self.current_symbol)

    def create_skeleton(self, hand_region, w, h):
        """Create hand skeleton from detected landmarks"""
        try:
            white = cv2.imread("white.jpg")
            if white is None:
                self.create_white_background()
                white = cv2.imread("white.jpg")

            # Detect hands in the region
            hands = self.hd2.findHands(hand_region, draw=False, flipType=True)

            if hands and hands[0]:
                hand = hands[0]
                pts = hand['lmList']

                # Calculate offset for centering
                os = ((400 - w) // 2) - 15
                os1 = ((400 - h) // 2) - 15

                # Draw skeleton lines
                self.draw_skeleton_lines(white, pts, os, os1)

                # Draw landmarks
                for i in range(21):
                    cv2.circle(white, (pts[i][0] + os, pts[i][1] + os1), 
                             3, (0, 0, 255), -1)

                return white

        except Exception as e:
            print(f"Skeleton creation error: {e}")

        return None

    def draw_skeleton_lines(self, image, pts, os, os1):
        """Draw skeleton lines connecting hand landmarks"""
        # Finger connections
        connections = [
            (0, 4), (5, 8), (9, 12), (13, 16), (17, 20),  # Finger lines
            (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)    # Palm connections
        ]

        # Draw finger segments
        for i in range(0, 4):
            cv2.line(image, (pts[i][0] + os, pts[i][1] + os1),
                    (pts[i + 1][0] + os, pts[i + 1][1] + os1), (0, 255, 0), 2)

        for start in range(5, 18, 4):
            for i in range(start, start + 3):
                cv2.line(image, (pts[i][0] + os, pts[i][1] + os1),
                        (pts[i + 1][0] + os, pts[i + 1][1] + os1), (0, 255, 0), 2)

        # Draw palm connections
        palm_connections = [(5, 9), (9, 13), (13, 17), (0, 5), (0, 17)]
        for start, end in palm_connections:
            cv2.line(image, (pts[start][0] + os, pts[start][1] + os1),
                    (pts[end][0] + os, pts[end][1] + os1), (0, 255, 0), 2)

    def predict_gesture(self, skeleton):
        """Predict gesture from skeleton image"""
        try:
            # Prepare image for prediction
            skeleton_rgb = cv2.cvtColor(skeleton, cv2.COLOR_BGR2RGB)
            skeleton_input = skeleton_rgb.reshape(1, 400, 400, 3)
            skeleton_input = skeleton_input.astype('float32') / 255.0

            # Get predictions
            prob = self.model.predict(skeleton_input)[0]

            # Get top predictions
            top_indices = np.argsort(prob)[-3:][::-1]
            ch1, ch2, ch3 = top_indices[0], top_indices[1], top_indices[2]

            # Apply gesture classification rules
            predicted_char = self.classify_gesture(ch1, ch2, skeleton)

            # Update character tracking
            self.update_character_tracking(predicted_char)

        except Exception as e:
            print(f"Prediction error: {e}")

    def classify_gesture(self, ch1, ch2, skeleton):
        """Apply classification rules to determine final character"""
        # This is a simplified version of the original classification logic
        # You would implement the full gesture classification rules here

        gesture_map = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'
        }

        return gesture_map.get(ch1, chr(65 + ch1) if ch1 < 26 else 'Unknown')

    def update_character_tracking(self, char):
        """Update character tracking and sentence building"""
        if char == self.prev_char:
            return

        self.current_symbol = char
        self.char_display.config(text=char)

        # Handle special characters
        if char == 'Space':
            if not self.text_sentence.endswith(' '):
                self.text_sentence += ' '
                self.update_word_suggestions()
        elif char not in ['Unknown', 'No Hand Detected']:
            self.text_sentence += char
            self.update_word_suggestions()

        self.prev_char = char
        self.update_sentence_display()

    def update_word_suggestions(self):
        """Update word suggestions based on current input"""
        if not self.dictionary:
            return

        try:
            # Get current word
            words = self.text_sentence.strip().split()
            if words:
                current_word = words[-1].lower()

                # Get suggestions
                suggestions = []
                if len(current_word) > 0:
                    # Try to get suggestions from dictionary
                    if not self.dictionary.check(current_word):
                        suggestions = self.dictionary.suggest(current_word)[:4]
                    else:
                        suggestions = [current_word]

                # Update suggestion buttons
                for i, btn in enumerate(self.suggestion_buttons):
                    if i < len(suggestions):
                        btn.config(text=suggestions[i], state='normal')
                    else:
                        btn.config(text="", state='disabled')

                self.word_suggestions = suggestions + [""] * (4 - len(suggestions))

        except Exception as e:
            print(f"Suggestion error: {e}")

    def apply_suggestion(self, index):
        """Apply selected word suggestion"""
        if index < len(self.word_suggestions) and self.word_suggestions[index]:
            words = self.text_sentence.strip().split()
            if words:
                words[-1] = self.word_suggestions[index].upper()
                self.text_sentence = ' '.join(words) + ' '
                self.update_sentence_display()

    def update_camera_display(self, frame):
        """Update camera display in GUI"""
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (640, 480))

            image = Image.fromarray(frame_resized)
            photo = ImageTk.PhotoImage(image=image)

            self.camera_label.config(image=photo, text="")
            self.camera_label.image = photo

        except Exception as e:
            print(f"Camera display error: {e}")

    def update_skeleton_display(self, skeleton):
        """Update skeleton display in GUI"""
        try:
            skeleton_rgb = cv2.cvtColor(skeleton, cv2.COLOR_BGR2RGB)
            skeleton_resized = cv2.resize(skeleton_rgb, (300, 300))

            image = Image.fromarray(skeleton_resized)
            photo = ImageTk.PhotoImage(image=image)

            self.skeleton_label.config(image=photo, text="")
            self.skeleton_label.image = photo

        except Exception as e:
            print(f"Skeleton display error: {e}")

    def update_sentence_display(self):
        """Update the sentence display"""
        self.sentence_display.delete(1.0, tk.END)
        self.sentence_display.insert(tk.END, self.text_sentence)

    def speak_text(self):
        """Convert text to speech"""
        if self.text_sentence.strip():
            try:
                # Run in separate thread to avoid blocking GUI
                def speak():
                    self.speak_engine.say(self.text_sentence)
                    self.speak_engine.runAndWait()

                thread = threading.Thread(target=speak)
                thread.daemon = True
                thread.start()

                self.status_var.set("Speaking...")
                self.root.after(3000, lambda: self.status_var.set("Ready"))

            except Exception as e:
                print(f"Speech error: {e}")
                messagebox.showerror("Error", "Speech synthesis failed")
        else:
            messagebox.showinfo("Info", "No text to speak")

    def clear_text(self):
        """Clear all text"""
        self.text_sentence = ""
        self.current_symbol = "Ready"
        self.word_suggestions = ["", "", "", ""]

        self.update_sentence_display()
        self.char_display.config(text=self.current_symbol)

        for btn in self.suggestion_buttons:
            btn.config(text="", state='disabled')

        self.status_var.set("Text cleared - Ready")

    def cleanup(self):
        """Clean up resources before closing"""
        try:
            if hasattr(self, 'vs') and self.vs.isOpened():
                self.vs.release()
            cv2.destroyAllWindows()
        except:
            pass
        finally:
            self.root.quit()
            self.root.destroy()

    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")
        finally:
            self.cleanup()

def main():
    """Main function to run the application"""
    print("Starting Sign Language to Speech Converter...")
    print("Make sure you have:")
    print("1. A webcam connected")
    print("2. The model file 'cnn8grps_rad1_model.h5' in the same directory")
    print("3. All required packages installed")

    try:
        app = SignLanguageConverter()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")

if __name__ == "__main__":
    main()
