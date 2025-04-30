import cv2
import numpy as np

# load image
image = cv2.imread('expected_markings1.jpeg')
resized = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
# cv2.imshow("Resized", resized)
# print("Image shape:", image.shape)
image = resized

# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# apply gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# apply threshold to isolate markings
# TODO might need to adjust threshold
# _, thresh = cv2.threshold(blurred, 80, 120, cv2.THRESH_BINARY_INV)
thresh = cv2.adaptiveThreshold(blurred, 250, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)

# find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
# '''''
print(f"Found {len(contours)} contours")
cv2.imshow("Threshold", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
# '''''

# loop through contours to find square markings
actual_positions = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 100 or area > 10000:
        continue  # filter out noise or very large shapes

    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = float(w) / h

    if 0.85 < aspect_ratio < 1.15:  # roughly square
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            actual_positions.append([cx, cy])

actual_positions = np.array(actual_positions)

# output detected positions
print("Detected marking positions:")
for pos in actual_positions:
    print(pos)
'''''
#calculate and print centroid positions of each detected contour
actual_positions = []
for cnt in contours:
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        actual_positions.append([cx, cy])

actual_positions = np.array(actual_positions)

#output detected positions
print("Detected marking positions:")
for pos in actual_positions:
    print(pos)
'''