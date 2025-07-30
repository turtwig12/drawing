import cv2
import os
import time
import sys
import numpy as np
from PIL import Image, ImageEnhance

def extract_frames(video_path, output_dir, output_line_dir, sample_rate=1):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_line_dir, exist_ok=True)

    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        print("Error: Cannot open video.")
        return

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    frame_interval = int(fps * sample_rate)
    total_frames_to_save = frame_count // frame_interval

    def format_duration(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{secs:02}"

    print(f"Video duration: {format_duration(duration)}")
    print(f"Saving approx. {total_frames_to_save} frames...\n")

    start_time = time.time()







    def print_progress_bar(iteration, total, length=50):
        elapsed = time.time() - start_time
        avg_time = elapsed / max(1, iteration)
        eta = avg_time * (total - iteration)
        if eta <0:
            eta = 0
        percent = int(100 * (iteration / float(total)))
        bar = '█' * int(length * iteration // total) + '-' * (length - int(length * iteration // total))
        sys.stdout.write(f"\r|{bar}| {percent}%  ETA: {format_duration(eta)}")
        sys.stdout.flush()

    count = 0
    saved_count = 0
    while True:
        success, frame = vidcap.read()
        def make_line_image(frame):
            # Convert BGR (OpenCV) to RGB (PIL)
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Enhance contrast moderately
            enhancer = ImageEnhance.Contrast(pil_image)
            enhanced_image = enhancer.enhance(1.3)#1.3 gives best results

            # Convert to grayscale for edge detection
            gray = np.array(enhanced_image.convert('L'))

            # Apply Gaussian blur to reduce noise
            gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Detect edges with Canny (more sensitive thresholds)
            edges = cv2.Canny(gray_blurred, threshold1=40, threshold2=80)

            # Create white background image and draw black edges
            lines_image = np.full_like(edges, 255)
            lines_image[edges > 0] = 0

            # Convert grayscale to RGB for saving/viewing
            lines_image_rgb = cv2.cvtColor(lines_image, cv2.COLOR_GRAY2RGB)

            return lines_image_rgb
        frame_line=make_line_image(frame)

        if not success:
            break

        if count % frame_interval == 0:
            img_name = os.path.join(output_dir, f"frame_{saved_count:05}.jpg")
            img_name_line = os.path.join(output_line_dir, f"frame_{saved_count:05}_line.jpg")
            cv2.imwrite(img_name, frame)
            cv2.imwrite(img_name_line, frame_line)
            saved_count += 1
            print_progress_bar(saved_count, total_frames_to_save)

        count += 1

    vidcap.release()
    print("\nDone.")

# Example usage
extract_frames("IMG_6420.mov", "output_frames", "output_frames_lines", sample_rate=0.1)
