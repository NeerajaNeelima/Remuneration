from app import db

class SubjectInformation(db.Model):
    __tablename__ = 'Subject_information'
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(255))
    subject_name = db.Column(db.String(255))

class FacultyInformation(db.Model):
    __tablename__ = 'Faculty_information'
    id = db.Column(db.Integer, primary_key=True)
    pan_no = db.Column(db.String(255),index=True)
    Names = db.Column(db.String(255))
    bank_account = db.Column(db.Integer)
    ifsc_code = db.Column(db.String(255))

class ExaminationBills(db.Model):
    __tablename__ = 'Examination_bills'
    examination_id = db.Column(db.Integer, primary_key=True)
    pan_no = db.Column(db.String(255), db.ForeignKey('Faculty_information.pan_no'))
    name_of_the_staff = db.Column(db.String(255))
    bank_account_no = db.Column(db.Integer)
    ifsc_code = db.Column(db.String(255))
    transaction_type = db.Column(db.String(255))
    no_of_scripts = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    grand_total = db.Column(db.Float) 