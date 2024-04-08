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

        for i in range(len(fft_shifted)):
            for j in range(len(fft_shifted[i])):
                text_binary += str(int(fft_shifted[i][j].real) % 2)

        return text_binary

    if mode == 0:

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

        encoded_image = Image.open(image_path)
        encoded_pixels = np.array(encoded_image)
        decoded_text_binary = fft_decode(encoded_pixels)
        decoded_text = ''

        for i in range(0, len(decoded_text_binary), 8):
            byte = decoded_text_binary[i:i + 8]
            decoded_text += chr(int(byte, 2))
            if decoded_text.endswith(' '):
                break

        with open('output.txt', 'w') as file:
            file.write(decoded_text)

if __name__ == "__main__":

    if sys.argv[2] == '0':
        steganography(sys.argv[1], 0, sys.argv[3], sys.argv[4])

    elif sys.argv[2] == '1':
        steganography(sys.argv[3], 1, text_file='output.txt')