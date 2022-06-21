import sys
from PIL import Image

list_im = [Image.open(x) for x in ['0.jpg', '1.jpg']]

# creates a new empty image, RGB mode, and size 444 by 95
new_im = Image.new('RGB', (2160,1920))

x_offset = 0
for im in list_im:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('test.jpg')