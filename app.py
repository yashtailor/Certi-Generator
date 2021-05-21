from zlib import DEF_BUF_SIZE
from flask import Flask, render_template,request,send_from_directory
from flask.helpers import send_file
from flask.wrappers import Request
from certi import compress,generate_certis
from io import BytesIO
import zipfile
import json
import time
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