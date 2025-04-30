import cv2
import numpy as np

# expected positions of dots
expected_positions = np.array([
    [320, 90],  # top
    [470, 240],  # right
    [320, 390],  # bottom
    [170, 240],  # left
])

# tolerance for alignment
position_tolerance = 50

# start camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

alignment_status = "Searching"
move_suggestion = "Searching for dots"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 100 < area < 10000:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    if len(centers) == 4:
        # sort the centers to match the expect [top, right, bottom, left]
        centers = sorted(centers, key=lambda c: c[1])  # sorted by y
        top, bottom = centers[0], centers[3]
        middle = sorted(centers[1:3], key=lambda c: c[0])  # sorted by x
        left, right = middle[0], middle[1]
        detected = np.array([top, right, bottom, left])

        #compute difference between expected and actual
        diffs = np.linalg.norm(detected - expected_positions, axis=1)
        mean_shift = np.mean(detected - expected_positions, axis=0)
        dx, dy = mean_shift

        if np.all(diffs < position_tolerance):
            alignment_status = "Aligned"
            move_suggestion = "Perfectly Aligned"
        else:
            alignment_status = "Not Aligned"
            move_suggestion = ""
            if abs(dx) > position_tolerance:
                move_suggestion += "Move Left" if dx > 0 else "Move Right"
            if abs(dy) > position_tolerance:
                if move_suggestion:
                    move_suggestion += " and "
                move_suggestion += "Move Up" if dy > 0 else "Move Down"
    # else:
        # alignment_status = "Searching"
        # move_suggestion = "Searching for dots"

    #draw expected positions
    for pt in expected_positions:
        cv2.circle(frame, tuple(pt.astype(int)), 5, (255, 0, 0), 2)


    #display text
    cv2.putText(frame, alignment_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0) if alignment_status == "Aligned" else (0, 0, 255), 2)
    cv2.putText(frame, move_suggestion, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 255, 0), 2)

    # show video
    cv2.imshow("Alignment Checker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()