from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PokeSearch(FlaskForm):
    search = StringField('Choose Your Pokemon! (Any Pokemon looked up will be added to your party until you have 6.)', validators=[DataRequired()])
    submit = SubmitField('Choose Your Pokemon!')