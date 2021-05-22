from zlib import DEF_BUF_SIZE
from flask import Flask, render_template,request
from flask.helpers import send_file
from certi import compress,generate_certis
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
cloudinary.config( 
  cloud_name = "codemafia", 
  api_key = "126772947881962", 
  api_secret = "aBU9n2w7UKS1f28wsqg1CNEih8s" 
)

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/step1')
def step1():
   return render_template('step1.html')

@app.route('/step2')
def step2():
   return render_template('step2.html')

@app.route('/step3')
def step3():
   return render_template('step3.html')

@app.route('/step4')
def step4():
   return render_template('step4.html')

@app.route('/get-file')
def get_file():
   return send_file('Certis.zip', attachment_filename='Certis.zip')

@app.route('/get-template')
def get_template():
   return send_file('template.csv', attachment_filename='template.csv',mimetype='text/csv', as_attachment=True)

@app.route('/get-certificate-template')
def get_certi_template():
   return send_file('certificate_template.jpg', attachment_filename='certificate.jpg',mimetype='image/jpg', as_attachment=True)

@app.route('/deleteResources',methods=["POST"])
def test_cloudinary():
   image_public_id = request.form['image_pub_id']
   sheet_public_id = request.form['sheet_pub_id']
   font_public_id = request.form['font_pub_id']
   if image_public_id != "":
      print(cloudinary.uploader.destroy(image_public_id,resource_type='image'))
   if sheet_public_id != "":
      print(cloudinary.uploader.destroy(sheet_public_id,resource_type='raw'))
   if font_public_id != "":
      print(cloudinary.uploader.destroy(font_public_id,resource_type='raw'))
   return {
      "success":"ok",
   }

@app.route('/generateCerti',methods=["POST"])
def generate_certi():
   image_url = request.form['image_url']
   font_url = request.form['font_url']
   sheet_url = request.form['sheet_url']
   coords = json.loads(request.form['coords'])
   print(image_url,font_url,sheet_url,coords)
   data = {
      "image_url":image_url,
      "font_url":font_url,
      "sheet_url":sheet_url,
      "coords":coords
   }
   file_names = generate_certis(data)
   compress(file_names)
   return {
      "success":"ok"
   }

if __name__ == '__main__':
   app.run()