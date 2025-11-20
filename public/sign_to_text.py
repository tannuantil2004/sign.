# ✅ Final Combined ISL Detection (No Voice, Big Text on Webcam)
from ultralytics import YOLO
import cv2

# -----------------------
# Load trained YOLO models
# -----------------------
alphabet_model_path = r"/Users/ritesh/Downloads/isl-project(college)/main/isl_a_to_z_variant/weights/best.pt"
number_model_path   = r"/Users/ritesh/Downloads/isl-project(college)/main/isl_numbers_model/weights/best.pt"

alphabet_model = YOLO(alphabet_model_path)
number_model   = YOLO(number_model_path)

# Define class names
alphabet_classes = [
    "A","B","C","D","E_1","E_2","E_3","F","G","H","I_1","I_2","J_1","J_2","K","L","M","N",
    "O","P","Q","R","S","T","U","V","W","X","Y","Z"
]
number_classes = [str(i) for i in range(10)]

# -----------------------
# Webcam initialization
# -----------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot access webcam.")
    exit()
print("✅ Webcam started. Press 'q' to quit.")

# -----------------------
# Optimization variables
# -----------------------
frame_count = 0
skip_frames = 3          # detect every 3rd frame
last_label = None
stability_counter = 0
STABLE_FRAMES = 10       # keep detection stable for 10 frames

# -----------------------
# Real-time loop
# -----------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    detected_label = None

    # Run detection every few frames
    if frame_count % skip_frames == 0:
        results_alpha = alphabet_model(frame, conf=0.6, verbose=False)
        results_num   = number_model(frame, conf=0.6, verbose=False)

        detections = []
        # Extract alphabet detections
        for r in results_alpha[0].boxes:
            cls = int(r.cls[0])
            detections.append(alphabet_classes[cls])

        # Extract number detections
        for r in results_num[0].boxes:
            cls = int(r.cls[0])
            detections.append(number_classes[cls])

        if detections:
            detected_label = detections[0]
            last_label = detected_label
            stability_counter = STABLE_FRAMES
        elif stability_counter > 0:
            stability_counter -= 1
            detected_label = last_label
    else:
        # Maintain stable label between detections
        if stability_counter > 0:
            stability_counter -= 1
            detected_label = last_label

    # -----------------------
    # Display detection on webcam feed
    # -----------------------
    if detected_label:
        text = f"Detection: {detected_label}"
        font_scale = 2.0   # Large readable text (~30–50px depending on resolution)
        thickness = 5
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        text_x = 30
        text_y = 60

        cv2.putText(
            frame,
            text,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (0, 255, 0),
            thickness,
            cv2.LINE_AA
        )

    # Show the frame
    cv2.imshow("ISL Detection (Smooth & Stable)", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------
# Cleanup
# -----------------------
cap.release()
cv2.destroyAllWindows()
print("🧠 Webcam stopped.")

