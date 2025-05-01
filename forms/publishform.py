from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField


class PublishForm(FlaskForm):
    title = StringField()
    content = StringField()
    con = TextAreaField()
    file = FileField()
    submit = SubmitField()
