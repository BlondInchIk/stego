import os
import sys
import imageio
import scipy.fftpack
import scipy.signal
import scipy.ndimage
import numpy as np
import random
from PIL import Image, ImageChops

def generate_difference_image(image1_path, image2_path, output_path):
    # Загрузка изображений
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Создание маски различий
    diff = ImageChops.difference(image1, image2)
    mask = diff.convert('L').point(lambda x: 255 if x != 0 else 0, '1')

    # Наложение маски на оригинальное изображение
    masked_image = Image.composite(image1, Image.new('RGB', image1.size, 'black'), mask)

    # Сохранение результата
    masked_image.save(output_path)
    print("Создано изображение с видимыми изменениями:", output_path)

def generate_random_sequence(seed, length):
    random.seed(seed)
    sequence = [random.randint(0, 40) for _ in range(length)]
    return sequence

def ternary_entropyf(pP1, pM1):
    p0 = 1-pP1-pM1
    P = np.hstack((p0.flatten(), pP1.flatten(), pM1.flatten()))
    H = -P*np.log2(P)
    eps = 2.2204e-16
    H[P<eps] = 0
    H[P>1-eps] = 0
    return np.sum(H)

def calc_lambda(rho_p1, rho_m1, message_length, n):
    l3 = 1e+3
    m3 = float(message_length+1)
    iterations = 0
    while m3 > message_length:
        l3 = l3 * 2
        pP1 = (np.exp(-l3 * rho_p1)) / (1 + np.exp(-l3 * rho_p1) + np.exp(-l3 * rho_m1))
        pM1 = (np.exp(-l3 * rho_m1)) / (1 + np.exp(-l3 * rho_p1) + np.exp(-l3 * rho_m1))
        m3 = ternary_entropyf(pP1, pM1)
        iterations += 1
        if iterations > 10: return l3
    l1 = 0
    m1 = float(n)
    lamb = 0
    iterations = 0
    alpha = float(message_length)/n
    while float(m1-m3)/n > alpha/1000.0 and iterations<300:
        lamb = l1+(l3-l1)/2
        pP1 = (np.exp(-lamb*rho_p1))/(1+np.exp(-lamb*rho_p1)+np.exp(-lamb*rho_m1))
        pM1 = (np.exp(-lamb*rho_m1))/(1+np.exp(-lamb*rho_p1)+np.exp(-lamb*rho_m1))
        m2 = ternary_entropyf(pP1, pM1)
        if m2 < message_length:
            l3 = lamb
            m3 = m2
        else:
            l1 = lamb
            m1 = m2
    iterations = iterations + 1
    return lamb

def embed(x, rho_p1, rho_m1, m, custom_data, seed):
    n = x.shape[0] * x.shape[1]
    lamb = calc_lambda(rho_p1, rho_m1, m, n)
    pChangeP1 = (np.exp(-lamb * rho_p1)) / (1 + np.exp(-lamb * rho_p1) + np.exp(-lamb * rho_m1))
    pChangeM1 = (np.exp(-lamb * rho_m1)) / (1 + np.exp(-lamb * rho_p1) + np.exp(-lamb * rho_m1))
    y = x.copy()
    randChange = np.random.rand(y.shape[0], y.shape[1])
    y[randChange < pChangeP1] = y[randChange < pChangeP1] + 1;
    y[(randChange >= pChangeP1) & (randChange < pChangeP1+pChangeM1)] = y[(randChange >= pChangeP1) & (randChange < pChangeP1+pChangeM1)] - 1;
    data = "".join(format(ord(char), '08b') for char in custom_data)
    binary_data = []
    for char in data:
        binary_data.append(int(char))
    y = y.reshape(-1)
    flag = 0
    lenArray = len(binary_data)
    point = 0
    while flag != lenArray:
        if seed[point] == 1:
            if binary_data[flag] == 1:
                if y[point] % 2 == 0:
                    y[point] += 1
            else:
                if y[point] % 2 != 0:
                    y[point] -= 1
            flag += 1
            point += 1
        else:
            point += 1
            continue
            
    y = y.reshape((x.shape[0],x.shape[1]))
    return y

def find(x, seed):
    # lamb = calc_lambda(rho_p1, rho_m1, m, n)
    # pChangeP1 = (np.exp(-lamb * rho_p1)) / (1 + np.exp(-lamb * rho_p1) + np.exp(-lamb * rho_m1))
    # pChangeM1 = (np.exp(-lamb * rho_m1)) / (1 + np.exp(-lamb * rho_p1) + np.exp(-lamb * rho_m1))
    y = x.copy()
    y = y.reshape(-1)
    result = ""
    string = '' 
    text = open('output.txt', 'w', encoding='utf-8')
    lenArray = len(seed)
    point = 0
    while point != lenArray:
        if seed[point] == 1:
            if y[point] % 2 == 0:
                result += '0'
            elif y[point] % 2 != 0:
                result += '1'
            point += 1
        else:
            point += 1
            continue
    bytes_list = [result[i:i+8] for i in range(0, len(result), 8)]
    for bytes in bytes_list:
        num = int(bytes, 2)
        if 31 < num < 127:
            string += chr(num)
    text.write(string)
    text.close()
    y = y.reshape((x.shape[0],x.shape[1]))
    return y

def cost_fn(cover):
    k, l = cover.shape[:2]
    hpdf = np.array([
        -0.0544158422,  0.3128715909, -0.6756307363,  0.5853546837,  
         0.0158291053, -0.2840155430, -0.0004724846,  0.1287474266,  
         0.0173693010, -0.0440882539, -0.0139810279,  0.0087460940,  
         0.0048703530, -0.0003917404, -0.0006754494, -0.0001174768
    ])        
    sign = np.array([-1 if i%2 else 1 for i in range(len(hpdf))])
    lpdf = hpdf[::-1] * sign
    F = []
    F.append(np.outer(lpdf.T, hpdf))
    F.append(np.outer(hpdf.T, lpdf))
    F.append(np.outer(hpdf.T, hpdf))
    sgm, pad_size = 1, 16
    rho = np.zeros((k, l))
    for i in range(3):
        cover_padded = np.pad(cover, (pad_size, pad_size), 'symmetric').astype('float32')
        R0 = scipy.signal.convolve2d(cover_padded, F[i], mode="same")
        X = scipy.signal.convolve2d(1./(np.abs(R0)+sgm), np.rot90(np.abs(F[i]), 2), 'same');
        if F[0].shape[0]%2 == 0: X = np.roll(X, 1, axis=0)
        if F[0].shape[1]%2 == 0: X = np.roll(X, 1, axis=1)
        X = X[(X.shape[0]-k)//2:-(X.shape[0]-k)//2, (X.shape[1]-l)//2:-(X.shape[1]-l)//2]
        rho += X
    wet_cost = 10**13
    rho_m1 = rho.copy()
    rho_p1 = rho.copy()
    rho_p1[rho_p1>wet_cost] = wet_cost
    rho_p1[np.isnan(rho_p1)] = wet_cost
    rho_p1[cover==255] = wet_cost
    rho_m1[rho_m1>wet_cost] = wet_cost
    rho_m1[np.isnan(rho_m1)] = wet_cost
    rho_m1[cover==0] = wet_cost
    return rho_p1, rho_m1 


def hide(cover_path, stego_path, data, key):
    cover = imageio.imread(cover_path)
    stego = cover.copy()
    seed = generate_random_sequence(key, cover[:,:,1].shape[0] * cover[:,:,1].shape[1])
    for channel in range(3):
        rho_p1, rho_m1 = cost_fn(cover[:,:,channel])
        sz = len(data) * 8
        stego[:,:,channel] = embed(cover[:,:,channel], rho_p1, rho_m1, sz, data, seed)
        print("channel:", channel, "modifs:", np.sum(np.abs(stego[:,:,channel].astype("int16")-cover[:,:,channel].astype("int16"))))
    imageio.imwrite(stego_path, stego)

def show(cover_path, key):
    cover = imageio.imread(cover_path)
    stego = cover.copy()
    seed = generate_random_sequence(key, cover[:,:,1].shape[0] * cover[:,:,1].shape[1])
    stego[:,:,1] = find(cover[:,:,1],seed)
    # imageio.imwrite(stego_path, stego)

def read_data(file_path):
       with open(file_path, 'r') as file:
           message = file.read()
       return message

if __name__ == "__main__":
    if sys.argv[2] == '0':
        data_path = sys.argv[4]
        data = read_data(data_path)
        hide(sys.argv[1], sys.argv[3], data, 10)
        output_path = 'difference_image.jpg'  # Путь для сохранения результирующего изображения

        generate_difference_image(sys.argv[1], sys.argv[3], output_path)

    elif sys.argv[2] == '1':
        show(sys.argv[1], 10)