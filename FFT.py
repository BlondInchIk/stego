from PIL import Image
import numpy as np
import numpy.fft as fft
import sys


def steganography(image_path, mode, output_image=None, text_file=None):
    def fft_encode(pixels, text_binary):

        fft_pixels = fft.fft2(pixels)
        fft_shifted = fft.fftshift(fft_pixels)
        text_idx = 0

        for i in range(len(fft_shifted)):
            for j in range(len(fft_shifted[i])):
                if text_idx < len(text_binary):
                    fft_shifted[i][j] = fft_shifted[i][j] + int(text_binary[text_idx])
                    text_idx += 1

        fft_shifted = fft.ifftshift(fft_shifted)
        encoded_pixels = fft.ifft2(fft_shifted).real.astype(np.uint8)
        return encoded_pixels

    def fft_decode(encoded_pixels):

        fft_pixels = fft.fft2(encoded_pixels)
        fft_shifted = fft.fftshift(fft_pixels)
        text_binary = ''
        text_length = 0

        for i in range(len(fft_shifted)):
            for j in range(len(fft_shifted[i])):
                text_binary += str(int(abs(fft_shifted[i][j][0])) % 2)
                text_length += 1
                if text_length % 8 == 0 and text_binary[-8:] == '00000000':
                    break
            else:
                continue
            break

        text_binary = text_binary[:-(text_length % 8)]  # Remove padding bits

        return text_binary

    if mode == 0:
        if output_image is None or text_file is None:
            print("Error: Output image path and text file path are required in encode mode (mode 0).")
            return

        image = Image.open(image_path)
        with open(text_file, 'r') as file:
            text = file.read()

        width, height = image.size
        text += ' ' * (width * height - len(text))
        text_binary = ''.join(format(ord(char), '08b') for char in text)

        pixels = np.array(image)
        encoded_pixels = fft_encode(pixels, text_binary)
        stego_image = Image.fromarray(encoded_pixels)
        stego_image.save(output_image)

    elif mode == 1:
        if text_file is None:
            print("Error: Output text file path is required in decode mode (mode 1).")
            return

        encoded_image = Image.open(image_path)
        encoded_pixels = np.array(encoded_image)
        decoded_text_binary = fft_decode(encoded_pixels)
        decoded_text = ''

        for i in range(0, len(decoded_text_binary), 8):
            byte = decoded_text_binary[i:i + 8]
            decoded_text += chr(int(byte, 2))
            if decoded_text.endswith(' '):
                break

        with open(text_file, 'w', encoding='utf8') as file:
            file.write(decoded_text)


if len(sys.argv) < 2:
    print("Usage: python script.py <image_path> <mode> <output_image> <text_file>")

image_path = input("Enter image path: ")
mode = int(input("Enter mode (0 for encode, 1 for decode): "))

if mode == 0:
    output_image = input("Enter output image path: ")
    text_file = input("Enter text file path: ")
    steganography(image_path, mode, output_image, text_file)
elif mode == 1:
    text_file = input("Enter output text file path: ")
    steganography(image_path, mode, text_file=text_file)
else:
    print("Invalid mode. Please enter 0 for encode or 1 for decode.")
