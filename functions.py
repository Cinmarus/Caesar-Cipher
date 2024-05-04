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


def get_nominal_freq():
    with open('ch-freq-en.txt', 'r') as file:
        lines = file.readlines()
        nominal_freq = {}
        for i in lines:
            i = i.split()
            nominal_freq.update({i[0].lower(): float(i[1])})
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
    diff_base = 200
    for shift in range(0, 25):
        new_text = try_shift(text_lst.copy(), shift)
        new_diff = calc_diff(new_text)
        if new_diff < diff_base:
            diff_base = new_diff
            key = shift
    return key


def try_shift(text, shift):             # do przerobienia bo wygląda jak gówno
    for i in range(len(text)):
        xD = 0
        if 65 <= ord(text[i]) <= 90:
            text[i] = text[i].lower()
            xD = 1
        if ord(text[i]) < 97 or ord(text[i]) > 122:
            continue
        if ord(text[i]) + shift <= 122:
            b = ord(text[i]) + shift
        else:
            b = ord(text[i]) + shift - 26
        if xD == 1:
            text[i] = chr(b).upper()
        else:
            text[i] = chr(b)
    return text


def calc_diff(text):
    freq = get_freq(text)
    nominal_freq = get_nominal_freq()
    diff = 0
    for i in freq:
        diff += abs(freq[i] - nominal_freq[i])
    return diff


def decode(file, shift):
    with open(f'secret_files/{file}.txt', 'r') as file:
        text = file.read()
        decoded = try_shift(list(text), shift)
    return ''.join(decoded)


def save_to_file(source, file_name):
    with open(f'desecretised_files\desecretised_{file_name}.txt', 'w') as file:
        file.write(source)


def main():
    print_menu()
    file_to_decode = choose_file()
    content = get_file(file_to_decode)
    key = find_key(content)
    print('The key used for decoding is:', key)
    print(f'Your decoded text is saved into file: decoded_{file_to_decode}.txt')
    decoded = decode(file_to_decode, key)
    save_to_file(decoded, file_to_decode)