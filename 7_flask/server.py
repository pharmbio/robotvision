from flask import Flask, Response, render_template
from camera import Webcam

# Flask livefeed using Motion JPEG 

server = Flask(__name__)
print("hello")


@server.route('/')
def index():
    return render_template('index.html')

def generate(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@server.route('/video_feed')
def video_feed():
    return Response(generate(Webcam()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    server.run(debug=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# # def gen(camera):
# #     while(camera.isOpened()):
# #         (ret, frame) = camera.read()
# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/feed')
# def feed():
#     return Response("hello", mimetype='multipart/x-mixed-replace; boundary=frame')


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)
