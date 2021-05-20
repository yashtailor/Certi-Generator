import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.utils import make_msgid
from email.mime.multipart import MIMEMultipart  # New line
from email.mime.base import MIMEBase  # New line
from email import encoders  # New line
import csv
import numpy as np
import pandas as pd
import cv2
import io
from io import StringIO,BytesIO
from PIL import ImageFont, ImageDraw, Image, ImageQt
from urllib.request import urlopen
import zlib
import zipfile
# User configuration
sender_email = 'conveners2021@technovanza.org'
sender_name = 'Technovanza Conveners, 2021'
# password = input('Please, type your password: ')

x1 = 804
y1 = 884
x2 = 780 
y2 = 948
x3 = 420
y3 = 1015
x4 = 344
y4 = 1076

receiver_emails = []
receiver_names = []
receiver_positions = []
receiver_types = []
# receiver_desigs = []
url_csv = "https://res.cloudinary.com/codemafia/raw/upload/v1621526877/CertiSheets/fmyuw0wpfpje9bcwkepn.csv"
response = urlopen(url_csv)
lines = [l.decode('utf-8') for l in response.readlines()]
csv_reader = csv.reader(lines)

def compress(file_names):
    print("File Paths:")
    print(file_names)

    path = "C:/data/"

    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile("Certis.zip", mode="w")
    count = 0
    try:
        for file_name in file_names:
            # Add file to the zip file
            # first parameter file to zip, second filename in zip
            if count == 0:
                count += 1
                continue
            print('COA - '+file_name+'.pdf')
            zf.write('COA - '+file_name+'.pdf', 'COA - '+file_name+'.pdf', compress_type=compression)

    except FileNotFoundError:
        print("An error occurred")
    finally:
        # Don't forget to close the file!
        zf.close()

for data in csv_reader:
        # names = []
        receiver_names.append(data[0])
        receiver_positions.append(data[1])
        receiver_types.append(data[2])
        # receiver_emails.append(data[1])
        # receiver_positions.append(data[3])
        # names.append(data[3])
        # names.append(data[3])
        # names.append(data[4])
        # partners_names = data[2].split(',')
        # for pname in partners_names:
        #         names.append(pname)
        # receiver_names.append(names)
        # receiver_desigs.append(data[1])
        # pos = data[3]
        # if pos[:2]=='DC':
        #         receiver_positions.append('Department Coordinator')
        # else:
        #         receiver_positions.append('Techno Manager')
print(receiver_names,receiver_positions,receiver_types)


filename = 'text.txt'

font_url = "https://res.cloudinary.com/codemafia/raw/upload/v1621526250/FontFiles/bpjcwpabqtzk8s915yo8.ttf"

# fd = urllib.urlopen(font_url)
# image_font = io.BytesIO(fd.read())

for receiver_name, receiver_position,receiver_type  in zip(receiver_names, receiver_positions,receiver_types):
        if receiver_name=='Name':
                continue
        if len(receiver_name)==0:
                continue
        print("Sending the email...",receiver_name)
        # Configurating user's info
        # img = cv2.imread('COA_VJTI_Senate.png')
        # pil_im = Image.fromarray(img)  
        pil_im = Image.open(urlopen("https://res.cloudinary.com/codemafia/image/upload/v1621529612/Templates/usscpnihffrnwllncydb.png"))
        draw = ImageDraw.Draw(pil_im)  
        # use a truetype font  
        font = ImageFont.truetype(urlopen(font_url), 45)  
        # font2 = ImageFont.truetype("JosefinSans-SemiBold.ttf", 80)  
        #x = 1416 y = 1296 x = 1424 y = 1292
        #x = 1780 y = 1432
        # Draw the text  
        draw.text((x1,y1), receiver_name, font=font,fill=(0,0,0),thickness=3)  
        draw.text((x2,y2), receiver_position, font=font,fill=(0,0,0),thickness=3)  
        draw.text((x3,y3), '2019-20', font=font,fill=(0,0,0),thickness=3)  
        draw.text((x4,y4), receiver_type, font=font,fill=(0,0,0),thickness=3)  
        # draw.text((1588,1420), 'Marketing Executive', font=font2,fill=(0,0,0))
        # Get back the image to OpenCV  
        # cv2_im_processed = np.array(pil_im)
        # font = cv2.FONT_HERSHEY_SIMPLEX 
        # ft = cv2.freetype.createFreeType2()
        # ft.loadFontData(fontFileName='JosefinSans-Bold.ttf',
        #         id=0)
        # org 
        org = (1404,1368)
        print(org) 
                        
        # fontScale 
        fontScale = 3
                        
        # Blue color in BGR 
        color = (0, 0, 0) 
                        
        # Line thickness of 2 px 
        thickness = 3
                        
        # Using cv2.putText() method 
        # image2 = cv2.putText(img, receiver_name, org, ft,  
        #                         fontScale, color, thickness, cv2.LINE_AA) 

        # Certi_img = Image.fromarray(cv2_im_processed, 'RGB')
        # filename = 'COA - '+receiver_name+'.pdf'
        pil_im.convert('RGBA')
        pil_im.save('COA - '+receiver_name+'.pdf')
        # cv2.imwrite(filename,cv2_im_processed)

        '''       
        msg = MIMEMultipart()
        msg['To'] = formataddr((receiver_name, receiver_email))
        msg['From'] = formataddr((sender_name, sender_email))
        msg['Subject'] = 'Certificate of Appreciation : Technovanza 2020-2021'
        msg['X-Priority'] = '1'
        body = "Thank you for being the face of Technovanza in your college.We thank you for your efforts and making Technovanza once again successful this year despite the pandemic.We hereby attach the certificate of the same.\n\nRegards,\nTeam Technovanza(2020-21),\nVJTI Mumbai"
        part1 = MIMEText(body, "plain")
        msg.attach(part1)
        # msg.attach(MIMEText(email_body, 'html'))
        if len(receiver_name)==0:
                continue
        try:
                # Open PDF file in binary mode
                with open('CA_'+receiver_name+'.png', "rb") as attachment:
                                part = MIMEBase("application", "octet-stream")
                                part.set_payload(attachment.read())

                # Encode file in ASCII characters to send by email
                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {'COA_'+receiver_name+'.png'}",
                )

                msg.attach(part)
        except Exception as e:
                print(f"Oh no! We didn't found the attachment!n{e}")
                break

        try:
                # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
                server = smtplib.SMTP('smtp.gmail.com', 587)
                # Encrypts the email
                context = ssl.create_default_context()
                server.starttls(context=context)
                # We log in into our Google account
                server.login(sender_email, password)
                # Sending email from sender, to receiver with the email body
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print('Email sent!')
        except Exception as e:
                print(f'Oh no! Something bad happened!n{e}')
                break
        finally:
                print('Closing the server...')
                server.quit() '''



'''
Vedika Sankpal,Convener,vedikasankpal16@gmail.com
Chinmay Desai,Convener,chinmaycm1@gmail.com
Shrenil Chovatiya,Convener,chovatiyashrenil@gmail.com
Abhinav Ven,Convener,abhinavven@gmail.com
'''

compress(receiver_names)
