from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request
from Automata_Form import AutomataForm
from flask_sqlalchemy import SQLAlchemy
from config import Config
WTF_CSRF_SECRET_KEY = 'a random string'

app = Flask(__name__)
app.config.from_object(Config)
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class automata_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estados = db.Column(db.String(100), unique=True, nullable=False)
    simbolos = db.Column(db.String(100), unique=True, nullable=False)
    transiciones = db.Column(db.String(100), unique=True, nullable=False)
    finales = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"automata_db('{self.estados}', '{self.simbolos}', '{self.transiciones}, '{self.finales} ')"




# Routes to Render Something
@app.route("/", methods=['GET', 'POST'])
def home():
    form = AutomataForm()
    if form.validate_on_submit():
        print(form.estados.data)
        return redirect(url_for('home'))
    else:
        print('unsuccess')
    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
