import braintree
import os
from decimal import Decimal
from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required
from models.user import *
from models.image import *
from models.donation import *
from app import login_manager


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ["MERCHANT_ID"],
        public_key=os.environ["PUBLIC_KEY"],
        private_key=os.environ["PRIVATE_KEY"]
    )
)

donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

@donations_blueprint.route('/<image_id>/new', methods=["GET"])
@login_required
def new(image_id):
    token = gateway.client_token.generate()
    return render_template('donations/new.html', token=token, image_id=image_id)

@donations_blueprint.route('/<image_id>', methods=["POST"])
@login_required
def create(image_id):
    nonce = request.form["nonce"]
    amount = request.form["amount"]
    image = Image.get_by_id(image_id)
    result = gateway.transaction.sale({
        "amount": str(amount),
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        image = Image.get_by_id(image_id)
        donation = Donation(image=image, amount=Decimal(amount))
        if donation.save():
            flash("Donation recorded! ", "success")
        else:
            flash("Donation not recorded! ", "danger")
        flash("Payment received! ", "success")
        return redirect(url_for("home"))
    else:
        flash("Payment failed! ", "danger")
        return redirect(url_for("home"))
