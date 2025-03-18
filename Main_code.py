import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

class AttendanceSystem:
    def __init__(self):
        """Initialize the attendance system"""
        # Create necessary directories if they don't exist
        self.face_database_dir = Path("face_database")
        self.attendance_dir = Path("attendance")
        self.face_database_dir.mkdir(exist_ok=True)
        self.attendance_dir.mkdir(exist_ok=True)
        
        # Initialize storage for known faces
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Load known faces on initialization
        self.load_known_faces()
        
        # Initialize attendance file path
        self.attendance_file = self.attendance_dir / f"attendance_{datetime.now().strftime('%Y-%m')}.xlsx"
        self.initialize_attendance_file()

    def load_known_faces(self):
        """Load and encode all known faces from the face_database directory"""
        print("Loading known faces...")
        
        # Check if face_database directory is empty
        if not any(self.face_database_dir.iterdir()):
            print("Warning: No faces found in database. Please add face images to face_database directory.")
            return

        # Load each image file from the face_database directory
        for image_file in self.face_database_dir.glob("*.jpg"):
            try:
                # Get person's name from filename (removing .jpg extension)
                name = image_file.stem
                
                # Load and encode face
                image = face_recognition.load_image_file(str(image_file))
                face_encodings = face_recognition.face_encodings(image)
                
                if face_encodings:
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append(name)
                    print(f"Loaded face for: {name}")
                else:
                    print(f"No face found in image: {image_file}")
                    
            except Exception as e:
                print(f"Error loading face from {image_file}: {str(e)}")

        print(f"Loaded {len(self.known_face_names)} faces successfully")

    def initialize_attendance_file(self):
        """Create or load the attendance Excel file"""
        if not self.attendance_file.exists():
            # Create new attendance file with headers
            df = pd.DataFrame(columns=['Name', 'Date', 'Time'])
            df.to_excel(self.attendance_file, index=False)
            print(f"Created new attendance file: {self.attendance_file}")

    def mark_attendance(self, name):
        """Mark attendance for a recognized person"""
        try:
            # Read existing attendance file
            df = pd.read_excel(self.attendance_file)
            
            # Get current date and time
            now = datetime.now()
            date_str = now.strftime('%Y-%m-%d')
            time_str = now.strftime('%H:%M:%S')
            
            # Check if attendance already marked for today
            today_attendance = df[(df['Name'] == name) & (df['Date'] == date_str)]
            if today_attendance.empty:
                # Add new attendance record
                new_record = pd.DataFrame({
                    'Name': [name],
                    'Date': [date_str],
                    'Time': [time_str]
                })
                df = pd.concat([df, new_record], ignore_index=True)
                df.to_excel(self.attendance_file, index=False)
                print(f"Marked attendance for {name}")
                return True
            else:
                print(f"Attendance already marked for {name} today")
                return False
                
        except Exception as e:
            print(f"Error marking attendance: {str(e)}")
            return False

    def process_frame(self, frame):
        """Process a single frame for face recognition"""
        # Convert BGR frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        # Initialize list for names of recognized people
        face_names = []
        
        # Check each face found in the frame
        for face_encoding in face_encodings:
            # Compare with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            
            if True in matches:
                # Find the first matching face
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                
                # Mark attendance for recognized person
                self.mark_attendance(name)
            
            face_names.append(name)
        
        return face_locations, face_names

    def run(self):
        """Run the attendance system with webcam feed"""
        print("Starting attendance system...")
        
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        try:
            while True:
                # Read frame from webcam
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                # Process frame for face recognition
                face_locations, face_names = self.process_frame(frame)
                
                # Draw results on frame
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Draw rectangle around face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    
                    # Draw name below face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), 
                              cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
                
                # Display the frame
                cv2.imshow('Attendance System', frame)
                
                # Break loop on 'q' press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        finally:
            # Clean up
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create and run attendance system
    attendance_system = AttendanceSystem()
    attendance_system.run()
