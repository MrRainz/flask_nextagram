import os
from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import *
from models.follow import *
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_web.util.google_oauth import oauth

follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')


@follows_blueprint.route('/<user_id>', methods=["GET"])
def new(user_id):
    return render_template('follows/new.html')

@follows_blueprint.route('/<id>/follow_user', methods=["POST"])
@login_required
def follow(id):
    user = User.get_or_none(User.id == id)
    if user.private:
        follow = Follow(following=id, follower=current_user.id)
        follow_message = f"Follow request sent to {user.username}, pending approval."
    else:
        follow = Follow(following=id, follower=current_user.id, approved=True)
        follow_message = f"Followed {user.username}!", "success"
    if follow.save():
        flash(follow_message, "success")
    else:
        flash(f"Error following {user.username}!", "danger")
    return redirect(url_for('users.show', id=id))

@follows_blueprint.route('/<id>/unfollow_user', methods=["POST"])
@login_required
def unfollow(id):
    follow = Follow.get_or_none((Follow.follower_id == current_user.id) & (Follow.following_id == id))
    user = User.get_or_none(User.id == id)
    if follow:
        follow.delete_instance()
        flash(f"Unfollowed {user.username}!", "success")
    else:
        flash(f"Error unfollowing {user.username}!", "danger")
    return redirect(url_for('users.show', id=id))


@follows_blueprint.route("/<user_id>/approve/<follower_id>", methods=["POST"])
@login_required
def approve(user_id, follower_id):
    follow = Follow.select().where((Follow.follower == follower_id) & (Follow.following == current_user.id))
    if follow:
        follow[0].approved = True
        if follow[0].save():
            flash("Request Approved! ", "success")
        else:
            flash("Error approving request.", "danger")
        return redirect(url_for('users.request', id=current_user.id))
    else:
        flash("Sorry, error approving request.", "danger")
        return redirect(url_for('users.profile', id=user_id))


@follows_blueprint.route("/<user_id>/delete/<follower_id>", methods=["POST"])
@login_required
def delete(user_id, follower_id):
    follow = Follow.get_or_none((Follow.follower_id == follower_id) & (Follow.following_id == user_id))
    user = User.get_or_none(User.id == user_id)
    if follow:
        follow.delete_instance()
        flash("Follow request removed!", "success")
    else:
        flash(f"Error removing follow request!", "danger")
    return redirect(url_for('users.request', id=user_id))