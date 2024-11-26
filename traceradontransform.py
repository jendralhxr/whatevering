import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt

def rotate_image(image, angle):
    """Rotates the image by the given angle."""
    return scipy.ndimage.rotate(image, angle, reshape=False, mode='constant', cval=0)

def trace_transform(image, angles, func=np.sum):
    """
    Applies the Trace Transform on an image by rotating it at specified angles and applying the functional transform.
    
    Args:
        image: 2D array representing the image.
        angles: List of angles (in degrees) to rotate the image.
        func: Function to apply along the pixel values on each trace line (default is sum).
    
    Returns:
        Transformed image for each angle.
    """
    transformed_images = []
    
    for angle in angles:
        rotated_image = rotate_image(image, angle)
        # Apply the chosen functional transform (e.g., sum) along rows (axis=1)
        trace_values = func(rotated_image, axis=1)
        transformed_images.append(trace_values)
    
    return np.array(transformed_images)

# Example usage
if __name__ == "__main__":
    # Create a simple test image (e.g., a 2D Gaussian or any pattern)
    image = np.zeros((100, 100))
    image[30:70, 30:70] = 255  # Square pattern in the center
    
    # Define a range of angles
    angles = np.linspace(0, 180, 10)  # 10 angles between 0 and 180 degrees
    
    # Apply Trace Transform
    transformed = trace_transform(image, angles)
    
    # Plot original and transformed images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    
    plt.subplot(1, 2, 2)
    plt.imshow(transformed, aspect='auto', cmap='gray')
    plt.title('Trace Transformed Image')
    plt.show()
