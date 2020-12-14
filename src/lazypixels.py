import cv2
from pathlib import Path
import random


def crypt(img, key):
    key_data = collect_key_data(key)
    rows, cols = img.shape[:-1]

    for target, digits in key_data.items():
        frm = target * SEGMENT_SIZE
        if frm + SEGMENT_SIZE > rows:
            to = rows
        else:
            to = frm + SEGMENT_SIZE

        digit = 0
        for i in range(frm, to):
            for j in range(cols):
                bgr = list(img[i, j])
                new_bgr = list()
                for value in bgr:
                    value_str = str(value)
                    while len(value_str) != 3:
                        value_str = '0' + value_str

                    index = 0
                    for x in range(digits[digit]):
                        index += 1
                        if index == len(value_str):
                            index = 0

                    new_digit = digits[digit]
                    for x in range(index):
                        new_digit = new_digit * 10

                    n = (int(value_str) + new_digit) // 256
                    new_value = value + new_digit - 256 * n

                    new_bgr.append(new_value)
                    digit = check_digit(digit)
                img[i, j] = new_bgr
    cv2.imwrite(str(IMAGE), img)
    return img


def decrypt(img, key):
    key_data = collect_key_data(key)
    rows, cols = img.shape[:-1]

    for target, digits in key_data.items():
        frm = target * SEGMENT_SIZE
        if frm + SEGMENT_SIZE > rows:
            to = rows
        else:
            to = frm + SEGMENT_SIZE
        
        digit = 0
        for i in range(frm, to):
            for j in range(cols):
                bgr = list(img[i, j])
                new_bgr = list()
                for value in bgr:
                    value_str = str(value)
                    while len(value_str) != 3:
                        value_str = '0' + value_str

                    index = 0
                    for x in range(digits[digit]):
                        if index + 1 == len(value_str):
                            index = 0
                        index += 1

                    new_digit = digits[digit]
                    for x in range(index):
                        new_digit *= 10

                    new_value = int(value_str) - new_digit
                    while new_value < 0:
                        new_value += 256

                    new_bgr.append(new_value)
                    digit = check_digit(digit)
                img[i, j] = new_bgr
    cv2.imwrite(str(IMAGE), img)
    return img


def generate_key(segments):
    key = ''
    for i in range(segments):
        key += str(i)
        for i in range(12):
            int_digit = random.randint(0, 15)
            hex_digit = hex(int_digit)[2:]
            key += hex_digit
        key += '-'
    return key[:-1]


def check_digit(digit):
    digit = digit + 1
    if digit == 12:
        return 0
    else:
        return digit


def collect_key_data(key):
    key_segments = key.split('-')

    key_data = {}
    for segment in key_segments:
        segment_target = int(segment[:-12])
        segment_key = segment[1:]

        key_data[segment_target] = []
        for digit in segment_key:
            key_data[segment_target].append(int(digit, 16))
    return key_data


IMAGE  = Path()

# length fo rows per image segment
SEGMENT_SIZE = 50

img = cv2.imread(str(IMAGE))
rows, cols = img.shape[:-1]
segments = rows / SEGMENT_SIZE

if type(segments) == float:
    segments = int(segments) + 1

key = generate_key(segments)
crypt(img, key)
print('Generated key: {}'.format(key))
decrypt(img, key)
