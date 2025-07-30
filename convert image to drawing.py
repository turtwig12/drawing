import cv2
import numpy as np
from PIL import Image, ImageEnhance

# Load image and enhance contrast moderately
input_path = 'output_frames/frame_00130.jpg'
image = Image.open(input_path)
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(1.3)  # Moderate contrast enhancement

# Convert to grayscale for edge detection
gray = np.array(image.convert('L'))

# Optional: smooth image to reduce noise before edge detection
gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect edges using Canny (tweak thresholds as needed)
edges = cv2.Canny(gray_blurred, threshold1=40, threshold2=80) #senstivity

# Create an output image: white background, black edges
lines_image = np.full_like(edges, 255)  #makes the background white
lines_image[edges > 0] = 0  #Draws black edges


# Convert to RGB for saving/viewing
lines_image_rgb = cv2.cvtColor(lines_image, cv2.COLOR_GRAY2RGB)

# Save the final edge image
output_path = 'edges_output.png'
cv2.imwrite(output_path, lines_image_rgb)

print(f"Processed image saved as {output_path}")

# Display the image
cv2.imshow("Clean Edges", lines_image_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()


