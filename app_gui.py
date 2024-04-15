import tkinter as tk
from tkinter import simpledialog, messagebox
from camera_capture import capture_image
from security_manager import save_user, check_user, get_image_path, get_all_users
import face_recognition
import os

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple 2FA System")
        self.geometry("300x200")
        self.main_menu()

    def main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        users = get_all_users()
        user_list = ', '.join(users)
        tk.Label(self, text=f"Users: {user_list}").pack(pady=10)
        tk.Button(self, text="Add New User", command=self.add_user).pack(pady=10)
        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def add_user(self):
        self.username = simpledialog.askstring("Username", "Enter a unique username:")
        if self.username:
            self.save_path = f'C:\\Users\\Chris\\Desktop\\FacialRecognition\\pythonProject\\saved_images\\{self.username}.jpg'
            capture_image(self.save_path)
            password = simpledialog.askstring("Password", "Enter your password:", show="*")
            if password:
                save_user(self.username, self.save_path, password)
                messagebox.showinfo("Success", "New user added successfully!")
            self.main_menu()

    def login(self):
        self.username = simpledialog.askstring("Login", "Enter your username:")
        if self.username:
            password = simpledialog.askstring("Password", "Enter your password:", show="*")
            if password:
                if check_user(self.username, password):
                    login_image_path = f'C:\\Users\\Chris\\Desktop\\FacialRecognition\\pythonProject\\saved_images\\{self.username}_login.jpg'
                    capture_image(login_image_path)  # Capture a new image for login
                    image_path = get_image_path(self.username)
                    if image_path and self.verify_face(image_path, login_image_path):
                        messagebox.showinfo("Login Success", "Account Verified")
                    else:
                        messagebox.showerror("Login Failed", "Facial recognition failed")
                else:
                    messagebox.showerror("Login Failed", "Password is incorrect")
            self.main_menu()

    def verify_face(self, saved_image_path, login_image_path):
        try:
            base_image = face_recognition.load_image_file(saved_image_path)
            login_image = face_recognition.load_image_file(login_image_path)
            base_encodings = face_recognition.face_encodings(base_image)
            login_encodings = face_recognition.face_encodings(login_image)
            if base_encodings and login_encodings:
                results = face_recognition.compare_faces([base_encodings[0]], login_encodings[0])
                return results[0]
            return False
        except Exception as e:
            print(f"Failed to verify face: {e}")
            return False

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()
