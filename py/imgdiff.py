from PIL import Image
from PIL import ImageChops
img1 = Image.open("./imgs/white.png")
img2 = Image.open("./imgs/black.png")
# make sure img1,img2 have the same picture width and height.
diff = ImageChops.difference(img1, img2)
diff_alpha = diff.convert("RGBA")
diff_pxls = diff_alpha.load()

for y in range(diff.height):
    for x in range(diff.width):
        r, g, b, a = diff_pxls[y, x]
        avg = (r + g + b) // 3
        diff_pxls[y, x] = (r, g, b, 255 - avg)

diff.save('./imgs/shadow.png')
diff_alpha.save('./imgs/shawdow_alpha.png')
