from flask import Flask
from worker import wq_service

app = Flask(__name__)


@app.route('/')
def index():
    # return "Hello Video Thumbnailer!!"
    return 'f'


# submit jobs to the queue
@app.route('/convert', methods=['GET'])
def convert():
    wq_service.add_to_eq("./test3.mp4")
    return 'wtf'


@app.route('/convert-bucket', methods=['GET'])
def convert_all():
    return "Converting all videos inside the bucket"


@app.route('/list-gif')
def list_gif():
    return wq_service.list_gif()


@app.route('/track')
def track():
    return


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
