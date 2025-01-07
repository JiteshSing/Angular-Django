from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Employee
from service.service.EmployeeService import EmployeeService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class EmployeeCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['fullName'] = requestForm['fullName']
        self.form['username'] = requestForm["username"]
        self.form['password'] = requestForm["password"]
        self.form['dob'] = requestForm["dob"]
        self.form['number'] = requestForm["number"]

    def input_validation(self):
        inputError = self.form["inputError"]


        if (DataValidator.isNull(self.form['fullName'])):
            self.form["error"] = True
            inputError["fullName"] = "Name can not be null"
        elif (DataValidator.max_len_50(self.form['fullName'])):
            inputError['fullName'] = "Name can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['fullName'])):
                inputError['fullName'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["username"])):
            self.form["error"] = True
            inputError["fullName"] = "username can not be null"
        elif (DataValidator.isemail(self.form["username"])):
                self.form["error"] = True
                inputError["username"] = "Email Id must be like mailto:abc@gmail.com"
        else:
            if (DataValidator.max_len_50(self.form['username'])):
                inputError['username'] = "username can be only 50 character"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['password'])):
            self.form["error"] = True
            inputError["password"] = "password can not be null"
        else:
            if (DataValidator.max_len_10(self.form['password'])):
                inputError['password'] = "password can be only 10 character"
                self.form['error'] = True

        if DataValidator.isNull(self.form['dob']):
            inputError['dob'] = "Date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['dob']):
                inputError['dob'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if DataValidator.isNull(self.form['number']):
            inputError['number'] = "Mobile No. can't be NUll"
            self.form['error'] = True

        elif (DataValidator.ismobilecheck(self.form['number'])):
                inputError['number'] = "Mobile No. should start with 6,7,8,9 and no. must be of 10 digits"
                self.form['error'] = True
        else:
            if (DataValidator.max_len_10(self.form['number'])):
                inputError['number'] = "number can be only 10 digit"
                self.form['error'] = True

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]
        if DataValidator.isNotNull(self.form['number']):
            if (DataValidator.ismobilecheck(self.form['number'])):
                inputError['number'] = "Mobile No. should start with 6,7,8,9 and no. must be of 10 digits"
                self.form['error'] = True
            else:
                if (DataValidator.max_len_10(self.form['number'])):
                    inputError['number'] = "number can be only 10 digit"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['fullName'])):
            if (DataValidator.max_len_50(self.form['fullName'])):
                inputError['fullName'] = "Name can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['fullName'])):
                    inputError['fullName'] = "Name contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form["username"])):
            if (DataValidator.isemail(self.form["username"])):
                self.form["error"] = True
                inputError["username"] = "Email Id must be like mailto:abc@gmail.com"
            else:
                if (DataValidator.max_len_50(self.form['username'])):
                    inputError['username'] = "username can be only 50 character"
                    self.form['error'] = True


        if DataValidator.isNotNull(self.form['dob']):
            if DataValidator.isDate(self.form['dob']):
                inputError['dob'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True


        return self.form["error"]

    def get(self, request, params={}):
        c = self.get_service().get(params['id'])
        res = {}
        if (c != None):
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data found"
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data": res["data"]})

    def delete(self, request, params={}):
        c = self.get_service().get(params["id"])
        res = {}
        if (c != None):
            self.get_service().delete(params["id"])
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data has been deleted Successfully"
        else:
            res["error"] = True
            res["message"] = "Data was not deleted"
        return JsonResponse({"data": res})

    def search(self, request, params={}):
        res = {}
        json_request = json.loads(request.body)
        if (json_request):
            params["name"] = json_request.get("name", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg":""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Employee.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        json_request = json.loads(request.body)
        json_request['id'] = 0
        # json_request['cid'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["fullName"] = json_request.get("fullName", None)
            params["username"] = json_request.get("username", None)
            params["password"] = json_request.get("password", None)
            params["dob"] = json_request.get("dob", None)
            params["number"] = json_request.get("number", None)
            params["pageNo"] = json_request.get("pageNo", None)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation1()):
            print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            res["error"] = True
            res["mesg"] = "NO record found"
        else:
            c = self.get_service().search1(params)
            # res = {"mesg": ""}
            if (c != None):
                res["data"] = c["data"]
                if res["data"] == []:
                    res["mesg"] = "No record found"
                res["MaxId"] = c["MaxId"]
                res["index"] = c["index"]
                res["LastId"] = Employee.objects.last().id
                res["error"] = False
            else:
                res["error"] = True
                res["message"] = "No record found"
        return JsonResponse({"result": res, "form": self.form})

    def find_dict_index(self, dict_list, key, value):
        for index, item in enumerate(dict_list):
            if int(item.get(key)) == int(value):
                print('--------------', index)
                return index

    def form_to_model(self, obj):
        # preload_response = self.preload(None).content.decode()
        # preload_data = json.loads(preload_response)
        # preload_list = preload_data["preloadList"]
        #
        # index = self.find_dict_index(preload_list, 'eid', self.form['eid'])

        print("ORS API Employee ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.fullName = self.form["fullName"]
        obj.username = self.form["username"]
        obj.password = self.form["password"]
        obj.dob = self.form["dob"]
        obj.number = self.form["number"]
        return obj

    def save(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            if (self.form["id"] > 0):
                dup = Employee.objects.exclude(id=self.form['id']).filter(username=self.form["username"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Employee username already exists"
                else:
                    r = self.form_to_model(Employee())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Employee.objects.filter(username=self.form["username"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Employee username already exists"
                else:
                    r = self.form_to_model(Employee())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Employee
    def get_service(self):
        return EmployeeService()
