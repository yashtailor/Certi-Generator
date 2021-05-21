import csv
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from urllib.request import urlopen
import zipfile
import os
import numpy as np

def compress(file_names):
    print("File Paths:")
    print(file_names)

    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile("Certis.zip", mode="w")
    try:
        for file_name in file_names:
            # Add file to the zip file
            # first parameter file to zip, second filename in zip
            print(file_name)
            zf.write(file_name, file_name, compress_type=compression)

    except FileNotFoundError:
        print("An error occurred")
    finally:
        # Don't forget to close the file!
        zf.close()

def generate_certis(data):
        files = os.listdir()
        flag = False
        for file in files:
            if file == "Certis.zip":
                flag = True
        if flag:
            os.remove('Certis.zip')
        url_img = data['image_url']
        url_font = data['font_url']
        url_sheet = data['sheet_url']
        coords = data['coords']
        print(coords)
        response = urlopen(url_sheet)
        lines = [l.decode('utf-8') for l in response.readlines()]
        csv_reader = csv.reader(lines)
        file_names = []
        count = 0
        for row in csv_reader:
            print("currently working with row:",row)
            if count==0:
                count += 1
                continue
            img = Image.open(urlopen(url_img)).convert('RGBA')
            x = np.array(img)
            r, g, b, a = np.rollaxis(x, axis = -1)
            r[a == 0] = 255
            g[a == 0] = 255
            b[a == 0] = 255
            x = np.dstack([r, g, b, a])
            img = Image.fromarray(x, 'RGBA')
            draw = ImageDraw.Draw(img)  
            for i in range(len(coords)):
                size = int(float(coords[i][2][:-2]))
                x = int(float(coords[i][0][:-2]))
                y = int(float(coords[i][1][:-2]))
                font = ImageFont.truetype(urlopen(url_font), size)  
                draw.text((x,y),row[i], font=font,fill=(0,0,0))  
            img = img.convert("RGB")
            img.save('COA - '+row[0]+'.pdf')
            file_names.append('COA - '+row[0]+'.pdf')
        return file_names


# ANOTHER WAY BUT HAD ISSUES WITH SAVING IMAGE IN RGBA
#     pil_im = Image.open(urlopen(url_img))
#     draw = ImageDraw.Draw(pil_im)  
#     for i in range(len(coords)):
#         size = int(float(coords[i][2][:-2]))
#         x = int(float(coords[i][0][:-2]))
#         y = int(float(coords[i][1][:-2]))
#         font = ImageFont.truetype(urlopen(url_font), size)  
#         draw.text((x,y),row[i], font=font,fill=(0,0,0))  
#     background = Image.new("RGB", pil_im.size, (255, 255, 255))
#     background.paste(pil_im, mask=pil_im.split()[3]) # 3 is the alpha channel