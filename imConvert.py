from PIL import Image
import os
x = os.listdir('pics/validation')
for folder in x:
    y = os.listdir('pics/validation/' + folder)
    for file in y:
        print (folder)
        print (file)
        path = 'pics/validation/' + folder + '/'
        n = file.split('.')[0]
        im = Image.open(path + file)
        
        im = im.convert("RGB")
        im.save(path + n + '.jpg')
        os.remove(path + file)