from functions import *

print_menu()
file_to_decode = choose_file()
content = get_file(file_to_decode)
get_freq(content)

