from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField


class Form(FlaskForm):
    name = StringField('name')
    descr = StringField('descr')
    company = StringField('company')
    category = StringField('category')
    salary = FloatField('salary')
    submit_button = SubmitField('Submit')

