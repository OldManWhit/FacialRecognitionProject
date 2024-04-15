import os
import cv2


def setup_directory(path):
    """Ensure the directory exists; if not, create it.

    Args:
        path (str): The path of the directory to check and create if it doesn't exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def capture_image(save_path):
    """Capture an image using the webcam and save it to the specified path.

    Args:
        save_path (str): The complete path where the image will be saved.
    """
    setup_directory(os.path.dirname(save_path))  # Ensure directory exists
    cap = cv2.VideoCapture(0)  # Initialize the camera

    if not cap.isOpened():
        print("Error: Cannot open webcam.")
        return

    print("Press 's' to save and exit, 'q' to quit.")
    while True:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:
            print("Error: Cannot capture frame.")
            break

        cv2.imshow("Capture", frame)  # Display the capturing frame

        key = cv2.waitKey(1)
        if key == ord('s'):  # Save on pressing 's'
            cv2.imwrite(save_path, frame)
            print(f"Image saved to {save_path}")
            break
        elif key == ord('q'):  # Exit on pressing 'q'
            break

    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Destroy all OpenCV windows


if __name__ == "__main__":
    save_path = 'C:\\Users\\Chris\\Desktop\\FacialRecognition\\pythonProject\\saved_images\\user_image.jpg'
    capture_image(save_path)
