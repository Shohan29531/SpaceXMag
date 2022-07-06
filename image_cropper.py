from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -30)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

im = Image.open("image_segments/8.jpg")
im = trim(im)
im.show()
im.save('image_segments/8_cropped.jpg')


