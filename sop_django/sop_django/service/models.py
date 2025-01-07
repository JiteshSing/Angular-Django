from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return data

    class Meta:
        db_table = 'SOS_ROLE'

class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    login_id = models.EmailField()
    password = models.CharField(max_length=20)
    confirmpassword = models.CharField(max_length=20, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default = '')
    gender = models.CharField(max_length=50,default='')
    mobilenumber = models.CharField(max_length=50,default='')
    role_Id = models.IntegerField()
    role_Name = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'login_id': self.login_id,
            'password': self.password,
            'confirmpassword': self.confirmpassword,
            'dob': self.dob,
            'address': self.address,
            'gender': self.gender,
            'mobilenumber': self.mobilenumber,
            'role_Id': self.role_Id,
            'role_Name': self.role_Name
        }

        return data

    class Meta:
        db_table = 'SOS_USER'

class College(models.Model):
    collegeName = models.CharField(max_length=50)
    collegeAddress = models.CharField(max_length=50)
    collegeState = models.CharField(max_length=50)
    collegeCity = models.CharField(max_length=20)
    collegePhoneNumber = models.CharField(max_length=20)

    def to_json(self):
        data = {
            'id': self.id,
            'collegeName': self.collegeName,
            'collegeAddress': self.collegeAddress,
            'collegeState': self.collegeState,
            'collegeCity': self.collegeCity,
            'collegePhoneNumber': self.collegePhoneNumber
        }
        return data

    class Meta:
        db_table = 'SOS_COLLEGE'


class BaseModel(models.Model):
    def to_json(self):
        data = {}
        return data


class Course(models.Model):
    courseName = models.CharField(max_length=50)
    courseDescription = models.CharField(max_length=100)
    courseDuration = models.CharField(max_length=100)

    def to_json(self):
        data = {
            'id': self.id,
            'courseName': self.courseName,
            'courseDescription': self.courseDescription,
            'courseDuration': self.courseDuration
        }
        return data

    class Meta:
        db_table = 'SOS_COURSE'

class vehicle(models.Model):
    vehicleId = models.CharField(max_length=50)
    vehicleName = models.CharField(max_length=50)
    vehicleType = models.CharField(max_length=50)
    purchaseDate = models.DateField(max_length=20)
    buyerName = models.CharField(max_length=20)
    tid=models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'vehicleId': self.vehicleId,
            'vehicleName': self.vehicleName,
            'vehicleType': self.vehicleType,
            'purchaseDate': self.purchaseDate,
            'buyerName': self.buyerName,
            'tid' : self.tid

        }
        return data

    class Meta:
        db_table = 'SOS_VEHICLE'

class Project(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    openDate = models.DateField(max_length=20)
    version = models.CharField(max_length=20)
    cid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'openDate': self.openDate,
            'version': self.version,
            'cid': self.cid

        }
        return data

    class Meta:
        db_table = 'SOS_PROJECT'


class Lead(models.Model):
    date = models.DateField(max_length=20)
    contactName = models.CharField(max_length=50)
    mobile = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20)
    sid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'date': self.date,
            'contactName': self.contactName,
            'mobile': self.mobile,
            'status': self.status,
            'sid': self.sid

        }
        return data

    class Meta:
        db_table = 'SOS_Lead'

class Order(models.Model):
    quantity=models.IntegerField(default=0)
    product = models.CharField(max_length=50)
    date = models.DateField(max_length=20)
    amount=models.BigIntegerField(default=0)
    oid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'quantity': self.quantity,
            'product': self.product,
            'date': self.date,
            'amount': self.amount,
            'oid': self.oid

        }
        return data

    class Meta:
        db_table = 'SOS_ORDER'

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobile = models.BigIntegerField(default=0)
    expertise = models.CharField(max_length=20)
    did = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'dob': self.dob,
            'mobile': self.mobile,
            'expertise': self.expertise,
            'did': self.did

        }
        return data

    class Meta:
        db_table = 'SOS_DOCTOR'

class Employee(models.Model):
    fullName = models.CharField(max_length=50)
    username = models.EmailField(max_length=20)
    password = models.CharField(max_length=20)
    dob = models.DateField(max_length=20)
    number = models.BigIntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'fullName': self.fullName,
            'username': self.username,
            'password': self.password,
            'dob': self.dob,
            'number': self.number,

        }
        return data

    class Meta:
        db_table = 'SOS_EMPLOYEE'

class Task(models.Model):
    creationDate = models.DateField(max_length=20)
    taskTitle = models.CharField(max_length=50)
    details = models.CharField(max_length=50)
    assignedTo = models.CharField(max_length=50)
    taskStatus = models.CharField(max_length=50)
    tid = models.IntegerField(default=0)
    aid = models.IntegerField(default=0)


    def to_json(self):
        data = {
            'id': self.id,
            'creationDate': self.creationDate,
            'taskTitle': self.taskTitle,
            'details': self.details,
            'assignedTo': self.assignedTo,
            'taskStatus': self.taskStatus,
            'tid': self.tid,
            'aid': self.aid

        }
        return data

    class Meta:
        db_table = 'SOS_TASK'

class Initiative(models.Model):
    initiativeName = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    startDate = models.DateField(max_length=20)
    number = models.BigIntegerField(default=0)
    tid = models.IntegerField(default=0)


    def to_json(self):
        data = {
            'id': self.id,
            'initiativeName': self.initiativeName,
            'type': self.type,
            'startDate': self.startDate,
            'number': self.number,
            'tid': self.tid

        }
        return data

    class Meta:
        db_table = 'SOS_INITIATIVE'
class Wishlist(models.Model):
    product = models.CharField(max_length=50)
    date = models.DateField(max_length=20)
    name = models.CharField(max_length=50)
    remark = models.CharField(max_length=50)
    pid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'product': self.product,
            'date': self.date,
            'name': self.name,
            'remark': self.remark,
            'pid': self.pid

        }
        return data

    class Meta:
        db_table = 'SOS_WISHLIST'

class Supplier(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    registrationDate = models.DateField(max_length=20)
    paymentTerm=models.BigIntegerField(default=0)
    sid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'registrationDate': self.registrationDate,
            'paymentTerm': self.paymentTerm,
            'sid': self.sid

        }
        return data

    class Meta:
        db_table = 'SOS_SUPPLIER'

class Staffmember(models.Model):
    fullName = models.CharField(max_length=50)
    joiningDate = models.DateField(max_length=20)
    division = models.CharField(max_length=50)
    previousEmployer=models.CharField(max_length=50)
    did = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'fullName': self.fullName,
            'division': self.division,
            'joiningDate': self.joiningDate,
            'previousEmployer': self.previousEmployer,
            'did': self.did

        }
        return data

    class Meta:
        db_table = 'SOS_STAFFMEMBER'

class Position(models.Model):
    designation = models.CharField(max_length=50)
    openingDate = models.DateField(max_length=20)
    requiredExperience = models.CharField(max_length=50)
    condition=models.CharField(max_length=50)
    cid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'designation': self.designation,
            'openingDate': self.openingDate,
            'requiredExperience': self.requiredExperience,
            'condition': self.condition,
            'cid': self.cid

        }
        return data

    class Meta:
        db_table = 'SOS_POSITION'

class Portfoliomanagement(models.Model):
    portfolioName = models.CharField(max_length=50)
    initialinvestmentAmount = models.BigIntegerField(default=0)
    risktoleranceLevel = models.CharField(max_length=50)
    investmentStrategy = models.CharField(max_length=250)
    rid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'portfolioName': self.portfolioName,
            'initialinvestmentAmount': self.initialinvestmentAmount,
            'risktoleranceLevel': self.risktoleranceLevel,
            'investmentStrategy': self.investmentStrategy,
            'rid': self.rid

        }
        return data

    class Meta:
        db_table = 'SOS_PORTFOLIOMANAGEMENT'

class Customer(models.Model):
    clientName = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    contactNumber = models.BigIntegerField(default=0)
    importance = models.CharField(max_length=250)
    cid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'clientName': self.clientName,
            'location': self.location,
            'contactNumber': self.contactNumber,
            'importance': self.importance,
            'cid': self.cid

        }
        return data

    class Meta:
        db_table = 'SOS_CUSTOMER'

class Market(models.Model):
    quantity = models.BigIntegerField(default=0)
    purchasePrice = models.FloatField(default=0)
    purchaseDate = models.DateField(max_length=20)
    orderType = models.CharField(max_length=50)
    oid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'quantity': self.quantity,
            'purchasePrice': self.purchasePrice,
            'purchaseDate': self.purchaseDate,
            'orderType': self.orderType,
            'oid': self.oid

        }
        return data

    class Meta:
        db_table = 'SOS_MARKET'


class Purchaseorder(models.Model):
    totalQuantity = models.BigIntegerField(default=0)
    product = models.CharField(max_length=50)
    orderDate = models.DateField(max_length=20)
    totalCost = models.BigIntegerField(default=0)
    pid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'totalQuantity': self.totalQuantity,
            'product': self.product,
            'orderDate': self.orderDate,
            'totalCost':self.totalCost,
            'pid': self.pid

        }
        return data

    class Meta:
        db_table = 'SOS_PURCHASEORDER'

# class Issue(models.Model):
#     openDate = models.DateField(max_length=20)
#     title= models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     assignTo= models.CharField(max_length=50)
#     status=models.CharField(max_length=50)
#     sid=models.IntegerField(default=0)
#     aid=models.IntegerField(default=0)
#
#     def to_json(self):
#         data = {
#             'id': self.id,
#             'openDate': self.openDate,
#             'title': self.title,
#             'description': self.description,
#             'assignTo': self.assignTo,
#             'status': self.status,
#             'sid':self.sid,
#             'aid': self.sid
#         }
#         return data
#
#     class Meta:
#         db_table = 'SOS_ISSUE'

class Medication(models.Model):
    fullName = models.CharField(max_length=50)
    illness = models.CharField(max_length=50)
    prescriptionDate = models.DateField(max_length=20)
    dosage=models.BigIntegerField(default=0)
    mid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'fullName': self.fullName,
            'illness': self.illness,
            'prescriptionDate': self.prescriptionDate,
            'dosage': self.dosage,
            'mid': self.mid

        }
        return data

    class Meta:
        db_table = 'SOS_MEDICATION'

# class Owner(models.Model):
#     name= models.CharField(max_length=50)
#     dob = models.DateField(max_length=20)
#     vehicleId = models.IntegerField(default=0)
#     insuranceAmount= models.IntegerField(default=0)
#     did=models.IntegerField(default=0)
#     vid=models.IntegerField(default=0)
#
#     def to_json(self):
#         data = {
#             'id': self.id,
#             'name': self.name,
#             'dob': self.dob,
#             'vehicleId': self.vehicleId,
#             'insuranceAmount': self.insuranceAmount,
#             'did':self.did,
#             'vid': self.vid
#         }
#         return data
#
#     class Meta:
#         db_table = 'SOS_OWNER'

class Contact(models.Model):
    name= models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobile = models.BigIntegerField(default=0)
    cid=models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'dob': self.dob,
            'mobile': self.mobile,
            'cid':self.cid,
        }
        return data

    class Meta:
        db_table = 'SOS_CONTACT'
class Faculty(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'password': self.password,
            'address': self.address,
            'gender': self.gender,
            'dob': self.dob,
            'college_ID': self.college_ID,
            'collegeName': self.courseName,
            'subject_ID': self.subject_ID,
            'subjectName': self.subjectName,
            'course_ID': self.course_ID,
            'courseName': self.courseName,
        }
        return data

    class Meta:
        db_table = 'SOS_FACULTY'


class Marksheet(models.Model):
    rollNumber = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    maths = models.IntegerField()

    def to_json(self):
        data = {
            'id': self.id,
            'rollNumber': self.rollNumber,
            'name': self.name,
            'physics': self.physics,
            'chemistry': self.chemistry,
            'maths': self.maths
        }
        return data

    class Meta:
        db_table = 'SOS_MARKSHEET'


class Student(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobileNumber = models.CharField(max_length=20)
    email = models.EmailField()
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'dob': self.dob,
            'mobileNumber': self.mobileNumber,
            'email': self.email,
            'college_ID': self.college_ID,
            'collegeName': self.collegeName
        }
        return data

    class Meta:
        db_table = 'SOS_STUDENT'


class Subject(models.Model):
    subjectName = models.CharField(max_length=50)
    subjectDescription = models.CharField(max_length=50)

    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'subjectName': self.subjectName,
            'subjectDescription': self.subjectDescription,
            # 'dob':self.dob,
            'course_ID': self.course_ID,
            # 'courseName': self.courseName
        }
        return data

    class Meta:
        db_table = 'SOS_SUBJECT'

class TimeTable(models.Model):
    examTime = models.CharField(max_length=40)
    examDate = models.DateField()
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'examTime': self.examTime,
            'examDate': self.examDate,
            'subject_ID': self.subject_ID,
            'subjectName': self.subjectName,
            'course_ID': self.course_ID,
            'courseName': self.courseName,
            'semester': self.semester
        }
        return data

    class Meta:
        db_table = 'SOS_TIMETABLE'