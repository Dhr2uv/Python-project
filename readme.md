# Facial Recognition Attendance System

A simple facial recognition-based attendance system that captures attendance using webcam and stores it in an Excel file.

## Features
- Real-time face detection and recognition
- Automatic attendance marking in Excel
- Support for multiple faces
- Simple console interface with visual feedback

## Setup Instructions

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add face images:
- Create photos of people whose attendance needs to be tracked
- Save them in the `face_database` directory
- Name the files as `PersonName.jpg` (e.g., "John_Smith.jpg")
- Make sure each image contains only one clear face

## Directory Structure
```
attendance_system/
├── face_database/     # Store face images here
├── attendance/        # Attendance Excel files are saved here
├── main.py           # Main application file
├── requirements.txt  # Project dependencies
└── README.md        # This file
```

## Usage

1. Make sure you have added face images to the `face_database` directory.

2. Run the application:
```bash
python main.py
```

3. The system will:
   - Load known faces from the database
   - Open your webcam
   - Start detecting and recognizing faces
   - Mark attendance automatically when a known face is detected

4. Controls:
   - Press 'q' to quit the application
   - Attendance is automatically saved to an Excel file in the `attendance` directory

## Attendance Records

- Attendance is stored in Excel files named `attendance_YYYY-MM.xlsx`
- A new file is created for each month
- Each record contains:
  - Name of the person
  - Date of attendance
  - Time of detection
- Duplicate entries for the same person on the same day are prevented

## Troubleshooting

1. If the webcam doesn't open:
   - Check if another application is using the webcam
   - Try closing other applications that might be using the camera
   - Verify your webcam is properly connected

2. If faces aren't being recognized:
   - Ensure the face database contains clear, well-lit photos
   - Check that image files are named correctly
   - Make sure there's good lighting when using the system

3. If dependencies fail to install:
   - Make sure you have CMake installed for the face_recognition library
   - On Windows, you might need Visual C++ build tools
   - Try installing dependencies one by one to identify any specific issues

## Notes

- The system uses a tolerance value of 0.6 for face recognition (can be adjusted in the code)
- Better lighting conditions will improve recognition accuracy
- The system can handle multiple faces simultaneously
- Attendance is marked only once per day per person
