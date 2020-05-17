from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class AutomataForm(FlaskForm):

    estados = StringField('estados',
                        validators=[DataRequired()])

    simbolos = StringField('simbolos',
                        validators=[DataRequired()])

    transiciones = StringField('transiciones',
                        validators=[DataRequired()])

    final = StringField('finales',
                        validators=[DataRequired()])
    
    submit = SubmitField('enviar')

