import os
y = os.listdir("pics/train")
for thing in y:
    x = os.listdir("pics/train/" + thing)
    for bar in x:
        if '.png' in bar:
            os.remove('pics/train/' + thing + '/' + bar)