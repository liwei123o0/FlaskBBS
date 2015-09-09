from flask.ext.wtf import Form
from wtforms import SubmitField,StringField
from wtforms.validators import Required

class PostForm(Form):
    body = StringField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
