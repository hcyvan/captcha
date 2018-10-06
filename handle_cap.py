import os
from PIL import Image


def test():
    cap = '1538763811397.png'
    img = Image.open(os.path.join('sina', cap))
    img = img.convert('RGB')

    for i in range(100):
        to_remove = []
        for j in range(40):
            r, g, b = img.getpixel((i, j))
            if r == 101 and g == 101:
                # img.putpixel((i, j), (255, 255, 255))
                if len(to_remove)==0 or to_remove[-1][1] == j-1:
                    to_remove.append((i, j))
            else:
                if len(to_remove) >= 2:
                    for x, y in to_remove:
                        img.putpixel((x, y), (255, 255, 255))
                to_remove = []

    img.save(os.path.join('sina_handled', cap+'-2.png'))


def resize_sina_cap():
    sample_dir = './sina/test'
    sample_resize_dir = './sina/test_resize'
    for cap_file in os.listdir(sample_dir):
        cap = os.path.join(sample_dir, cap_file)
        img = Image.open(cap)
        img.resize((160,60), Image.ANTIALIAS)
        img.save(os.path.join(sample_resize_dir, cap_file))


if __name__ == '__main__':
    resize_sina_cap()
