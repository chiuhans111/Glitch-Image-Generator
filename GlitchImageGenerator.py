# Glitch Image Generator
# Author: Hans chiu (twitter: @chiu_hans)

from PIL import Image, ImageFile
import numpy as np
import io

ImageFile.LOAD_TRUNCATED_IMAGES = True


def img2data(img, quality=10):
    """encode the image"""
    file = io.BytesIO()
    file.name = 'file.jpg'
    img.save(file, quality=quality)
    return list(file.getvalue())


def data2img(data):
    """decode the image"""
    file = io.BytesIO()
    file.write(bytearray(data))
    return Image.open(file)


def glitch(img, amount=10, quality=10):
    """glitch the image"""
    img = img.convert('RGB')

    while True:
        # only break the loop when image is successfully glitched
        try:
            data = img2data(img, quality=quality)

            for t in range(amount):
                # glitch the data
                i = np.random.randint(0, len(data))
                data[i] ^= 1 << np.random.randint(8)

            data = np.array(data).astype('uint8')
            result = data2img(data)

            if np.sum(np.abs(np.array(result) - np.array(img))) == 0:
                raise Exception('same')

            if np.sum(np.abs(np.array(result))) == 0:
                raise Exception('empty')

        except Exception as e:
            # glitch again, this one doesn't work
            continue

        break
    return result


# The following code is just a example:

img_array = np.random.rand(64, 64, 3)*255
img = Image.fromarray(img_array.astype('uint8'))
img = glitch(img, 20, 80)
img = img.resize([512, 512], Image.NEAREST)
img = glitch(img, 50, 80)
img.save(f'./glitched_img.jpg')
