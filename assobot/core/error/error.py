import requests
from werkzeug.exceptions import HTTPException
from flask import *

from assobot import APP

@APP.errorhandler(HTTPException)
def generic_handle_HTTP_Exception(e):
    titre =f'{e.code} {e.name}'
    if (e.code > 400 and e.code < 500):
        if (e.code == 403 ) :
            message='Oups... permission requise'
        else :
            message='Oups... Il semblerait que vous vous êtes perdu'
        return render_template('default/error/error.html', titre=titre, message=message, error=True), e.code
    else:
        message='Oups... Une erreur est survenue. Veillez réessayer plus tard'
        return render_template('default/error/error.html', titre=titre, message=message, error=True), e.code