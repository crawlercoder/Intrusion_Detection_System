import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Open the camera
        self.cap = cv2.VideoCapture(0)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Button to capture a photo
        capture_btn = ttk.Button(window, text="Capture Photo", command=self.capture)
        capture_btn.pack(pady=10)

        # Button to close the app
        close_btn = ttk.Button(window, text="Close", command=self.close_app)
        close_btn.pack(pady=10)

        flip_btn = ttk.Button(window, text="Flip Horizontally", command=self.flip_horizontally)
        flip_btn.pack(pady=10)

        # List to store PhotoImage objects
        self.imgtk_list = []

        self.update()

    def capture(self):
    # Capture frame by frame
        ret, frame = self.cap.read()

        # Generate a unique filename using timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"captured_photo_{timestamp}.jpg"

        # Save the captured frame as an image file in BGR color order
        cv2.imwrite(filename, frame)
        print(f"Photo captured and saved as {filename}!")

        # Create a new PhotoImage object for the canvas using BGR frame
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.imgtk_list.append(imgtk)

    def flip_horizontally(self):
        # Check if there's a captured image to flip
        if self.imgtk_list:
            # Get the last captured image
            last_imgtk = self.imgtk_list[-1]

            # Flip the image horizontally
            flipped_img = Image.fromarray(last_imgtk._PhotoImage__photo.subsample(1, 1).to_image().transpose(Image.FLIP_LEFT_RIGHT))

            # Create a new PhotoImage object for the canvas
            flipped_imgtk = ImageTk.PhotoImage(image=flipped_img)

            # Update the canvas with the flipped image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=flipped_imgtk)

            # Store the flipped PhotoImage object in the list
            self.imgtk_list.append(flipped_imgtk)


    def update(self):
    # Get a frame from the video source
        ret, frame = self.cap.read()

        if ret:
            # Convert the OpenCV image to a PIL image with BGR to RGB conversion
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)

            # Convert to PhotoImage
            imgtk = ImageTk.PhotoImage(image=img)

            # Store the PhotoImage object in the list
            self.imgtk_list.append(imgtk)

            # Update the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

        # Call the update() method after 10 milliseconds
        self.window.after(10, self.update)


    # def capture(self):

    #     # Capture frame by frame
    #     ret, frame = self.cap.read()

    #     # Generate a unique filename using timestamp
    #     timestamp = time.strftime("%Y%m%d_%H%M%S")
    #     filename = f"captured_photo_{timestamp}.jpg"

    #     # Convert from BGR to RGB
    #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #     # Save the captured frame as an image file in RGB color order
    #     cv2.imwrite(filename, rgb_frame)
    #     print(f"Photo captured and saved as {filename}!")

    #     # Create a new PhotoImage object for the canvas
    #     img = Image.fromarray(rgb_frame)
    #     imgtk = ImageTk.PhotoImage(image=img)
    #     self.imgtk_list.append(imgtk)

        


    # def update(self):
    # # Get a frame from the video source
    #     ret, frame = self.cap.read()

    #     if ret:
    #         # Convert the OpenCV image to a PIL image with BGR to RGB conversion
    #         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         img = Image.fromarray(rgb_frame)

    #         # Convert to PhotoImage
    #         imgtk = ImageTk.PhotoImage(image=img)

    #         # Store the PhotoImage object in the list
    #         self.imgtk_list.append(imgtk)

    #         # Update the canvas
    #         self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

    #     # Call the update() method after 10 milliseconds
    #     self.window.after(10, self.update)


    def close_app(self):
        # Release the camera and close the app
        self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "Camera App")
    root.mainloop()
