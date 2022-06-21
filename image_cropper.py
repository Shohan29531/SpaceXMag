from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -30)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

im = Image.open("11.jpg")
im = trim(im)
im.show()
im.save('11_cropped.jpg')


