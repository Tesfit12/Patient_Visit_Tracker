import flask
import flask_wtf
import wtforms
from wtforms import validators as valid, ValidationError
from patient_project.models import User


class PatientIdForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Name', validators=[valid.DataRequired(message='Name can not be empty !')])
    father = wtforms.StringField('Father', validators=[valid.DataRequired(message='Father can not be empty !')])
    visa = wtforms.StringField('Visa', validators=[valid.DataRequired(message='Visa can not be empty !')])
    file = wtforms.IntegerField('File', validators=[valid.DataRequired(message='file can not be empty !')])
    phone = wtforms.IntegerField('Phone', validators=[valid.DataRequired(message='Phone can not be empty !')])
    age = wtforms.IntegerField('Age', validators=[valid.DataRequired(message='please fill this !')])
    gender = wtforms.StringField('Gender', validators=[valid.DataRequired(message='please fill this !')])
    patient_detail = wtforms.StringField('patient_detail')
    submit = wtforms.SubmitField("Submit")

    # not sure if it is going to work

    def check_user(self, file):
        patient_name = User.query.filter_by(file=file).first()
        if patient_name:
            return False
        return True


class PatientLastVisitForm(flask_wtf.FlaskForm):
    medicine = wtforms.StringField('Drug-given/Changed',
                                   validators=[valid.DataRequired(message='Drug-name can not be empty !')])
    usage = wtforms.StringField('How-to-take', validators=[valid.DataRequired(message='usage can not be empty !')])
    duration = wtforms.StringField('Duration', validators=[valid.DataRequired(message='Duration can not be empty !')])
    dateGiven = wtforms.StringField('Date-Given', validators=[valid.DataRequired(message="field can't be empty")])

    disease = wtforms.StringField('Disease', validators=[valid.DataRequired(message="field can't be empty")])
    checkedByDr = wtforms.StringField('checked-by-Dr.', validators=[valid.DataRequired(message="field can't be empty")])
    examinations = wtforms.StringField('Examinations', validators=[valid.DataRequired(message="field can't be empty")])
    patientDescription = wtforms.StringField('Patient-Description')

    explainReason = wtforms.StringField('Explain-Reason')
    medicine_cart = []
    submit = wtforms.SubmitField("ADD")
