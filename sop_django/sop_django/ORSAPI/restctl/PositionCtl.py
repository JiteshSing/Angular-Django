from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Position
from service.service.PositionService import PositionService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class PositionCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'cid': 1, 'condition': "Open"},
            {'cid': 2, 'condition': "Closed"},
            {'cid': 3, 'condition': "OnHold"},

        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['designation'] = requestForm['designation']
        self.form['cid'] = requestForm["cid"]
        self.form['openingDate'] = requestForm["openingDate"]
        self.form['requiredExperience'] = requestForm["requiredExperience"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form['designation'])):
            self.form["error"] = True
            inputError["designation"] = "designation can not be null"
        elif (DataValidator.max_len_50(self.form['designation'])):
            inputError['designation'] = "designation can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['designation'])):
                inputError['designation'] = "designation contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['cid'])):
            self.form["error"] = True
            inputError["cid"] = "condition can not be null"

        if DataValidator.isNull(self.form['openingDate']):
            inputError['openingDate'] = "openingDate can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['openingDate']):
                inputError[
                    'openingDate'] = "Incorrect openingDate format, should be DD-MM-YYYY format and openingDate should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['requiredExperience'])):
            self.form["error"] = True
            inputError["requiredExperience"] = "requiredExperience can not be null"


        elif (DataValidator.max_len_50(self.form['requiredExperience'])):

            inputError['requiredExperience'] = "requiredExperience can should be below 50 character"

            self.form['error'] = True

        else:

            if (DataValidator.isalphacheck(self.form['requiredExperience'])):
                inputError['requiredExperience'] = "requiredExperience contains only letters"

                self.form['error'] = True

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNotNull(self.form["requiredExperience"])):
            if (DataValidator.isalphacheck(self.form['requiredExperience'])):
                inputError['requiredExperience'] = "requiredExperience contain only letter"
                self.form['error'] = True
            else:
                if (DataValidator.max_len_50(self.form['requiredExperience'])):
                    inputError['requiredExperience'] = "requiredExperience can should be below 50 character"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['designation'])):
            if (DataValidator.isalphacheck(self.form['designation'])):
                inputError['designation'] = "designation contain only letter"
                self.form['error'] = True
            else:
                if (DataValidator.max_len_50(self.form['designation'])):
                    inputError['designation'] = "designation can should be below 50 character"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['cid'])):
            pass

        if DataValidator.isNotNull(self.form['openingDate']):
            if DataValidator.isDate(self.form['openingDate']):
                inputError[
                    'openingDate'] = "Incorrect openingDate format, should be DD-MM-YYYY format and openingDate should not be in past "
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
            params["designation"] = json_request.get("designation", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Position.objects.last().id
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
            params["designation"] = json_request.get("designation", None)
            params["cid"] = json_request.get("cid", None)
            params["openingDate"] = json_request.get("openingDate", None)
            params["requiredExperience"] = json_request.get("requiredExperience", None)
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
                res["LastId"] = Position.objects.last().id
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

        index = self.find_dict_index(preload_list, 'cid', self.form['cid'])

        print("ORS API Position ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.designation = self.form["designation"]
        obj.condition = preload_list[index]["condition"]
        obj.openingDate = self.form["openingDate"]
        obj.requiredExperience = self.form["requiredExperience"]
        obj.cid = self.form["cid"]
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
                dup = Position.objects.exclude(id=self.form["id"]).filter(designation=self.form["designation"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "designation  already exists"
                else:
                    r = self.form_to_model(Position())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Position.objects.exclude(id=self.form["id"]).filter(designation=self.form["designation"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = " designation  already exists"
                else:
                    r = self.form_to_model(Position())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Position
    def get_service(self):
        return PositionService()
