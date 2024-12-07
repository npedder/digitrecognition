import os
from PIL import Image

folder_images = "SVHNLite/test"
size_images = dict()


maxWidth = 0
maxHeight = 0
minWidth = 1000
minHeight = 10000

for dirpath, _, filenames in os.walk(folder_images):
    for path_image in filenames:
        image = os.path.abspath(os.path.join(dirpath, path_image))
        with Image.open(image) as img:
            width, height = img.size
            size_images[path_image] = {'width': width, 'height': height}
            if width > maxWidth:
                maxWidth = width
            if height > maxHeight:
                maxHeight = height
            if height < minWidth:
                minHeight = height
            if width < minWidth:
                minWidth = width
                smallestImage = image
print("Max height: ", maxHeight)
print("Max width: ", maxWidth)

print("Min height: ", minHeight)
print("Min width: ", minWidth)
print(smallestImage)
#print(size_images, flush=True)