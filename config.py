import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' 
    
    #  Flask y algunas de sus extensiones utilizan el valor de la clave secreta como clave criptográfica, útil para generar firmas o tokens. La extensión Flask-WTF lo utiliza para proteger los formularios web contra un ataque llamado Cross-Site Request Forgery o CSRF
