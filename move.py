import os

x = os.listdir('pics/validation')
for folder in x:
    y = os.listdir('pics/validation/' + folder)
    for file in y:
        print (folder)
        print (file)
        path = 'pics/validation/' + folder + '/'
        n = file.split('.')[0]
        toPath = 'pics/train/'
        os.rename(path + file, toPath + folder + '/' + file)