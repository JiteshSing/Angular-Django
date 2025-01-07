from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Doctor
from service.service.DoctorService import DoctorService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class DoctorCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'did': 1, 'expertise': "cancer"},
            {'did': 2, 'expertise': "heart"},
            {'did': 3, 'expertise': "lungs"},

        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['name'] = requestForm['name']
        self.form['did'] = requestForm["did"]
        self.form['dob'] = requestForm["dob"]
        self.form['mobile'] = requestForm["mobile"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form['name'])):
            self.form["error"] = True
            inputError["name"] = "name can not be null"
        elif (DataValidator.max_len_50(self.form['name'])):
            inputError['name'] = "name can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['name'])):
                inputError['name'] = "name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['did'])):
            self.form["error"] = True
            inputError["did"] = "expertise can not be null"

        if DataValidator.isNull(self.form['dob']):
            inputError['dob'] = "dob can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['dob']):
                inputError[
                    'dob'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['mobile'])):
            self.form["error"] = True
            inputError["mobile"] = "mobile can not be null"
        elif (DataValidator.ismobilecheck(self.form['mobile'])):
            inputError['mobile'] = "mobile can should be start with 9,8,7,6 digit and 10 digit max"
            self.form['error'] = True
        else:
            if (DataValidator.max_len_10(self.form['mobile'])):
                inputError['mobile'] = "mobile can be only 10 digit"
                self.form['error'] = True


        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNotNull(self.form["mobile"])):
            if (DataValidator.max_len_10(self.form['mobile'])):
                inputError['mobile'] = "mobile can should be below 10 digit"
                self.form['error'] = True
            else:
                if (DataValidator.ismobilecheck(self.form['mobile'])):
                    inputError['mobile'] = "mobile can should be start with 9,8,7,6 digit"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['name'])):
            if (DataValidator.max_len_50(self.form['name'])):
                inputError['name'] = "name can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['name'])):
                    inputError['name'] = "name contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['did'])):
            pass

        if DataValidator.isNotNull(self.form['dob']):
            if DataValidator.isDate(self.form['dob']):
                inputError[
                    'dob'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
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
        # res = {}
        json_request = json.loads(request.body)
        if (json_request):
            params["name"] = json_request.get("name", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Doctor.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        json_request = json.loads(request.body)
        json_request['id'] = 0
        # json_request['did'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["name"] = json_request.get("name", None)
            params["did"] = json_request.get("did", None)
            params["dob"] = json_request.get("dob", None)
            params["mobile"] = json_request.get("mobile", None)
            params["pageNo"] = json_request.get("pageNo", None)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation1()):
            print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            res["error"] = True
            res["message"] = ""
        else:
            c = self.get_service().search1(params)
            # res = {"mesg": ""}
            if (c != None):
                res["data"] = c["data"]
                if res["data"] == []:
                    res["mesg"] = "No record found"
                res["MaxId"] = c["MaxId"]
                res["index"] = c["index"]
                res["LastId"] = Doctor.objects.last().id
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
        preload_response = self.preload(None).content.decode()
        preload_data = json.loads(preload_response)
        preload_list = preload_data["preloadList"]

        index = self.find_dict_index(preload_list, 'did', self.form['did'])

        print("ORS API Doctor ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.name = self.form["name"]
        obj.expertise = preload_list[index]["expertise"]
        obj.dob = self.form["dob"]
        obj.mobile = self.form["mobile"]
        obj.did = self.form["did"]
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
                dup = Doctor.objects.exclude(id=self.form['id']).filter(mobile=self.form["mobile"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Mobile number already exists"
                else:
                    r = self.form_to_model(Doctor())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Doctor.objects.filter(mobile=self.form["mobile"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Mobile number already exists"
                else:
                    r = self.form_to_model(Doctor())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Doctor
    def get_service(self):
        return DoctorService()
