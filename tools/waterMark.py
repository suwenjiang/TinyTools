from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, sys
 
FONT = 'Arial.ttf'
 
def add_watermark(in_file, text, out_file='d:\\watermark.jpg', angle=23, opacity=0.25):
    img = Image.open(in_file).convert('RGB')
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 2
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)
    while n_width+n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 2),
              text, font=n_font,fill=(255,0,0,255))
    watermark = watermark.rotate(angle,Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
 
if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     sys.exit('Usage: %s <input-image> <text> <output-image> ' \
    #              '<angle> <opacity> ' % os.path.basename(sys.argv[0]))
    add_watermark(r'd:\Gallery\gallery\2015-07-09_1504.png','swj.me')