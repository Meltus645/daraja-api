from flask import Blueprint
from app.services.daraja_services import init_push, callback
from app.utils.constants import BASEDIR

daraja =Blueprint('daraja', __name__, template_folder= BASEDIR /'templates', static_folder = BASEDIR / 'static')
 
daraja.route('/init_push', methods =['POST'])(init_push)
daraja.route('/callback', methods =['GET','POST'])(callback)