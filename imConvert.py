from PIL import Image
import os
x = os.listdir('pics/train')
for folder in x:
    y = os.listdir('pics/train/' + folder)
    for file in y:
        print (folder)
        print (file)
        path = 'pics/train/' + folder + '/'
        n = file.split('.')[0]
        im = Image.open(path + file)
        im = im.convert("RGB")
        im.save(path + n + '.jpg')