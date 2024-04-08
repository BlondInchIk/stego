from PIL import Image

def encode_image(image_path, message):
    img = Image.open(image_path)
    width, height = img.size
    pixel_map = img.load()

    message_bits = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'
    message_index = 0

    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]

            modified_pixel = list(pixel)
            for i in range(3):  # для каждого канала (r, g, b)
                if message_index < len(message_bits):
                    bit = int(message_bits[message_index])
                    if bit == 0:
                        if modified_pixel[i] % 2 != 0:
                            modified_pixel[i] -= 1
                    else:
                        if modified_pixel[i] % 2 == 0:
                            modified_pixel[i] += 1
                    message_index += 1

            pixel_map[x, y] = tuple(modified_pixel)

    img.save('encoded_image.png')

def decode_image(image_path):
    img = Image.open(image_path)
    width, height = img.size
    pixel_map = img.load()

    message_bits = ''

    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]
            for i in range(3):
                message_bits += str(pixel[i] % 2)

    message = ''
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        if byte == '11111111':
            break
        message += chr(int(byte, 2))

    return message

# Пример использования
print("loading...")

# Чтение секретного текста из файла
with open("t.txt", "r") as file:
    secret_message = file.read()

# secret_message = ("I am writing to you - what more? What more can I say? Now, I know, it is in your will to punish Me with contempt.")
encode_image("mouse.png", secret_message)

# Извлечение сообщения из изображения
decoded_message = decode_image("encoded_image.png")

# Сохранение расшифрованного сообщения в файле decode.txt
with open("decode.txt", "w") as file:
    file.write(decoded_message)

# Если ошибка, проверим кодировку (Для больших текстов)
# with open("decode.txt", "w", encoding="utf-8") as file:
#     file.write(decoded_message)
print("Done")

