from flask import Flask, render_template, request, url_for, redirect

import pymongo;
import collections
import sys
print(sys.path)

from random import randint
  

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['ncdpython']
collection = db['patient']

@app.route('/')
def welcome():
    return render_template('registration.html')

def home():
    #when we are trying to re render it its showing method not allowed 
    return redirect(url_for('welcome'))

def making_global(aadh):
    global aadhaar
    aadhaar=aadh
    


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method=="POST":

        firstname=""
        lastname=""
        gender=""
        aadhaar=""
        phone=""
        birthday=""
        pincode=""
        total=0
        screening=""
        msg = " "
        patient_id=""

        firstname=request.form['firstname']
        lastname=request.form['lastname']
        gender=request.form['gender']
        aadhaar=request.form['aadhaar']
        phone=request.form['phone']
        birthday=request.form['birthday']
        pincode=request.form['pincode']

    making_global(aadhaar)

    pid=collection.find({"patient_id":1,"_id":0})
    #print(pid)
    pid2=dict(pid)
    if(len(pid2)>0):
        for i in pid:
            id=random_n_digits(14)
            if(id==i):
                continue
            else:
                patient_dict={
                    "patient_id" : id,
                    "first_name" : firstname,
                    "last_name" : lastname, 
                    "gender" : gender , 
                    "aadhaar_uid" : aadhaar, 
                    "phone_no" : phone, 
                    "dob" : birthday, 
                    "pincode" : pincode
                }
                collection.insert_one(patient_dict)
                break
                
                
    else:
        id=random_n_digits(14)
        patient_dict={
                    "patient_id" : id,
                    "first_name" : firstname,
                    "last_name" : lastname, 
                    "gender" : gender , 
                    "aadhaar_uid" : aadhaar, 
                    "phone_no" : phone, 
                    "dob" : birthday, 
                    "pincode" : pincode
                }
        collection.insert_one(patient_dict)
    
        patient_id = collection.find_one({"aadhaar_uid": aadhaar},{"patient_id" : 1, "_id" : 0})

    return render_template('question.html',patient_id=patient_id.get('patient_id'))

def random_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
    

@app.route('/submit', methods=['GET','POST'])
def ncd_rac():
    if request.method == "POST":
        total=0
        age=-1
        smoke=-1
        alcohol=-1
        waist=-1
        phy_act=-1
        fam_his=-1
        
        age = int(request.form['age'])
        if (age ==-1):
            return redirect(url_for('fail'))
        
        smoke = int(request.form['smoke'])
        if (smoke == -1):
            return redirect(url_for('fail'))

        alcohol = int(request.form['smoke'])
        if (alcohol == -1):
            return redirect(url_for('fail'))

        waist = int(request.form['waist'])
        if (waist ==-1):
            return redirect(url_for('fail'))

        phy_act = int(request.form['phy_act'])
        if (phy_act == -1):
            return redirect(url_for('fail'))

        fam_his = int(request.form['fam_his'])
        if (fam_his == -1):
            return redirect(url_for('fail'))   

        total = age + smoke + alcohol + waist + phy_act + fam_his

        res=""
        screening=""
        
        if total>4:
            res="The person may be at higher risk of NCDs and needs to be prioritized for attending screening."
            screening ="yes";
        else:
            res="The person is not at risk of NCDs and doesn't need screening."
            screening ="no";

    
    prev={"aadhaar_uid" : aadhaar}
    nextt={"$set" : {"score" : total,"screening" : screening}}
    collection.update_one(prev, nextt)   

    return render_template('result.html',result=res,total=total, age=age,smoke=smoke,alcohol=alcohol,
                            waist=waist,phy_act=phy_act,fam_his=fam_his)              
    

@app.route('/fail')
def fail():
    str="Please answer all the questions."
    return render_template('error.html',str=str)

#back to registration.html page
@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('registration.html')


if __name__ == "__main__":  
    app.run(debug=True, port=8000)
    """client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['ncdpython']
    collections = db['patient']"""

'''@app.route('/success/<int:score>')
def success(score):
    res=""
    #print(score)
    if score>4:
        res="The person may be at higher risk of NCDs and needs to be prioritized for attending screening."
    else:
        res="The person is not at risk of NCDs and doesn't need screening."

    return render_template('result.html',result=res,sc=score)'''

