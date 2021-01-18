from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import *
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import boto3, botocore
import os

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ['AWS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET']
)

@images_blueprint.route('/<id>/new', methods=['GET'])
@login_required
def new(id):
    user = User.get_by_id(id)
    if current_user.id != int(id):
        return redirect(url_for('images.new', id=current_user.id))
    else:
        user = User.get_or_none(User.id == id)
        if user:
            return render_template('images/image.html', user=user)
        else:
            return redirect(url_for('images.new', id=current_user.id))


@images_blueprint.route('/<id>/new', methods=["POST"])
def create(id):
    try:
        file = request.files["my_file"]
        s3.upload_fileobj(
            file,
            os.environ["BUCKET_NAME"],
            "images/" + file.filename,
            ExtraArgs = {
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        flash("Successfully uploaded") 
        bucket_name = os.environ["BUCKET_NAME"]
        region = os.environ["REGION"]
        platform = os.environ["PLATFORM"]
        url = f"https://{bucket_name}.{region}.{platform}/images/{file.filename}"
        user = User.get_by_id(id)
        image = Image(user_id=user.id, image_url=url)
        if image.save():
            flash("Picture saved.")
        else:
            flash("Picture not saved.")
        return redirect(url_for("users.profile", id=current_user.id))
    except:
        flash("Upload failed. Did you select a file?")
        return redirect(url_for("images.new", id=current_user.id))