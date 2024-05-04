import re
import os


def print_menu():
    print("Select file that you want to decode:")
    for i in read_folder():
        print(i)
    print("If you have changed your mind type: Exit")


def choose_file():
    file_to_decode = input("Enter the name of the file: ").strip().lower()
    if file_to_decode in read_folder():
        return file_to_decode
    elif file_to_decode == 'exit':
        print("Goodbye!")
        exit()
    else:
        print("File not found")
        return choose_file()


def read_folder():
    file_list = []
    for file in os.listdir('secret_files'):
        if file.endswith('.txt'):
            file_list.append(file)
    file_list = [os.path.splitext(filename)[0] for filename in file_list]
    return file_list


print(read_folder())


def get_nominal_freq():
    with open('ch-freq-en.txt', 'r') as file:
        lines = file.readlines()
        nominal_freq = {}
        for i in lines:
            i = i.split()
            nominal_freq.update({i[0]: float(i[1])})
        return nominal_freq


def get_file(file):
    with open(f'secret_files/{file}.txt', 'r') as file:
        text = re.sub(r'[^a-zA-Z]', '', file.read()).lower()
    return text


def get_freq(text):
    freq = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
            'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
    letters = 0
    for i in text:
        if i in freq:
            freq[i] += 1
        letters += 1
    freq = {k: v * 100 / letters for k, v in freq.items()}
    return freq


def find_key(text):
    text_lst = list(text)
    diff_base = 100
    for shift in range(1, 25):
        new_text = try_shift(text_lst, shift)
        if calc_diff(new_text) < diff_base:
            diff_base = calc_diff(new_text)
            key = shift
    return key


def try_shift(text, shift):
    for i in range(len(text)):
        if ord(text[i]) + shift <= 122:
            b = ord(text[i]) + shift
        else:
            b = ord(text[i]) + shift - 26
        text[i] = chr(b)
    return text


def calc_diff(text):
    freq = get_freq(text)
    nominal_freq = get_nominal_freq()
    diff = 0
    for i in freq:
        diff += abs(freq[i] - nominal_freq[i])
    return diff



