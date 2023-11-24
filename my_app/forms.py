from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DecimalField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email, EqualTo, Length
import decimal

class ProductForm(FlaskForm):
    title = StringField(validators = [DataRequired()])
    description = StringField(validators = [DataRequired()])
    photo_file = FileField()
    price = DecimalField(
        places = 2, 
        rounding = decimal.ROUND_HALF_UP, 
        validators = [DataRequired(), NumberRange(min = 0)])
    category_id = SelectField(validators = [InputRequired()])
    submit = SubmitField()


class DeleteForm(FlaskForm):
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField(validators = [Email(), DataRequired()])
    password = PasswordField(validators=[ DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')