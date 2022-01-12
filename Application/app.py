from flask import Flask
from controller.InpaintController import InpaintController1

app = Flask(__name__)
app.register_blueprint(InpaintController1)

#Decorating our function with app.route method
@app.route('/')
def hello_world():
    return "Hello, This is home page."

#Running our Flask application using app.run method
if __name__ == '__main__':
   app.run()