from flask import Blueprint

cont = Blueprint("cont", __name__)

from . import views
from ..main import errors
