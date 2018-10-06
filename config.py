import string

IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160
MAX_CAPTCHA = 4
CHAR_SET = string.digits + string.ascii_letters
CHAR_SET_LEN = len(CHAR_SET)
IMAGE_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, 3)
