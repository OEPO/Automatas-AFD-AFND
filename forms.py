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
    
    cantidad1 = IntegerField('Cantidad de estados automata 1', validators = [])
    cantidad2 = IntegerField('Cantidad de estados automata 2', validators = [])
    simbolos1 = StringField('Alfabeto de automata 1', validators = [])
    simbolos2 = StringField('Alfabeto de automata 2', validators = [])
    tipo1 = BooleanField()
    tipo2 = BooleanField()
    
    submit = SubmitField(' Ingresar ')

class Transiciones(FlaskForm):

    origen1 = SelectField('Estado', choices = [(0,'--')])
    input1 = SelectField('Entrada', choices = [(0,'--')])
    destino1 = SelectField('Estado', choices = [(0,'--')])
    final1 = BooleanField()

    origen2 = SelectField('Estado', choices = [(0,'--')])
    input2 = SelectField('Entrada', choices = [(0,'--')])
    destino2 = SelectField('Estado', choices = [(0,'--')])
    final2 = BooleanField()
    
    reset1 = SubmitField('Reiniciar transiciones del Automata 1')
    reset2 = SubmitField('Reiniciar transiciones del Automata 2')
    addtrans1 = SubmitField('Agregar transición')
    addtrans2 = SubmitField('Agregar transición')

class inputString(FlaskForm):

    inputString1 = StringField('Cadena de Entrada', validators = [])
    inputString2 = StringField('Cadena de Entrada', validators = [])

    submit = SubmitField('Ingresar Cadena')

class inputStringUnion(FlaskForm):

    inputString = StringField('Cadena de Entrada', validators = [])

    submit = SubmitField('Ingresar Cadena')