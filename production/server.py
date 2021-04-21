from flask import Flask, Response, render_template
from realsense import Livefeed 
from scanner import Barcode

server = Flask(__name__)
print("hello")

@server.route('/')
def index():
    return render_template('index.html')

# Flask livefeed using Motion JPEG 
def generate(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@server.route('/livefeed')
def livefeed():
    return Response(generate(Livefeed()), mimetype='multipart/x-mixed-replace; boundary=frame')

# Read most central barcode and return value
@server.route('/read_barcode')
def read_barcode():
    return Response(ReadBarcode())

if __name__ == "__main__":
    server.run(debug=True)
