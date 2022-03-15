from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from moviesite.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username ',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),Email("this fied required valid email id")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    

     


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Login')


class movie(FlaskForm):
    movie_title = StringField('Movie Title', validators=[DataRequired()])
    movie_desc = TextAreaField('Context', validators=[DataRequired()])
    image_file = FileField('Movie Poster', validators=[FileAllowed(['jpg', 'png'])])
    movie_link = StringField('Movie Id Link for download and stream')
    submit = SubmitField('submit')
    action = BooleanField('action')
    suspense = BooleanField('suspense')
    adventure = BooleanField('adventure')
    horror = BooleanField('horror')
    comedy = BooleanField('comedy')
    scifci = BooleanField('scifci')
    release_date = StringField('release date')

    
class search_field(FlaskForm):
    search_movie = StringField('serch movie by name')
    category = SelectField(u'category', choices=[('action', 'action'), ('suspense', 'suspense'), ('adventure', 'adventure'),('horror','horror'),('comedy','comedy'),('scifci','scifci')])
    search = SubmitField('search')

    

   