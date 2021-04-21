import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import cv2
import random
from tkinter import *
from PIL import ImageGrab
from tensorflow import keras


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
DRAWING_THICKNESS = 10
SHADING_INTENSITY_LOWER = 0.2
SHADING_INTENSITY_UPPER = 0.7

# loading in trained model
model = keras.models.load_model("images/two_hidden_layers/model7.h5")

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
        self.capture_image()
        img = self.convert_image()
        self.make_prediction(img)

    def activate_draw(self, event):
        self.drawing_activated = True

    def deactivate_draw(self, event):
        self.drawing_activated = False

    def make_prediction(self, input_array):
        prediction = model.predict(input_array)

        predictions = {
            "0": prediction[0][0],
            "1": prediction[0][1],
            "2": prediction[0][2],
            "3": prediction[0][3],
            "4": prediction[0][4],
            "5": prediction[0][5],
            "6": prediction[0][6],
            "7": prediction[0][7],
            "8": prediction[0][8],
            "9": prediction[0][9],
        }

        sorted_keys = sorted(predictions.keys(), reverse=True, key=lambda k : predictions[k])
        print(sorted_keys)

        print("That is the number ", np.argmax(prediction))

    def convert_image(self):
        img = cv2.imread("images/digit.jpg", 0)
        img = cv2.resize(img, (28, 28))
        img = img / 255.0
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img[i][j] == 1.0:
                    img[i][j] = 0
                else:
                    img[i][j] = 1

        img = self.blur_image(img)

        plt.imshow(img, cmap="gray")
        plt.show()

        img = img.reshape(1, 28, 28)
        return img

    def blur_image(self, img):
        for i in range(len(img)):
            for j in range(len(img[i])):
                if 0 < i < 26 and 0 < j < 26:
                    if img[i][j] == 1:
                        img[i-1][j] = random.uniform(SHADING_INTENSITY_LOWER, SHADING_INTENSITY_UPPER) if img[i-1][j] == 0 else img[i-1][j]
                        img[i+1][j] = random.uniform(SHADING_INTENSITY_LOWER, SHADING_INTENSITY_UPPER) if img[i+1][j] == 0 else img[i+1][j]
                        img[i][j-1] = random.uniform(SHADING_INTENSITY_LOWER, SHADING_INTENSITY_UPPER) if img[i][j-1] == 0 else img[i][j-1]
                        img[i][j+1] = random.uniform(SHADING_INTENSITY_LOWER, SHADING_INTENSITY_UPPER) if img[i][j+1] == 0 else img[i][j+1]
        return img

    def draw(self, event):
        x1, y1, x2, y2 = event.x-DRAWING_THICKNESS, event.y-DRAWING_THICKNESS, event.x+DRAWING_THICKNESS, event.y+DRAWING_THICKNESS
        if self.drawing_activated:
                #self.canvas.create_oval(x1, y1, x2, y2, fill="black")
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black")

    def capture_image(self):
        widget = self.canvas
        x = self.master.winfo_rootx() + widget.winfo_x()
        y = self.master.winfo_rooty() + widget.winfo_y()
        x1 = x + widget.winfo_width()
        y1 = y + widget.winfo_height()

        ImageGrab.grab().crop((x+10, y+10, x1-10, y1-10)).save("images/digit.jpg")


def main():
    root = Tk()
    window = DrawingBoard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
