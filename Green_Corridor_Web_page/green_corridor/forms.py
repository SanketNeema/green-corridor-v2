from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from green_corridor import db  


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class NewDriver(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    mobile_no=StringField('Mobile No',
                        validators=[DataRequired(), Length(10)])

    assign_password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('assign_password')])
    submit = SubmitField('Create Driver')   

    def validate_username(self, email):
        user = db.collection('driver').document(email.data).get().to_dict()
        print(user)
        if user: 
            raise ValidationError('That email is taken. Please choose a different one.')

class PlaceCordinate(FlaskForm):
    source = StringField('Source',
                           validators=[DataRequired()])
    destination = StringField('Destination',
                           validators=[DataRequired()])
    submit = SubmitField('CREATE GREEN CORRIDOR')

# ref = db.reference('dinosaurs')
# snapshot = ref.order_by_child('height').limit_to_first(2).get()
# for key in snapshot:
#     print(key)

#db.collection('driver').document(email=email.data).get().exists