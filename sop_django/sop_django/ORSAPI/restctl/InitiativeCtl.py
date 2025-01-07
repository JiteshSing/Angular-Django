from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Initiative
from service.service.InitiativeService import InitiativeService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class InitiativeCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'tid': 1, 'type': "cancer"},
            {'tid': 2, 'type': "heart"},
            {'tid': 3, 'type': "lungs"},

        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['initiativeName'] = requestForm['initiativeName']
        self.form['tid'] = requestForm["tid"]
        self.form['startDate'] = requestForm["startDate"]
        self.form['number'] = requestForm["number"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form['initiativeName'])):
            self.form["error"] = True
            inputError["initiativeName"] = "initiativeName can not be null"
        elif (DataValidator.max_len_50(self.form['initiativeName'])):
            inputError['initiativeName'] = "initiativeName can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['initiativeName'])):
                inputError['initiativeName'] = "initiativeName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['tid'])):
            self.form["error"] = True
            inputError["tid"] = "type can not be null"

        if DataValidator.isNull(self.form['startDate']):
            inputError['startDate'] = "startDate can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['startDate']):
                inputError[
                    'startDate'] = "Incorrect Date format, should be DD-MM-YYYY format and startDate should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['number'])):
            self.form["error"] = True
            inputError["number"] = "version number can not be null"
        elif (DataValidator.isnumb(self.form['number'])):
            inputError['number'] = "version number only be digit"
            self.form['error'] = True
        else:
            if (DataValidator.max_len_10(self.form['number'])):
                inputError['number'] = "version number can be only 10 digit"
                self.form['error'] = True


        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNotNull(self.form["number"])):
            if (DataValidator.max_len_10(self.form['number'])):
                inputError['number'] = "version number can should be below 10 digit"
                self.form['error'] = True
            else:
                if (DataValidator.isnumb(self.form['number'])):
                    inputError['number'] = "version number should be only digit"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['initiativeName'])):
            if (DataValidator.max_len_50(self.form['initiativeName'])):
                inputError['initiativeName'] = "initiativeName can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['initiativeName'])):
                    inputError['initiativeName'] = "initiativeName contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['tid'])):
            pass

        if DataValidator.isNotNull(self.form['startDate']):
            if DataValidator.isDate(self.form['startDate']):
                inputError[
                    'startDate'] = "Incorrect Date format, should be DD-MM-YYYY format and startDate should in past or present"
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
            params["initiativeName"] = json_request.get("initiativeName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Initiative.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        json_request = json.loads(request.body)
        json_request['id'] = 0
        # json_request['tid'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["initiativeName"] = json_request.get("initiativeName", None)
            params["tid"] = json_request.get("tid", None)
            params["startDate"] = json_request.get("startDate", None)
            params["number"] = json_request.get("number", None)
            params["pageNo"] = json_request.get("pageNo", None)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation1()):
            print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            res["error"] = True
            res["message"] = ""
        else:
            c = self.get_service().search1(params)
            res = {"mesg": ""}
            if (c != None):
                res["data"] = c["data"]
                if res["data"] == []:
                    res["mesg"] = "No record found"
                res["MaxId"] = c["MaxId"]
                res["index"] = c["index"]
                res["LastId"] = Initiative.objects.last().id
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

        index = self.find_dict_index(preload_list, 'tid', self.form['tid'])

        print("ORS API Initiative ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.initiativeName = self.form["initiativeName"]
        obj.type = preload_list[index]["type"]
        obj.startDate = self.form["startDate"]
        obj.number = self.form["number"]
        obj.tid = self.form["tid"]
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
                dup = Initiative.objects.exclude(id=self.form['id']).filter(number=self.form["number"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "version number already exists"
                else:
                    r = self.form_to_model(Initiative())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Initiative.objects.filter(number=self.form["number"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "version number already exists"
                else:
                    r = self.form_to_model(Initiative())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Initiative
    def get_service(self):
        return InitiativeService()
