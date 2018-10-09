import math
import string

IMAGE_HEIGHT = 40
IMAGE_WIDTH = 100
MAX_CAPTCHA = 5
CHAR_SET = string.digits + string.ascii_letters
CKPT_PATH = './model/sina90/sina.capcha'
BOARD_PATH = './board/sina4'
LOG_PATH = './log/sina4.log'
STOP_ACC = 0.95

CHAR_SET_LEN = len(CHAR_SET)
IMAGE_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, 3)
IMAGE_HEIGHT_AFTER_3_CONV = math.ceil(math.ceil(math.ceil(IMAGE_HEIGHT/2)/2)/2)
IMAGE_WIDTH_AFTER_3_CONV = math.ceil(math.ceil(math.ceil(IMAGE_WIDTH/2)/2)/2)
