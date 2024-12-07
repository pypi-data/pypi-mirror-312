"""
Created on Nov 24, 2018\n
@author: Unknown
"""


import os
import shutil

class Lab1:
    """
    image operation, Grayscale, Resize, shapes, blur, crop, text to image, image pixel, thresholding, rotation, blending, histogram, bitwise
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-1') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 1 PDF copied to current directory: {filename}"
        return "Lab 1 PDF not found"

class Lab2:
    """
    point processing, Pixel Transformation, Color spaces, Power Law etc
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-2') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 2 PDF copied to current directory: {filename}"
        return "Lab 2 PDF not found"

class Lab3:
    """
    Linear Filtering, Filters, Smoothing, Edge Detection, Non Linear filtering, 1D 2D Sampling, Fourier Transformation, hybrid Images
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-3') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 3 PDF copied to current directory: {filename}"
        return "Lab 3 PDF not found"

class Lab4:
    """
    Feature Extraction, Histogram, LBP, convolution, Edge detector, corner detection
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-4') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 4 PDF copied to current directory: {filename}"
        return "Lab 4 PDF not found"

class Lab5:
    """
    Image segmentation, thresholding, watershed, clustering
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-5') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 5 PDF copied to current directory: {filename}"
        return "Lab 5 PDF not found"

class Lab6:
    """
    CNN, AlexNet, GoogleNet
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-6') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 6 PDF copied to current directory: {filename}"
        return "Lab 6 PDF not found"

class Lab7:
    """
    Wavelet Transformation, Boundary Detection, Hough Transformation, Line Detection by Hough Transformation, SIFT Feature Extraction
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-7') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 7 PDF copied to current directory: {filename}"
        return "Lab 7 PDF not found"

class Lab8:
    """
    RCNN, YOLO
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-8') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 8 PDF copied to current directory: {filename}"
        return "Lab 8 PDF not found"

class Lab9:
    """
    A: DCGAN, GAN ; B: CNN and LSTM
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-9') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 9 PDF copied to current directory: {filename}"
        return "Lab 9 PDF not found"

class Lab10:
    """
    Autoencoders, VAE
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-10') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 10 PDF copied to current directory: {filename}"
        return "Lab 10 PDF not found"

class Lab11:
    """
    Transformers, ViT, Self Attention
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-11') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 11 PDF copied to current directory: {filename}"
        return "Lab 11 PDF not found"

class Lab12:
    """
    VAE in detail.
    """
    def get_pdf(self):
        for folder in ['lab_tasks', 'lab_manuals']:
            for filename in os.listdir(folder):
                if filename.startswith('CV Lab-12') and filename.endswith('.pdf'):
                    file_path = os.path.join(folder, filename)
                    shutil.copy(file_path, os.getcwd())  # Copy to current directory
                    return f"Lab 12 PDF copied to current directory: {filename}"
        return "Lab 12 PDF not found"

class LabTasks:
    def copy_all(self):
        source_folder = 'lab_tasks'
        destination_folder = os.path.join(os.getcwd(), 'Lab Tasks')  # Current working directory + Lab Tasks folder
        
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            return f"The source folder '{source_folder}' does not exist."
        
        # Create the destination folder 'Lab Tasks' if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f"Created folder: {destination_folder}")
        
        # Iterate over all the files and subfolders in lab_tasks folder
        for item in os.listdir(source_folder):
            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)
            
            # If it's a directory, use shutil.copytree to copy the entire directory
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)
                print(f"Directory {source_path} copied to {destination_path}")
            
            # If it's a file, use shutil.copy to copy the file
            elif os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)
                print(f"File {source_path} copied to {destination_path}")
        
        return "All files and directories from 'lab_tasks' have been copied to 'Lab Tasks' folder in the current directory."