import cv2
import numpy as np


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


cap = cv2.VideoCapture("test.mp4")

while (cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny_edge(frame)
    cv2.imshow("cropped", canny_image)
    cropped_canny = region_of_interest(canny_image)
    cv2.imshow("canny", cropped_canny)
    lines = cv2.HoughLinesP(cropped_canny, 2, np.pi / 180, 50, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    cv2.imshow("lines", line_image)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("result", combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
