import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from PIL import ImageGrab, ImageOps
from tensorflow import keras
import cv2

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
NUM_PTS = CANVAS_HEIGHT // 10
DRAWING_THICKNESS = 10


model = keras.models.load_model("model.h5")

class DrawingBoard:
    def __init__(self, master):
        self.master = master
        self.grid = Grid()
        self.drawing_activated = False

        self.top_frame = Frame(self.master)
        self.top_frame.pack()
        self.predict_button = Button(self.top_frame, text="Predict", command=self.guess_number)
        self.predict_button.grid(row=0, column=0)
        self.clear_button = Button(self.top_frame, text="Clear", command=self.clear)
        self.clear_button.grid(row=0, column=1)
        self.canvas = Canvas(self.master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.activate_draw)
        self.canvas.bind("<ButtonRelease-1>", self.deactivate_draw)
        self.canvas.bind("<Motion>", self.draw)

    def clear(self):
        self.canvas.delete("all")

    def guess_number(self):
        self.capture_image(self.canvas)

        img = cv2.imread("images/digit.jpg", 0)
        img = cv2.resize(img, (28, 28))
        img = img / 255.0
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img[i][j] == 1.0:
                    img[i][j] = 0
                else:
                    img[i][j] = 1 - img[i][j]

        plt.imshow(img, cmap="gray")
        plt.show()

        img = img.reshape(1, 28, 28)

        self.make_prediction(img)


    def activate_draw(self, event):
        self.drawing_activated = True

    def deactivate_draw(self, event):
        self.drawing_activated = False


    def make_prediction(self, input_array):
        prediction = model.predict(input_array)

        print("That is the number ", np.argmax(prediction))


    def convert_image(self, image):
        image = image.resize((28, 28))
        image = image.convert("L")
        image_array = np.array(image)
        image_array = image_array / 255.0
        for i in range(len(image_array)):
            for j in range(len(image_array[i])):
                if image_array[i][j] == 1.0:
                    image_array[i][j] = 0


        image_array = image_array.reshape(1, 28, 28)
        print(len(image_array))
        print(len(image_array[0]))
        print(len(image_array[0][0]))
        print(image_array.shape)
        plt.imshow(image_array, cmap="gray")
        plt.show()
        print(image_array)
        return image_array


    def draw(self, event):
        x1, y1, x2, y2 = event.x-DRAWING_THICKNESS, event.y-DRAWING_THICKNESS, event.x+DRAWING_THICKNESS, event.y+DRAWING_THICKNESS
        if self.drawing_activated:
                #self.canvas.create_oval(x1, y1, x2, y2, fill="black")
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black")


    def capture_image(self, widget):
        x = self.master.winfo_rootx() + widget.winfo_x()
        y = self.master.winfo_rooty() + widget.winfo_y()
        x1 = x + widget.winfo_width()
        y1 = y + widget.winfo_height()
        return ImageGrab.grab().crop((x+10, y+10, x1-10, y1-10)).save("images/digit.jpg")


def main():
    root = Tk()
    window = DrawingBoard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
