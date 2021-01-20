from patient_project import db, app, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



class User(db.Model, UserMixin):
    id          = db.Column(db.Integer(), primary_key=True)
    name        = db.Column(db.String)
    father      = db.Column(db.String)
    visa        = db.Column(db.Integer)
    file        = db.Column(db.Integer)
    phone       = db.Column(db.Integer)
    age         = db.Column(db.Integer)
    gender       = db.Column(db.Integer)
    patient_detail       = db.Column(db.Integer)
    allPatientsVisit = db.relationship('PatientLastVisitDB', backref='owner')
    allPatientsChangedMedicine = db.relationship('PatientsChangedMedicine', backref='owner')




class PatientLastVisitDB(db.Model):
    id          = db.Column(db.Integer(), primary_key=True)
    medicine    = db.Column(db.String)
    usage       = db.Column(db.String)
    duration    = db.Column(db.String)
    dateGiven   = db.Column(db.String)
    explainReason = db.Column(db.String)
    disease = db.Column(db.String)
    checkedByDr = db.Column(db.String)
    examinations = db.Column(db.String)
    patientDescription = db.Column(db.String)
    status = db.Column(db.Boolean(), default=False)
    owner_id    = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, owner_id, medicine, usage, duration, dateGiven, explainReason, disease, checkedByDr, examinations, patientDescription):
        self.medicine = medicine
        self.usage = usage
        self.duration = duration
        self.dateGiven = dateGiven
        self.explainReason = explainReason
        self.disease = disease
        self.checkedByDr = checkedByDr
        self.examinations = examinations
        self.patientDescription = patientDescription
        self.owner_id = owner_id




class PatientsChangedMedicine(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    oldMedicine = db.Column(db.String)
    newMedicine = db.Column(db.String)
    newUsage = db.Column(db.String)
    newDuration = db.Column(db.String)
    newDateGiven = db.Column(db.String)
    newCheckedByDr = db.Column(db.String)
    newExplainReason = db.Column(db.String)
    newPatientDescription = db.Column(db.String)
    owner_id    = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, newMedicine, newUsage,newDuration, newDateGiven, newCheckedByDr, newExplainReason, newPatientDescription, owner_id, oldMedicine):
        self.oldMedicine = oldMedicine
        self.newMedicine = newMedicine
        self.newUsage = newUsage
        self.newDateGiven,  = newDateGiven,
        self.newDuration = newDuration
        self.newCheckedByDr = newCheckedByDr
        self.newExplainReason = newExplainReason
        self.newPatientDescription = newPatientDescription
        self.owner_id = owner_id


# class UserMedicalInfo(db.Model):
#     id              = db.Column(db.Integer, primary_key=True)
#     disease         = db.Column(db.String)
#     checkedByDr     = db.Column(db.String)
#     drugGiven       = db.Column(db.String)
#     examinations    = db.Column(db.String)
#     patientDescription = db.Column(db.String)
#     owner_id        = db.Column(db.Integer, db.ForeignKey('user.id'))
#
