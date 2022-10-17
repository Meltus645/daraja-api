from flask import Blueprint
from app.controllers.public_controller import home

public =Blueprint('public', __name__)
public.route('')(home)