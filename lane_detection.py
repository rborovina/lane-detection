import numpy as np
import cv2
from tkinter import *
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Lane detection")
window.state('zoomed')

window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=300, height=300)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

stop = True

def make_points(image, line):
    if np.isnan(line.min()):
        return [[0, 0, 0, 0]]

    slope, intercept = line
    y1 = int(image.shape[0])
    y2 = int(y1 * 2.2 / 3)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return [[x1, y1, x2, y2]]

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_points(image, left_fit_average)
    right_line = make_points(image, right_fit_average)

    averaged_lines = [left_line, right_line]
    return averaged_lines

def canny_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
    canny = cv2.Canny(gray, 50, 150)
    return canny

def display_lines(img, lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                try:
                    cv2.line(line_image, (x1, y1), (x2, y2), (153, 0, 0), 6)
                except:
                    print(line)

    return line_image

def region_of_interest(canny):
    height = canny.shape[0]
    width = canny.shape[1]
    mask = np.zeros_like(canny)

    trapezoid = np.array([[
        (width * 0.8 / 5, height),
        (width * 0.9 / 2, height * 2.1 / 3),
        (width * 1.1 / 2, height * 2.1 / 3),
        (width * 4.2 / 5, height)]], np.int32)

    cv2.fillPoly(mask, trapezoid, 255)
    masked_image = cv2.bitwise_and(canny, mask)
    return masked_image
def show_frame():
    if not stop:
        _, frame = cap.read()
        original = frame
        original_image = Image.fromarray(original)

        canny_image = canny_edge(frame)
        # cv2.imshow("cropped", canny_image)
        cropped = Image.fromarray(canny_image)

        cropped_canny = region_of_interest(canny_image)
        # cv2.imshow("canny", cropped_canny)
        canny = Image.fromarray(cropped_canny)

        lines = cv2.HoughLinesP(cropped_canny, 2, np.pi / 180, 50, np.array([]), minLineLength=40, maxLineGap=5)
        '''
        h, w = frame.shape[:2]

        x = np.arange(w)
        polynomial1 = lambda x: x ** 2 / 800
        polynomial2 = lambda x: x + 200
        y1 = polynomial1(x)
        y2 = polynomial2(x)

        points1 = np.array([[[xi, yi]] for xi, yi in zip(x, y1) if (0 <= xi < w and 0 <= yi < h)]).astype(np.int32)
        points2 = np.array([[[xi, yi]] for xi, yi in zip(x, y2) if (0 <= xi < w and 0 <= yi < h)]).astype(np.int32)
        points = np.concatenate((points1, np.flip(points2, 0)))

        cv2.fillPoly(frame, [points], color=[233, 233, 233, 0.4])
        '''

        averaged_lines = average_slope_intercept(frame, lines)
        line_image = display_lines(frame, averaged_lines)
        # cv2.imshow("lines", line_image)

        combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        # cv2.imshow("result", combo_image)
        result = Image.fromarray(combo_image)

        original = ImageTk.PhotoImage(image=original_image)
        cropped = ImageTk.PhotoImage(image=cropped)
        canny = ImageTk.PhotoImage(image=canny)
        #lines = ImageTk.PhotoImage(image=lines)
        result = ImageTk.PhotoImage(image=result)

        display1.imgtk = original  # Shows frame for display 1
        display1.configure(image=original)
        display2.imgtk = cropped  # Shows frame for display 2
        display2.configure(image=cropped)
        display3.imgtk = canny  # Shows frame for display 3
        display3.configure(image=canny)
        display4.imgtk = result  # Shows frame for display 4
        display4.configure(image=result)
        window.after(10, show_frame)

def select_video():
    global stop
    stop = True
    path = filedialog.askopenfilename()
    if len(path) > 0:
        global cap
        cap = cv2.VideoCapture(path)
        stop = False
        show_frame()


display1 = tk.Label(imageFrame)
display1.grid(row=0, column=0, padx=10, pady=2)  #Display 1
display2 = tk.Label(imageFrame)
display2.grid(row=1, column=0, padx=10, pady=2) #Display 2
display3 = tk.Label(imageFrame)
display3.grid(row=0, column=1, padx=10, pady=2) #Display 3
display4 = tk.Label(imageFrame)
display4.grid(row=1, column=1, padx=10, pady=2) #Display 4
display5 = tk.Button(window, text="Select a Video :)", command=select_video)
display5.grid(row=2, column=0)

#Slider window (slider controls stage position)
sliderFrame = tk.Frame(window, width=600, height=100)
sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

#Capture video frames
#cap = cv2.VideoCapture("test.mp4")

#show_frame() #Display
window.mainloop()  #Starts GUI