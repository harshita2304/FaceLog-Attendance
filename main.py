# ==============================
# FaceLog Attendance System (Final Version)
# Features:
# - Company Employees Screen
# - New Employee Form (Name, Role, Code)
# - Face Capture (20 images)
# - Face Recognition
# - One Attendance per Day
# ==============================

# Install:
# pip install opencv-python opencv-contrib-python pillow numpy

import cv2
import os
import csv
import numpy as np
from datetime import datetime
from tkinter import *
from tkinter import messagebox

# ==============================
# CONFIG
# ==============================
DATASET_PATH = "dataset"
ATTENDANCE_FILE = "attendance.csv"
EMPLOYEE_FILE = "employees.csv"
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# ==============================
# INITIAL SETUP
# ==============================
os.makedirs(DATASET_PATH, exist_ok=True)

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, 'w', newline='') as f:
        csv.writer(f).writerow(["Name", "Role", "Timestamp"])

if not os.path.exists(EMPLOYEE_FILE):
    with open(EMPLOYEE_FILE, 'w', newline='') as f:
        csv.writer(f).writerow(["Name", "Role", "Code"])

# ==============================
# LOAD EMPLOYEES
# ==============================
def load_employees():
    employees = {}
    with open(EMPLOYEE_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name, role, code = row
            employees[name] = role
    return employees

# ==============================
# CAPTURE FACES
# ==============================
def capture_faces(name):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(CASCADE_PATH)

    count = 0
    person_path = os.path.join(DATASET_PATH, name)
    os.makedirs(person_path, exist_ok=True)

    messagebox.showinfo("Info", f"Capturing faces for {name}")

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
    messagebox.showinfo("Done", f"Captured {count} images")

# ==============================
# TRAIN MODEL
# ==============================
def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, labels = [], []
    label_map = {}

    current_label = 0

    for person in os.listdir(DATASET_PATH):
        path = os.path.join(DATASET_PATH, person)
        label_map[current_label] = person

        for img_name in os.listdir(path):
            img = cv2.imread(os.path.join(path, img_name), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            labels.append(current_label)

        current_label += 1

    if not faces:
        raise Exception("No training data found")

    recognizer.train(faces, np.array(labels))
    return recognizer, label_map

# ==============================
# CHECK DUPLICATE
# ==============================
def already_marked_today(name):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(ATTENDANCE_FILE, 'r') as f:
        for row in csv.reader(f):
            if row and row[0] == name and row[2].startswith(today):
                return True
    return False

# ==============================
# MARK ATTENDANCE
# ==============================
def mark_attendance(name):
    if already_marked_today(name):
        return

    role = load_employees().get(name, "Unknown")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ATTENDANCE_FILE, 'a', newline='') as f:
        csv.writer(f).writerow([name, role, time_now])

    messagebox.showinfo("Attendance", f"Marked for {name}")

# ==============================
# FACE RECOGNITION
# ==============================
def recognize_face():
    if not os.listdir(DATASET_PATH):
        messagebox.showerror("Error", "No dataset found")
        return

    recognizer, label_map = train_model()
    detector = cv2.CascadeClassifier(CASCADE_PATH)
    cam = cv2.VideoCapture(0)

    session_marked = set()

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            label, conf = recognizer.predict(face)

            if conf < 70:
                name = label_map[label]

                if name not in session_marked and not already_marked_today(name):
                    mark_attendance(name)
                    session_marked.add(name)

                text = f"{name} (Marked)" if already_marked_today(name) else f"{name} (New)"
                cv2.putText(img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            else:
                cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow("Recognition", img)
        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

# ==============================
# NEW EMPLOYEE UI
# ==============================
def new_employee_screen():
    win = Toplevel()
    win.title("New Employee")
    win.geometry("300x300")

    Label(win, text="Name").pack()
    name = Entry(win)
    name.pack()

    Label(win, text="Role").pack()
    role = Entry(win)
    role.pack()

    Label(win, text="Code").pack()
    code = Entry(win)
    code.pack()

    def submit():
        n, r, c = name.get(), role.get(), code.get()

        if not n or not r or not c:
            messagebox.showerror("Error", "All fields required")
            return

        with open(EMPLOYEE_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([n, r, c])

        messagebox.showinfo("Success", f"{n} added")
        win.destroy()
        capture_faces(n)

    Button(win, text="Submit & Capture", command=submit).pack(pady=10)

# ==============================
# COMPANY SCREEN
# ==============================
def company_screen():
    win = Toplevel()
    win.title("Company Employees")
    win.geometry("300x200")

    Button(win, text="Start Face Recognition", bg="green", fg="white",
           command=recognize_face).pack(pady=50)

# ==============================
# MAIN UI
# ==============================
def create_gui():
    root = Tk()
    root.title("FaceLog System")
    root.geometry("300x250")

    Label(root, text="FaceLog System", font=("Arial", 16, "bold")).pack(pady=20)

    Button(root, text="Company Employees", width=25,
           command=company_screen).pack(pady=10)

    Button(root, text="New Employee", width=25,
           command=new_employee_screen).pack(pady=10)

    root.mainloop()

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    create_gui()
