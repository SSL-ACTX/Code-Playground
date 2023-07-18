import cv2
import numpy as np

# Load the input video
cap = cv2.VideoCapture('vid.mp4')

# Get the input video dimensions
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the available interpolation methods
interpolation_methods = {
    'Nearest Neighbor': cv2.INTER_NEAREST,
    'Bilinear': cv2.INTER_LINEAR,
    'Bicubic': cv2.INTER_CUBIC,
    'Lanczos': cv2.INTER_LANCZOS4
}

# Print the available interpolation methods
print('Available upscaling methods:')
for i, method_name in enumerate(interpolation_methods.keys()):
    print(f'{i + 1}. {method_name}')

# Get the user's choice of upscaling method
method_idx = int(input('Choose the upscaling method (enter the corresponding number): '))
method_name = list(interpolation_methods.keys())[method_idx - 1]
interpolation = interpolation_methods[method_name]

# Get the upscale factor from the user
upscale_factor = int(input('Enter the upscale factor (e.g. 2 for 2x): '))
new_width = width * upscale_factor
new_height = height * upscale_factor

# Get the user's choice of sharpening amount
sharpen_amount = float(input('Enter the sharpening amount (e.g. 0.5 for half): '))

# Create an output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, 30.0, (new_width, new_height))

# Define the sharpening kernel
sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) * sharpen_amount

# Loop through the input video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Upscale the frame by the specified factor using the chosen interpolation method
    upscaled_frame = cv2.resize(frame, (new_width, new_height), interpolation=interpolation)

    # Apply the sharpening filter to the upscaled frame
    sharpened_frame = cv2.filter2D(upscaled_frame, -1, sharpen_kernel)

    # Write the upscaled and sharpened frame to the output video
    out.write(sharpened_frame)

    # Display the upscaled and sharpened frame
    # cv2.imshow('Upscaled and Sharpened Video', sharpened_frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release the resources
cap.release()
out.release()
cv2.destroyAllWindows()
