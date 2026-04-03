# # ==============================
# # FaceLog Attendance System
# # ==============================
# # Requirements:
# # pip install opencv-python pillow

# import cv2
# import os
# import csv
# from datetime import datetime
# from tkinter import *
# from tkinter import messagebox

# # ==============================
# # CONFIGURATION
# # ==============================
# DATASET_PATH = "dataset"
# ATTENDANCE_FILE = "attendance.csv"
# CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# members = {
#     "Harshita": "Python Developer",
#     "Rajesh": "Senior Product Manager",
#     "Ananya": "Sales Intern",
#     "Vikram": "Sales Head",
#     "Priya": "Technical Lead",
#     "Sameer": "HR"
# }

# # Ensure dataset directory exists
# if not os.path.exists(DATASET_PATH):
#     os.makedirs(DATASET_PATH)

# # Ensure attendance file exists
# if not os.path.exists(ATTENDANCE_FILE):
#     with open(ATTENDANCE_FILE, mode='w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(["Name", "Role", "Timestamp"])

# # ==============================
# # FACE DATA CAPTURE
# # ==============================
# def capture_faces(name):
#     cam = cv2.VideoCapture(0)
#     detector = cv2.CascadeClassifier(CASCADE_PATH)

#     count = 0
#     person_path = os.path.join(DATASET_PATH, name)

#     if not os.path.exists(person_path):
#         os.makedirs(person_path)

#     messagebox.showinfo("Info", f"Capturing images for {name}. Look at camera.")

#     while True:
#         ret, img = cam.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = detector.detectMultiScale(gray, 1.3, 5)

#         for (x, y, w, h) in faces:
#             count += 1
#             face_img = gray[y:y+h, x:x+w]
#             file_path = os.path.join(person_path, f"{count}.jpg")
#             cv2.imwrite(file_path, face_img)

#             cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

#         cv2.imshow("Capturing Faces", img)

#         if cv2.waitKey(1) == 27 or count >= 20:
#             break

#     cam.release()
#     cv2.destroyAllWindows()
#     messagebox.showinfo("Done", f"Captured {count} images for {name}")

# # ==============================
# # FACE RECOGNITION + ATTENDANCE
# # ==============================
# import numpy as np

# def train_model():
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     faces = []
#     labels = []
#     label_map = {}

#     current_label = 0

#     for person in os.listdir(DATASET_PATH):
#         person_path = os.path.join(DATASET_PATH, person)
#         label_map[current_label] = person

#         for image_name in os.listdir(person_path):
#             img_path = os.path.join(person_path, image_name)
#             img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

#             if img is None:
#                 continue

#             faces.append(img)
#             labels.append(current_label)

#         current_label += 1

#     if len(faces) == 0:
#         raise Exception("No training data found. Capture faces first.")

#     recognizer.train(faces, np.array(labels))

#     return recognizer, label_map


# def mark_attendance(name):
#     role = members[name]
#     time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     with open(ATTENDANCE_FILE, mode='a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([name, role, time_now])

#     messagebox.showinfo("Attendance", f"Attendance marked for {name}")


# def recognize_face():
#     if not os.listdir(DATASET_PATH):
#         messagebox.showerror("Error", "No dataset found. Capture faces first.")
#         return

#     recognizer, label_map = train_model()
#     detector = cv2.CascadeClassifier(CASCADE_PATH)
#     cam = cv2.VideoCapture(0)

#     messagebox.showinfo("Info", "Press ESC to stop recognition")

#     while True:
#         ret, img = cam.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = detector.detectMultiScale(gray, 1.3, 5)

#         for (x, y, w, h) in faces:
#             face_img = gray[y:y+h, x:x+w]
#             label, confidence = recognizer.predict(face_img)

#             if confidence < 70:
#                 name = label_map[label]
#                 mark_attendance(name)
#                 cv2.putText(img, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#             else:
#                 cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

#             cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

#         cv2.imshow("Face Recognition", img)

#         if cv2.waitKey(1) == 27:
#             break

#     cam.release()
#     cv2.destroyAllWindows()

# # ==============================
# # GUI (TKINTER)
# # ==============================
# def create_gui():
#     root = Tk()
#     root.title("FaceLog Attendance System")
#     root.geometry("600x500")

#     Label(root, text="FaceLog Attendance System", font=("Arial", 16, "bold")).pack(pady=10)

#     # Capture Buttons
#     Label(root, text="Capture Dataset", font=("Arial", 12)).pack(pady=5)

#     for name in members:
#         Button(root, text=f"Capture {name}", width=25,
#                command=lambda n=name: capture_faces(n)).pack(pady=3)

#     # Attendance Section
#     Label(root, text="\nAttendance", font=("Arial", 12)).pack()

#     Button(root, text="Start Face Recognition", width=30, bg="green", fg="white",
#            command=recognize_face).pack(pady=10)

#     root.mainloop()

# # ==============================
# # MAIN
# # ==============================
# if __name__ == "__main__":
#     create_gui()

# ==============================
# FaceLog Attendance System (Updated - One Entry Per Day)
# ==============================

# Requirements:
# pip install opencv-python opencv-contrib-python pillow numpy

import cv2
import os
import csv
import numpy as np
from datetime import datetime
from tkinter import *
from tkinter import messagebox

# ==============================
# CONFIGURATION
# ==============================
DATASET_PATH = "dataset"
ATTENDANCE_FILE = "attendance.csv"
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

members = {
    "Harshita": "Python Developer",
    "Rajesh": "Senior Product Manager",
    "Ananya": "Sales Intern",
    "Vikram": "Sales Head",
    "Priya": "Technical Lead",
    "Sameer": "HR"
}

# ==============================
# INITIAL SETUP
# ==============================
if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Role", "Timestamp"])

# ==============================
# CAPTURE FACES
# ==============================
def capture_faces(name):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(CASCADE_PATH)

    count = 0
    person_path = os.path.join(DATASET_PATH, name)

    if not os.path.exists(person_path):
        os.makedirs(person_path)

    messagebox.showinfo("Info", f"Capturing images for {name}")

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(person_path, f"{count}.jpg"), face_img)

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow("Capturing Faces", img)

        if cv2.waitKey(1) == 27 or count >= 20:
            break

    cam.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Done", f"Captured {count} images for {name}")

# ==============================
# TRAIN MODEL
# ==============================
def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_map = {}

    current_label = 0

    for person in os.listdir(DATASET_PATH):
        person_path = os.path.join(DATASET_PATH, person)
        label_map[current_label] = person

        for image_name in os.listdir(person_path):
            img_path = os.path.join(person_path, image_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            faces.append(img)
            labels.append(current_label)

        current_label += 1

    if len(faces) == 0:
        raise Exception("No training data found. Capture faces first.")

    recognizer.train(faces, np.array(labels))
    return recognizer, label_map

# ==============================
# CHECK IF ALREADY MARKED TODAY
# ==============================
def already_marked_today(name):
    today = datetime.now().strftime("%Y-%m-%d")

    with open(ATTENDANCE_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == name and row[2].startswith(today):
                return True
    return False

# ==============================
# MARK ATTENDANCE
# ==============================
def mark_attendance(name):
    if already_marked_today(name):
        return

    role = members[name]
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ATTENDANCE_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, role, time_now])

    messagebox.showinfo("Attendance", f"Attendance marked for {name}")

# ==============================
# FACE RECOGNITION
# ==============================
def recognize_face():
    if not os.listdir(DATASET_PATH):
        messagebox.showerror("Error", "Capture faces first.")
        return

    recognizer, label_map = train_model()
    detector = cv2.CascadeClassifier(CASCADE_PATH)
    cam = cv2.VideoCapture(0)

    session_marked = set()

    messagebox.showinfo("Info", "Press ESC to stop")

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face_img)

            if confidence < 70:
                name = label_map[label]

                if name not in session_marked and not already_marked_today(name):
                    mark_attendance(name)
                    session_marked.add(name)

                if already_marked_today(name):
                    display_text = f"{name} (Marked)"
                else:
                    display_text = f"{name} (New)"

                cv2.putText(img, display_text, (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            else:
                cv2.putText(img, "Unknown", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow("Face Recognition", img)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

# ==============================
# GUI
# ==============================
def create_gui():
    root = Tk()
    root.title("FaceLog Attendance System")
    root.geometry("600x500")

    Label(root, text="FaceLog Attendance System", font=("Arial", 16, "bold")).pack(pady=10)

    Label(root, text="Capture Dataset", font=("Arial", 12)).pack(pady=5)

    for name in members:
        Button(root, text=f"Capture {name}", width=25,
               command=lambda n=name: capture_faces(n)).pack(pady=3)

    Label(root, text="\nAttendance", font=("Arial", 12)).pack()

    Button(root, text="Start Face Recognition", width=30,
           bg="green", fg="white", command=recognize_face).pack(pady=10)

    root.mainloop()

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    create_gui()
