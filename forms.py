from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField, BooleanField

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Form(FlaskForm):
    
    cantidad1 = IntegerField('cantidad1', validators = [] )
    cantidad2 = IntegerField('cantidad1', validators = [] )
    simbolos1 = StringField('alfabeto1', validators = [])
    simbolos2 = StringField('alfabeto2', validators = [])
    tipo1 = BooleanField()
    tipo2 = BooleanField()
    submit = SubmitField(' Ingresar ')

class Transiciones(FlaskForm):

    origen1 = SelectField('origen1', choices = [(0,'--')])
    input1 = SelectField('input1', choices = [(0,'--')])
    destino1 = SelectField('destino1', choices = [(0,'--')])
    final1 = BooleanField()

    origen2 = SelectField('origen1', choices = [(0,'--')])
    input2 = SelectField('input1', choices = [(0,'--')])
    destino2 = SelectField('destino1', choices = [(0,'--')])
    final2 = BooleanField()
    
    submit = SubmitField('Agregar transicion(es)')