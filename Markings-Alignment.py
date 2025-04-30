import cv2
import numpy as np

# expected positions of dots
# TODO update this with actual positions: DONE (see Obtain-Expected-Positions.py)
expected_positions = np.array([
    [980, 871],  # top
    [1266, 565],  # right
    [949, 316],  # bottom
    [661, 595],  # left
])

# tolerance for alignment
position_tolerance = 50

# open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # detect markings: black marks on white background
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # filter markings by size and shape
    centers = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100 or area > 10000:  # TODO adjust for actual marking size: DONE
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    alignment_status = "Not Aligned"  # TODO add alignment suggestion functionality
    if len(centers) == 4:
        # sort centers in expected diamond shape order(top, right, bottom, left)
        centers = sorted(centers, key=lambda c: c[1])  # sort by y
        top, bottom = centers[0], centers[3]
        middle = sorted(centers[1:3], key=lambda c: c[0])  # sort by x
        left, right = middle[0], middle[1]
        detected = np.array([top, right, bottom, left])

        # compare with expected positions
        diffs = np.linalg.norm(detected - expected_positions, axis=1)
        if np.all(diffs < position_tolerance):
            alignment_status = "Aligned"

    # show status
    cv2.putText(frame, alignment_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0) if alignment_status == "Aligned" else (0, 0, 255), 2)
    cv2.imshow("Alignment Check", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
