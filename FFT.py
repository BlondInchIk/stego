import numpy as np
from PIL import Image

def text_to_binary(text):
    """Convert text to binary string"""
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def embed_text(image_path, text_file_path, output_image_path):
    """Embed text into image using FFT"""
    # Load image
    image = np.array(Image.open(image_path))
    # Convert text to binary
    with open(text_file_path, 'r') as file:
        text = file.read()
    binary_text = text_to_binary(text)
    # Check if text can fit in the image
    if len(binary_text) > image.size:
        print("Text is too long to embed in the image.")
        return
    # Perform FFT
    fft_image = np.fft.fft2(image)
    # Embed text in the FFT image
    for i, bit in enumerate(binary_text):
        x = i // image.shape[1]
        y = i % image.shape[1]
        if bit == '1':
            fft_image[x, y] = fft_image[x, y] + 100  # Add a small value to change the FFT result
        else:
            fft_image[x, y] = fft_image[x, y] - 100  # Subtract a small value to change the FFT result
    # Perform inverse FFT
    embedded_image = np.fft.ifft2(fft_image).real
    # Normalize the values
    embedded_image = np.uint8(embedded_image)
    # Save the resulting image
    result_image = Image.fromarray(embedded_image)
    result_image.save(output_image_path)
    print("Text embedded successfully!")

# Пример использования
embed_text("stego.png", "C:/Users/vladi/OneDrive/Документы/text.txt", "C:/Usersvladi\OneDrive\Документы\output_image_embedded.bmp")

def extract_text(image_path, output_text_file):
    """Extract text from image using FFT"""
    # Load image
    image = np.array(Image.open(image_path))
    # Perform FFT
    fft_image = np.fft.fft2(image)
    # Initialize empty binary string
    binary_text = ''
    # Extract text from the FFT image
    for i in range(image.size):
        x = i // image.shape[1]
        y = i % image.shape[1]
        # If FFT coefficient is greater than the original image, assume it's a '1'
        if fft_image[x, y] > image[x, y]:
            binary_text += '1'
        else:
            binary_text += '0'
    # Convert binary text to ASCII text
    text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
    # Save the extracted text to a file
    with open(output_text_file, 'w') as file:
        file.write(text)
    print("Text extracted successfully!")

# Пример использования
extract_text("C:\Users\vladi\OneDrive\Документы\output_image_embedded.bmp", "C:\Users\vladi\OneDrive\Документы/extracted_text.txt")
