import re

def number_sort(img1, img2):
    num1 = re.findall(r'.*?([0-9]+)', img1)[0]
    num2 = re.findall(r'.*?([0-9]+)', img2)[0]
    if int(num1) < int(num2):
        return -1
    if int(num1) == int(num2):
        return 0
    return 1
