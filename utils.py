from flask import flash

def flash_message(message, category='info'):
    flash(message, category)
