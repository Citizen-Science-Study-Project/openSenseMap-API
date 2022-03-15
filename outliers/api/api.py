import glob

import flask
from PIL import Image
from flask import request


def create_gif(id):
    try:
        # Create the frames
        frames = []
        imgs_list = glob.glob(f'gif/png_{id}/*.png')
        for i in imgs_list:
            new_frame = Image.open(i)
            frames.append(new_frame)

        # Save into a GIF file that loops forever
        frames[0].save(f'gif/png_{id}/png_to_gif.gif', format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=300, loop=0)
        return True

    except Exception:
        return False


app = flask.Flask(__name__)
app.config["DEBUG"] = True


# http://127.0.0.1:5000/?id=abc
@app.route('/', methods=['GET'])
def gif():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    if create_gif(id):
        return "GIF created"
    else:
        return "Error: Creating GIF"


app.run()
