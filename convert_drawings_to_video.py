import cv2
import os

def images_to_video(image_folder, output_video, fps=30):
    images = sorted([img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))])
    if not images:
        raise ValueError("No images found in the folder.")

    # Read the first image to get the size
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' for AVI
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        if frame is None:
            break
        if frame.shape[:2] != (height, width):
            frame = cv2.resize(frame, (width, height))  # Ensure same size
        video.write(frame)

    video.release()
    print(f"Video saved as: {output_video}")
    print("Done")