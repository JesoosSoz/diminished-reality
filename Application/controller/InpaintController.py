import sys
sys.path.append("..")

from flask import Blueprint, render_template, session,abort
from services.PixellibSegmentation import PixellibSegmentation


InpaintController1 = Blueprint('InpaintController1 ',__name__, url_prefix="/order")
@InpaintController1.route("/")
def picture():
    """
    Callable by /picture through a GET method
    Retrieves the latest picture with the predictions made by the AI

    Params:

    Returns:
        The latest taken picture with predictions encoeded in base64
    """
    pixellibSegmentation = PixellibSegmentation()
    return str(pixellibSegmentation.Middle())