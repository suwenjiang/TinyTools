#coding:gbk
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, sys
import tempfile
import shutil

def resize_image(img):
    basewidth=800

    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    print hsize
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    # img.save('d:\\watermark.png')
    return img
FONT = 'Arial.ttf'
def add_watermark(in_file, text, angle=23, opacity=0.25):
    img = Image.open(in_file).convert('RGB')
    if img.size[0]>800:
        img=resize_image(img)
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 1
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)
    while n_width+n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 4,
              (watermark.size[1] - n_height) / 4),
              text, font=n_font,fill=(255,0,0,255))
    watermark = watermark.rotate(angle,Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    out_file=os.path.join(tempfile.mkdtemp(),os.path.split(in_file)[1])
    Image.composite(watermark, img, watermark).save(out_file, 'png')
    #remove the file
    shutil.move(out_file,in_file)

def get_imag_file_in_folder(path):
    image_format=[".png",'.jpg']
    list_imge=[]
    for root,dirname, files in os.walk(path):
         for file in files:

             if os.path.splitext(file)[1] in image_format:
                image_file=os.path.join(root,file)
                list_imge.append(image_file)
         return list_imge


if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     sys.exit('Usage: %s <input-image> <text> <output-image> ' \
    #              '<angle> <opacity> ' % os.path.basename(sys.argv[0]))
    imsglist=get_imag_file_in_folder('D:\Gallery\gallery\BathPublishService')
    for i in imsglist:
     add_watermark(i,'swj.me')