from flask import Flask
from wq_service import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Video Thumbnailer!!"


# submit jobs to the queue
@app.route('/convert')
def convert():
    run_task('extract', ['../../test3.mp4'])
    return "Hello Video Thumbnailer!!"


# submit jobs to the queue
# @app.route('/convert')
# def index():
#     return "Hello Video Thumbnailer!!"


# app.run(host='0.0.0.0',port=5000, debug=True)
if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
