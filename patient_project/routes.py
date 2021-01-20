import flask
from patient_project import db, app, forms, models
from flask_login import login_user, current_user, logout_user


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('home.html', foundPatient=[])


@app.route("/patients_ID", methods=('GET', 'POST'))
def patients_ID():
    form = forms.PatientIdForm()

    if form.validate_on_submit():

        patient = models.User()  # DB
        if not form.check_user(form.file.data):
            flask.flash("Patient's file'is already token please check your file number", 'warning')
            return flask.render_template('patients_ID.html', patientIdForm=form, num=100000000)
        patient.name = form.name.data
        patient.father = form.father.data
        patient.visa = form.visa.data
        patient.file = form.file.data
        patient.phone = form.phone.data
        patient.age = form.age.data
        patient.gender = form.gender.data
        patient.patient_detail = form.patient_detail.data

        db.session.add(patient)
        db.session.commit()

        flask.flash(f'Patient with file number [ {form.file.data} ] has Added to DB successfully', 'info')
        return flask.redirect(flask.url_for('home'))

    else:
        return flask.render_template('patients_ID.html', patientIdForm=form, num=100000000)


# @app.route('/patients_visit/', defaults={"MD_ID": None}, methods=('GET', 'POST'))
@app.route("/patients_visit/", methods=('GET', 'POST'))
def patients_visit():
    if current_user.is_authenticated:

        form = forms.PatientLastVisitForm()
        user = models.User.query.get(current_user.id)

        if user is not None:
            medicine_box = user.allPatientsVisit
            changed_box = user.allPatientsChangedMedicine
            return flask.render_template('patients_visit.html',
                                         patientVisitForm=form,
                                         medicine_box=medicine_box,
                                         changed_box=changed_box,
                                         id=None, bool_value='False')
    else:
        flask.flash(' ==> Enter your file number first...', 'warning')
        return flask.redirect(flask.url_for('home'))


# TODO I AM CONTROLLING THE ADD & EDIT BY THE ((boolean True and False)) i am using on route (add_medicine) to add and edit
@app.route('/edit_medicine:<id>/', methods=('GET', 'POST'))
def edit_medicine(id):
    form = forms.PatientLastVisitForm()

    user = models.User.query.get(current_user.id)
    medicine_box = user.allPatientsVisit
    changed_box = user.allPatientsChangedMedicine
    results = models.PatientLastVisitDB.query.get(id)

    form.medicine.data = results.medicine
    form.usage.data = results.usage
    form.duration.data = results.duration
    form.dateGiven.data = results.dateGiven
    form.explainReason.data = results.explainReason
    form.disease.data = results.disease
    form.checkedByDr.data = results.checkedByDr
    form.examinations.data = results.examinations

    return flask.render_template('patients_visit.html',
                                 patientVisitForm=form,
                                 textArea_1=results.patientDescription,
                                 medicine_box=medicine_box,
                                 changed_box=changed_box,
                                 bool_value='True', id=id)


# TODO I AM CONTROLLING THE ADD & EDIT BY THE ((boolean True and False)) i am using on route (add_medicine) to add and edit
@app.route('/add_medicine/', defaults={"id": None, "bool_value": 'False'}, methods=('GET', 'POST'))
@app.route('/add_medicine:<id>/<bool_value>', methods=('GET', 'POST'))
def add_medicine(id, bool_value):
    # TODO Check the boo_value if it is 'True' u're editing(updating an old item) if it is 'False' u're adding new item !
    # TODO it was NOT ease to come up with solution on this part it took me 2hrs !
    # TODO  i tried to use modal but it was a bit complicated !

    form = forms.PatientLastVisitForm()
    user = models.User.query.get(current_user.id)
    medicine_box = user.allPatientsVisit

    if form.validate_on_submit():

        if bool_value == 'False':
            userLastVisit = models.PatientLastVisitDB(
                medicine=form.medicine.data,
                usage=form.usage.data,
                duration=form.duration.data,
                dateGiven=form.dateGiven.data,
                explainReason=form.explainReason.data,
                disease=form.disease.data,
                checkedByDr=form.checkedByDr.data,
                examinations=form.examinations.data,
                patientDescription=flask.request.form.get('content'),
                owner_id=user.id
            )

            db.session.add(userLastVisit)
            db.session.commit()

            flask.flash(f'Drug -> [ {form.medicine.data} ] <- has add to Database ...', 'info')
            return flask.redirect(flask.url_for('patients_visit', bool_value='False'))

        else:
            # update the medicine if Dr order for drug change
            find_itemTo_edit = models.PatientLastVisitDB.query.get(id)
            editLastVisit = models.PatientsChangedMedicine(
                oldMedicine=find_itemTo_edit.medicine,
                newMedicine=form.medicine.data,
                newUsage=form.usage.data,
                newDuration=form.duration.data,
                newDateGiven=form.dateGiven.data,
                newCheckedByDr=form.checkedByDr.data,
                newExplainReason=form.explainReason.data,
                newPatientDescription=flask.request.form.get('content'),
                owner_id=user.id
            )

            # TODO change the bool to a false then in the jinja use the "text-decoration-line-through"
            find_itemTo_edit.status = True
            db.session.add(editLastVisit)
            db.session.commit()

            user = models.User.query.get(current_user.id)
            changed_box = user.allPatientsChangedMedicine
            flask.flash(f'Drug -> [ {form.medicine.data} ] <- has been added to new-medicine-database...', 'info')

            return flask.redirect(flask.url_for('patients_visit', changed_box=changed_box))

    else:
        flask.flash('Please fill the fields', 'warning')
        return flask.render_template('patients_visit.html', patientVisitForm=form, num=100000000,
                                     medicine_box=medicine_box,
                                     bool_value='True', id=id)


@app.route('/patient_profile/', defaults={"id": None}, methods=('GET', 'POST'))
@app.route('/patient_profile:<id>/', methods=('GET', 'POST'))
def patient_profile(id):
    # get all Forms
    patientIdForm = forms.PatientIdForm()
    patient_last_visit = forms.PatientLastVisitForm()

    user = models.User.query.get(id) if id is not None else models.User.query.get(current_user.id)
    print(user, 'from <<<< patient_profile')
    # TODO u must let him login b/c we use the current_user.is_authenticated in the base.html
    login_user(user, remember=True)

    patientIdForm.name.data = user.name
    patientIdForm.father.data = user.father
    patientIdForm.visa.data = user.visa
    patientIdForm.file.data = user.file
    patientIdForm.phone.data = user.phone
    patientIdForm.age.data = user.age
    patientIdForm.gender.data = user.gender
    patientIdForm.patient_detail.data = user.patient_detail

    # But you need to get for specific patient
    userRecords = user.allPatientsVisit
    userChangedMD = user.allPatientsChangedMedicine

    # TODO if you fetch from empty DB (>> you need to handle the error <<)
    if len(userRecords) > 0:  # means if user has a records !
        # TODO you can get the user id by saying current_user.id then fetch from DB
        # user old pills
        box1 = []
        box2 = []
        if len(userRecords) > 0:
            for d in userRecords:
                box1.append(d.disease)
                box2.append(d.medicine)

        # user changed pills
        box3 = []
        if len(userChangedMD) > 0:
            for d in userChangedMD:
                if d.newMedicine is not None:
                    box3.append(d.newMedicine)


        patient_last_visit.disease.data = [d for d in box1]
        patient_last_visit.checkedByDr.data = userRecords[-1].checkedByDr
        patient_last_visit.medicine.data = box2 + box3
        patient_last_visit.examinations.data = userRecords[-1].examinations
        # TODO i suppose to have another form her but ...it is better to send the data of the above to the textarea in the jinja other wise it will be not ease

        # user = models.User.query.get(current_user.id)
        medicine_box = user.allPatientsVisit
        changed_box = user.allPatientsChangedMedicine
        print(user, medicine_box, changed_box)
        return flask.render_template('patient_profile.html',
                                     patientIdForm=patientIdForm,
                                     patient_last_visit=patient_last_visit,
                                     medicine_box=medicine_box,
                                     changed_box=changed_box,
                                     textAreaValue_1=user.patient_detail,
                                     textAreaValue_2=userChangedMD[-1].newExplainReason if userChangedMD else
                                     userRecords[-1].patientDescription,
                                     patient_file=None)

    return flask.render_template('patient_profile.html',
                                 patientIdForm=patientIdForm,
                                 patient_last_visit=patient_last_visit,
                                 patient_file=None)


@app.route('/update_patient_profile', methods=('GET', 'POST'))
def update_patient_profile():
    # TODO get all the user data from the FORM
    # TODO this will let you update the user detail

    # get all Forms
    userIdForm = forms.PatientIdForm()

    # get all the data from DB
    userID = models.User.query.get(current_user.id)

    # updating userID DataBase
    userID.name = userIdForm.name.data
    userID.father = userIdForm.father.data
    userID.visa = userIdForm.visa.data
    userID.file = userIdForm.file.data
    userID.phone = userIdForm.phone.data
    userID.age = userIdForm.age.data
    userID.gender = userIdForm.gender.data
    userID.patient_detail = flask.request.form.get('content')

    db.session.commit()

    flask.flash('===> Patient profile has been updated successfully', 'info')
    return flask.redirect(flask.url_for('home'))


@app.route('/delete_medicine:<id>/', methods=('GET', 'POST'))
def delete_medicine(id):
    user = models.User.query.get(current_user.id)
    medicine_box = user.allPatientsVisit

    for item in medicine_box:
        if item.id == int(id):
            db.session.delete(item)
        db.session.commit()
    flask.flash('Medicine has been Deleted....>>>>', 'danger')

    return flask.redirect(flask.url_for('patients_visit'))


@app.route('/find_patient', methods=('GET', 'POST'))
def find_patient():
    patient_file = flask.request.form.get('content')

    patient = models.User.query.filter_by(file=int(patient_file)).first()  # if not will return None
    if patient:
        login_user(patient, remember=True)
        # U can redirect him with his file to the patient_profile
        return flask.redirect(flask.url_for('patient_profile'))
    else:
        flask.flash(f'No Patient with file number of [{patient_file}]', 'danger')
        return flask.redirect(flask.url_for('home'))


@app.route('/logout_patient')
def logout_patient():
    logout_user()
    flask.flash('you have logged out', 'success')
    return flask.redirect(flask.url_for('home'))





@app.route("/all_patients", methods=('GET', 'POST'))
def all_patients():
    allPatients = models.User.query.all()
    flask.flash('No Patients for now', 'success') if len(allPatients) == 0 else allPatients
    return flask.render_template('all_patients.html', allPatients=allPatients)


@app.route('/patient_all_visits')
def patient_all_visits():
    if current_user.is_authenticated:
        user = models.User.query.get(current_user.id)
        allPatientsVisits = user.allPatientsVisit
        allPatientsVisitsEdited = user.allPatientsChangedMedicine  # i need it for the edited visit !

        totalVisits = allPatientsVisits + allPatientsVisitsEdited
        return flask.render_template('patient_all_visits.html', allPatientsVisits=totalVisits)
    flask.flash('Enter patient file first to access to this page.', 'warning')
    return flask.redirect(flask.url_for('home'))



@app.route('/patient_single_visit:<id>/<data>/')
def patient_single_visit(id, data):
    print(id, data)
    if data == 'old':
        old_visit = models.PatientLastVisitDB.query.get(id)
        return flask.render_template('patient_single_visit.html', old_visit=old_visit)
    else:
        new_visit = models.PatientsChangedMedicine.query.get(id)
        return flask.render_template('patient_single_visit.html', new_visit=new_visit)

# TODO you should delete from the changed medicine table......
