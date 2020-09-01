import os
import secrets
from datetime import date
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    today = date.today()
    thea = today.strftime("%b-%d-%Y")
    picture_fn = random_hex + '-SALT-' + str(thea) + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def delete_picture(old_image):
	old_image_path = os.path.join(current_app.root_path, 'static/profile_pics', old_image)

	if os.path.exists(old_image_path):
	    print('Deleting old picture:' + old_image_path)
	    os.remove(old_image_path)

def send_reset_email(user):
    token = user.get_reset_token()
    print(token)
    msg = Message('Passwlord Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)
