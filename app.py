from flask import Flask, render_template,request
from flask.wrappers import Request
app = Flask(__name__)

@app.route('/')
def home():
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

@app.route('/generateCerti',methods=["POST"])
def generate_certi():
    image_url = request.form['image_url']
    font_url = request.form['font_url']
    sheet_url = request.form['sheet_url']
    print(image_url,font_url,sheet_url)
    return {
        "success":"ok"
    }

if __name__ == '__main__':
   app.run()