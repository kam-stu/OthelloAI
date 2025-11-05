from flask import Blueprint

othello_bp = Blueprint("othello", __name__)

from .update import *
from .ai import *
