from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SearchForm(FlaskForm):
    text = StringField('text',
                            validators= [DataRequired()])
    submit = SubmitField('Check')

class TrainForm(FlaskForm):
    submit = SubmitField('Train')