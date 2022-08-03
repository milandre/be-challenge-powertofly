from flask import Blueprint, redirect

# App blueprint init
main = Blueprint('main', __name__)


@main.route('/')
def index():
    # Redirect to API documentation
    return redirect("/docs", code=302)
