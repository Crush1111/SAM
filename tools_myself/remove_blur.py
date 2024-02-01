# -*- coding: utf-8 -*-
# Author: Bin-ze
# Email: binze.zero@gmail.com
# Date: 2023/12/28 10:08
# File Name: remove_blur.py

"""
Description of the script or module goes here.
from https://github.com/graphdeco-inria/gaussian-splatting/pull/348

Usage

blur_remove(folder_name)
this will open the images file and remove images that are blurry.

Logic

Laplacian variance helps to calculate the sharpness of the image and this is done for every image inside our dataset.
Next, the mean Laplacian variance is calculated for all images and the standard deviation is calculated as well.
Using this I choose a threshold that is set to be anything lower than mean - standard deviation.
Any image with a Laplacian variance lower than this set threshold is removed from the dataset.
Laplacian variance is a measure of the sharpness of an image.
It is calculated by computing the Laplacian of the image and then taking the variance of the Laplacian.
The Laplacian of an image is a second-order derivative, which means that it highlights high-frequency features in the image.

Here's the assumption:
If the image contains high variance, there is a wide response, including both edge and non-edge classes, representing normal focused images.
If the variance is very low, the response distribution is small, indicating very small edges in the image.
The blurrier the image, the smaller the edges.

The method of calculating the Laplacian mean and variance for the entire dataset to obtain an adaptive threshold seems unreliable,
Analysis:
This design is reasonable in a 360-degree scene because the scene is always centered in the field of view, and there will not be significant deviations in a series of captures.
However, it is different in large-scale scene capture. A simple example is moving from a high-texture area to a low-texture area. In such cases, this design may remove all low-texture captures, which is obviously an incorrect attempt.

How to solve it?
As a threshold-sensitive blur detection method, the threshold

"""

import cv2
import sys
import os
import argparse
import logging

import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

def blur_remove(input_folder, output_folder):
    # Go through the folder of images.
    logging.info("================================================================================================\n")
    logging.info(f"              Removing blurry images:   {input_folder} \n")
    logging.info("================================================================================================\n")
    image_paths = []
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        if os.path.isfile(file_path):
            image_paths.append(file_path)

    # Calculate the Laplacian and Laplacian variance of all images to detect which images are blurry.
    laplacian_variances = []
    for image_path in image_paths:
        image = cv2.imread(image_path)
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except:
            print('1')
        laplacian_variance = cv2.Laplacian(gray, cv2.CV_64F).var()

        laplacian_variances.append(laplacian_variance)

    # Calculate the mean and standard deviation of the Laplacian variance.
    mean_laplacian_variance = np.mean(laplacian_variances)
    std_laplacian_variance = np.std(laplacian_variances)

    # Plot a histogram showing the Laplacian variance on the x-axis and frequency on the y-axis.
    plt.hist(laplacian_variances)
    plt.xlabel('Laplacian Variance')
    plt.ylabel('Frequency')
    plt.title('Laplacian Variance Histogram')
    # Save the histogram outside the images folder.
    histogram_path = os.path.join(input_folder, 'laplacian_variance_histogram.png')
    # plt.savefig(histogram_path)
    plt.show()

    # Calculate the threshold for blurry images.
    if mean_laplacian_variance < std_laplacian_variance:
        logging.info("Dataset is skewed")
        threshold = mean_laplacian_variance - std_laplacian_variance / 2.5
    else:
        threshold = mean_laplacian_variance - std_laplacian_variance
        logging.info("Dataset is normal")

    threshold = threshold + 30  # aggressive image threshold
    logging.info(f"Mean Laplacian Variance: {mean_laplacian_variance}")
    logging.info(f"Standard Deviation: {std_laplacian_variance}")
    logging.info(f"Threshold: {threshold}")

    # Delete all blurry images.
    blurry_image_paths = []
    # Create a folder to store blurry files
    output_blur_folder =os.path.join(output_folder, "blurry_images")
    os.makedirs(output_blur_folder, exist_ok=True)

    for image_path, laplacian_variance in zip(image_paths, laplacian_variances):
        if laplacian_variance < threshold:
            blurry_image_paths.append(image_path)
            image_name = os.path.basename(image_path)
            output_image_path = os.path.join(output_blur_folder, image_name)
            os.rename(image_path, output_image_path)

    # Print the paths of the blurry images.
    logging.info("Blurred images: \n")
    for image_path in blurry_image_paths:
        logging.info(image_path)

    logging.info("================================================================================================\n")
    logging.info(f"              Number of blurry images detected: {len(blurry_image_paths)} \n")
    logging.info("================================================================================================\n")

    # Save the updated histogram with blurry images removed.
    plt.hist(laplacian_variances)
    plt.xlabel('Laplacian Variance')
    plt.ylabel('Frequency')
    plt.title('Laplacian Variance Histogram (Blurry Images Removed)')
    # Save the histogram outside the images folder.
    updated_histogram_path = os.path.join(input_folder, 'laplacian_variance_histogram_updated.png')
    # plt.savefig(updated_histogram_path)
    plt.show()

    logging.info(f"              Updating histogram: \n")
    logging.info(updated_histogram_path)
    logging.info("================================================================================================\n")

if __name__ == '__main__':
    # Create command-line arguments parser
    parser = argparse.ArgumentParser(description='Script to remove blurry images from a folder.')
    parser.add_argument('input_folder', type=str, help='Path to the folder containing the input images.')
    parser.add_argument('output_folder', type=str, help='Path to the folder where the output images will be stored.')

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the blur_remove function with the provided input and output folder paths
    blur_remove(args.input_folder, args.output_folder)