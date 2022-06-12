from flask import Flask
# from worker import wq_service

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Video Thumbnailer!!"


# # submit jobs to the queue
# @app.route('/convert')
# def convert():
#     return wq_service.add_to_q("./test3.mp4")
#
#
# @app.route('/convert-bucket')
# def convert_all():
#     return "Converting all videos inside the bucket"
#
#
# @app.route('/list-gif')
# def list_gif():
#     return wq_service.list_gif()
#
#
# @app.route('/track')
# def track():
#     return


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
    while 1:
        print('f')
