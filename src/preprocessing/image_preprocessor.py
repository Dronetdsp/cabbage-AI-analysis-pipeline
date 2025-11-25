"""
Image Preprocessing Module for Cabbage AI Analysis Pipeline
Handles image loading, normalization, augmentation, and preparation
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional, Union
import os


class ImagePreprocessor:
    """Preprocess images for AI model input"""

    def __init__(
        self,
        target_size: Tuple[int, int] = (512, 512),
        normalize: bool = True,
        color_mode: str = 'RGB'
    ):
        """
        Initialize image preprocessor

        Args:
            target_size: Target image dimensions (height, width)
            normalize: Whether to normalize pixel values to [0, 1]
            color_mode: Color mode ('RGB' or 'BGR')
        """
        self.target_size = target_size
        self.normalize = normalize
        self.color_mode = color_mode

    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load image from file

        Args:
            image_path: Path to image file

        Returns:
            Image as numpy array

        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image cannot be loaded
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Load with OpenCV
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # Convert color space if needed
        if self.color_mode == 'RGB':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image

    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Resize image to target size

        Args:
            image: Input image array

        Returns:
            Resized image
        """
        return cv2.resize(image, self.target_size, interpolation=cv2.INTER_LINEAR)

    def normalize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Normalize image pixel values to [0, 1]

        Args:
            image: Input image array

        Returns:
            Normalized image
        """
        return image.astype(np.float32) / 255.0

    def preprocess(self, image_path: str) -> np.ndarray:
        """
        Complete preprocessing pipeline

        Args:
            image_path: Path to image file

        Returns:
            Preprocessed image array
        """
        # Load image
        image = self.load_image(image_path)

        # Resize
        image = self.resize_image(image)

        # Normalize
        if self.normalize:
            image = self.normalize_image(image)

        return image

    def preprocess_batch(self, image_paths: list) -> np.ndarray:
        """
        Preprocess multiple images

        Args:
            image_paths: List of image file paths

        Returns:
            Batch of preprocessed images as array [N, H, W, C]
        """
        processed_images = []

        for path in image_paths:
            try:
                image = self.preprocess(path)
                processed_images.append(image)
            except Exception as e:
                print(f"Error processing {path}: {e}")
                continue

        if not processed_images:
            raise ValueError("No images were successfully processed")

        return np.array(processed_images)

    def apply_color_correction(self, image: np.ndarray) -> np.ndarray:
        """
        Apply automatic color correction

        Args:
            image: Input image array

        Returns:
            Color corrected image
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

        # Split channels
        l, a, b = cv2.split(lab)

        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)

        # Merge channels
        lab = cv2.merge([l, a, b])

        # Convert back to RGB
        corrected = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

        return corrected

    def remove_background(
        self,
        image: np.ndarray,
        lower_green: Tuple[int, int, int] = (25, 40, 40),
        upper_green: Tuple[int, int, int] = (90, 255, 255)
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simple background removal using color thresholding

        Args:
            image: Input image array (RGB)
            lower_green: Lower HSV threshold for green
            upper_green: Upper HSV threshold for green

        Returns:
            Tuple of (masked image, binary mask)
        """
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        # Create mask for green color
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Invert mask (we want the cabbage, not the background)
        mask = cv2.bitwise_not(mask)

        # Apply morphological operations to clean up mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Apply mask to image
        masked_image = cv2.bitwise_and(image, image, mask=mask)

        return masked_image, mask

    def augment_image(
        self,
        image: np.ndarray,
        flip_horizontal: bool = False,
        rotate_angle: Optional[float] = None,
        brightness_factor: Optional[float] = None
    ) -> np.ndarray:
        """
        Apply data augmentation to image

        Args:
            image: Input image array
            flip_horizontal: Whether to flip horizontally
            rotate_angle: Rotation angle in degrees
            brightness_factor: Brightness adjustment factor (1.0 = no change)

        Returns:
            Augmented image
        """
        augmented = image.copy()

        # Horizontal flip
        if flip_horizontal:
            augmented = cv2.flip(augmented, 1)

        # Rotation
        if rotate_angle is not None:
            h, w = augmented.shape[:2]
            center = (w // 2, h // 2)
            matrix = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
            augmented = cv2.warpAffine(augmented, matrix, (w, h))

        # Brightness adjustment
        if brightness_factor is not None:
            augmented = np.clip(augmented * brightness_factor, 0, 255).astype(np.uint8)

        return augmented

    def get_image_stats(self, image: np.ndarray) -> dict:
        """
        Get statistics about the image

        Args:
            image: Input image array

        Returns:
            Dictionary with image statistics
        """
        return {
            'shape': image.shape,
            'dtype': str(image.dtype),
            'min': float(np.min(image)),
            'max': float(np.max(image)),
            'mean': float(np.mean(image)),
            'std': float(np.std(image))
        }
