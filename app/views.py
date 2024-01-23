from app import app
# app/views.py
from flask import render_template, Blueprint, redirect, request, jsonify,flash,session
import mysql.connector

index = Blueprint('index', __name__)
#Connect with the databse in mysql
mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="renumeration_bill"
    )

mycursor=mydb.cursor()

#Routes

@index.route("/")
def renumuration_form():
    return render_template('Renumuration_form.html')


#Display Staff Names based on Pan number

def get_staff_name_from_database(pan_number):
    try:
        print(pan_number)
        query = "SELECT Names FROM faculty_information WHERE pan_no  = %s"
        mycursor.execute(query, (pan_number,))
        result = mycursor.fetchone()
        print(result)

        if result:
            print(result[0])
            return result[0]  # Return the staff name
        else:
            flash("Not Found Pan Number! Plz check your Pan Number")
    except Exception as e:
        print("Error fetching staff name:", e)
    
    return None  # Return None if staff name is not found


#Fetch subject name based on subject code

def get_subject_name_from_database(subject_code):
    try:
        query="SELECT subject_name FROM subject_information WHERE subject_code = %s"
        mycursor.execute(query,(subject_code,))
        result=mycursor.fetchone()

        if result:
            print(result[0])
            return result[0]
    except Exception as e:
        print("Error in fetching subject code :",e)
    return None  # Return None is subject name not found


#Fetch all subject codes for subject_information table

def get_all_subject_codes_from_database():
    try:
        query="SELECT subject_code FROM subject_information"
        mycursor.execute(query)
        result=mycursor.fetchall()
        subject_names = [row[0] for row in result]
        #print(subject_names)
        return subject_names

    except Exception as e:
        print("Error fetching subject names:", e)
        return None



@index.route("/renumuration_bill")
def renumuration_bill():
    return render_template('Renumeration_Bill.html')

#Axios for fetching staff name when pan number is entered

@index.route("/get_staff_name", methods=["GET"])
def get_staff_name():
    pan_number = request.args.get("panNumber")
    print(pan_number)
    staff_name = get_staff_name_from_database(pan_number)
    #print(staff_name)
    return jsonify({"staffName": staff_name})

#Axios for fetching all subject codes when  page start running 

@index.route("/get_all_subject_codes",methods=["GET"])
def get_all_sbuject_names():
    try:
        subject_codes=get_all_subject_codes_from_database()
        #print(subject_codes)
        return jsonify({"subjectCodes":subject_codes})
    except Exception as e:
        print("Error fetching all subject names:",e)
        return jsonify({"error":"Internal Server Error"}),500

#Axios for fetching subject name when subject code is selected

@index.route("/get_subject_name",methods=["GET"])
def get_subject_code():
    subject_code=request.args.get("subject_code")
    print(subject_code)
    subject_name=get_subject_name_from_database(subject_code)
    return jsonify({"subjectName":subject_name})


#Form information

@index.route('/submit_form', methods=['POST'])
def submit_form():
    pan_number = request.form.get('inputpanno')
    proceeding_no=request.form.get('inputprceedingno')
    name_of_the_examination=request.form.get('inputnameofexamination')
    subject_name=request.form.get('inputsubject')
    subject_code=request.form.get('inputcode')
    name_of_the_staff=request.form.get('inputname')
    phone_no=request.form.get('inputphoneno')
    designation=request.form.get('inputdesignation')
    #print(pan_number,proceeding_no,subject_code,subject_name,name_of_the_examination,name_of_the_staff,phone_no,designation)
     
    
    # fetching faculty information form table

    query2="SELECT bank_account,ifsc_code FROM faculty_information WHERE pan_no =  %s"
    mycursor.execute(query2,(pan_number,))
    faculty_data=mycursor.fetchone()
    bank_account_no=str(faculty_data[0])
    ifsc_code=faculty_data[1]
    #print(bank_account_no)
    #print(ifsc_code)
    #print(data)
    #data=list(enumerate(data))
    
    return render_template('Renumeration_Bill.html',pan_number=pan_number,
        proceeding_no=proceeding_no,
        name_of_the_examination=name_of_the_examination,
        subject_name=subject_name,
        subject_code=subject_code,
        name_of_the_staff=name_of_the_staff,
        phone_no=phone_no,
        designation=designation,
        bank_account_no=bank_account_no,
        ifsc_code=ifsc_code,
        )

#Store Renumeration Bill information in a examination_bill table

@index.route('/bill_submitted', methods=['POST'])
def bill_submitted():
    try:
        pan_no = request.form.get('pan_number')
        name_of_the_staff = request.form.get('name_of_the_staff')
        transaction_type = request.form.get('transaction_type')
        bank_account_no=request.form.get('bank_account_no')
        ifsc_code=request.form.get('ifsc_code')

        for i in range(1, 15):
            quantity = request.form.get(f'quantity_{i}', type=float)
            rate_per = request.form.get(f'rate_{i}', type=float)
       
            if quantity is not None and rate_per is not None:
                no_of_scripts = quantity
                rate = rate_per
                valid_values_found = True
                break  # Exit the loop once valid values are found

            # Access grandTotal value
        grand_total = request.form.get('grandTotal', type=float)
        print("-------------*******-------------------------")
        print("Pan No:", pan_no)
        print("Name of the Staff", name_of_the_staff)
        print("Bank Account No : ",bank_account_no)
        print("IFSC code : ",ifsc_code)
        print("Transaction Type:", transaction_type)
        print("No. of scripts:", no_of_scripts)
        print("Rate:", rate)
        print("Grand Total:", grand_total)
        print("-------------*******-------------------------")

        if not valid_values_found:
            error_message = "Please enter values for 'No. of scripts' and 'Rate'."
            print(error_message)
            response = {"status": "error", "message": error_message}
            return jsonify(response)
        
        query = """
        INSERT INTO examination_bills 
        (pan_no,name_of_the_staff,transaction_type,bank_account_no,ifsc_code,no_of_scripts,rate,grand_total) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

        values = (pan_no,name_of_the_staff,transaction_type,bank_account_no,ifsc_code,no_of_scripts,rate,grand_total)
        mycursor.execute(query, values)
        mydb.commit()
        
        response = {"status": "success", "message": "Data successfully saved!"}
        return jsonify(response)
    except Exception as e:
        # Display error message using Toastr
        response = {"status": "error", "message": "Error occured while storing data Plz fill required data No_of_scripts or Rate"}
        return jsonify(response)


# Bill submit message

@index.route('/success')
def success():
    
    return render_template('Success.html', success_message="Data Successfully Saved!....")


#Admin Page Route    

@index.route('/admin')
def admin():
    return render_template('Admin.html')   

#Final Report 

@index.route('/form_admin',methods=['POST'])
def form_admin():
    #examination_id=request.form.get('examination_id')
    transaction_type=request.form.get('transaction_type')
    print("--------------*********----------")
    print(transaction_type)
    print("--------------*********----------")
    select_query = """
        SELECT * FROM examination_bills
        WHERE transaction_type = %s
    """
    mycursor.execute(select_query, (transaction_type,))
    rows = mycursor.fetchall()

    # Print or process the retrieved rows
    for row in rows:
        print("*******************")
        print(row)
    
    unique_names=set(row[2] for row in rows)
    print("--------------------------")
    print("Unique Names",unique_names)

    return render_template('Report.html',rows=rows,unique_names=unique_names)



