from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Medication
from service.service.MedicationService import MedicationService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class MedicationCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'mid': 1, 'illness': "cancer"},
            {'mid': 2, 'illness': "heart"},
            {'mid': 3, 'illness': "ortho"},
        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['fullName'] = requestForm['fullName']
        self.form['prescriptionDate'] = requestForm["prescriptionDate"]
        self.form['dosage'] = requestForm["dosage"]
        self.form['mid'] = requestForm["mid"]

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



        if DataValidator.isNull(self.form['prescriptionDate']):
            inputError['prescriptionDate'] = "prescriptionDate can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['prescriptionDate']):
                inputError['prescriptionDate'] = "Incorrect prescriptionDate format, should be DD-MM-YYYY format and prescriptionDate should in past or present"
                self.form['error'] = True

        if DataValidator.isNull(self.form['dosage']):
            inputError['dosage'] = "dosage No. can't be NUll"
            self.form['error'] = True

        elif (DataValidator.isnumb(self.form['dosage'])):
            inputError['dosage'] = "dosage should be in integer"
            self.form['error'] = True
        elif (DataValidator.is_0(self.form['dosage'])):
            inputError['dosage'] = "dosage should  be  greater than 0"
            self.form['error'] = True

        else:
            if (DataValidator.max_len_5(self.form['dosage'])):
                inputError['dosage'] = "dosage in mg should in 5 digit"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['mid'])):
            self.form["error"] = True
            inputError["mid"] = "illness can not be null"
        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]
        if DataValidator.isNotNull(self.form['dosage']):
            if (DataValidator.max_len_5(self.form['dosage'])):
                inputError['dosage'] = "dosage No. should be in 5 digits"
                self.form['error'] = True
            # else:
            #      if (DataValidator.is_0(self.form['dosage'])):
            #       inputError['dosage'] = "dosage should be in number"
            #       self.form['error'] = True




        if (DataValidator.isNotNull(self.form['fullName'])):
            if (DataValidator.max_len_50(self.form['fullName'])):
                inputError['fullName'] = "fullName can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['fullName'])):
                    inputError['fullName'] = "fullName contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['mid'])):
            pass

        if DataValidator.isNotNull(self.form['prescriptionDate']):
            if DataValidator.isDate(self.form['prescriptionDate']):
                inputError['prescriptionDate'] = "Incorrect Date format, should be DD-MM-YYYY format and prescriptionDate should in past or present"
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
            params["fullName"] = json_request.get("fullName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg":""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Medication.objects.last().id
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
            params["mid"] = json_request.get("mid", None)
            params["prescriptionDate"] = json_request.get("prescriptionDate", None)
            params["dosage"] = json_request.get("dosage", None)
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
                res["LastId"] = Medication.objects.last().id
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

        index = self.find_dict_index(preload_list, 'mid', self.form['mid'])

        print("ORS API Medication ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.fullName = self.form["fullName"]
        obj.prescriptionDate = self.form["prescriptionDate"]
        obj.dosage = self.form["dosage"]
        obj.illness = preload_list[index]["illness"]
        obj.mid = self.form["mid"]
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
                dup = Medication.objects.exclude(id=self.form['id']).filter(fullName=self.form["fullName"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Full Name already exists"
                else:
                    r = self.form_to_model(Medication())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Medication.objects.filter(fullName=self.form["fullName"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Full Name already exists"
                else:
                    r = self.form_to_model(Medication())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Medication
    def get_service(self):
        return MedicationService()
