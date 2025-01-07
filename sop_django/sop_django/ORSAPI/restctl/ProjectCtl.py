from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Project
from service.service.ProjectService import ProjectService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class ProjectCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'cid': 1, 'category': "Sedan"},
            {'cid': 2, 'category': "SUV"},
            {'cid': 3, 'category': "XUV"},
            {'cid': 4, 'category': "Pick-up"},
            {'cid': 5, 'category': "Hunchback"},
            {'cid': 6, 'category': "Sports"}
        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['name'] = requestForm['name']
        self.form['cid'] = requestForm["cid"]
        self.form['openDate'] = requestForm["openDate"]
        self.form['version'] = requestForm["version"]

    def input_validation(self):
        inputError = self.form["inputError"]


        if (DataValidator.isNull(self.form['name'])):
            self.form["error"] = True
            inputError["name"] = "Name can not be null"
        elif (DataValidator.max_len_50(self.form['name'])):
            inputError['name'] = "Name can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['cid'])):
            self.form["error"] = True
            inputError["cid"] = "category can not be null"

        if DataValidator.isNull(self.form['openDate']):
            inputError['openDate'] = "open date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['openDate']):
                inputError[
                    'openDate'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["version"])):
            self.form["error"] = True
            inputError["version"] = "version can not be null"
        elif (DataValidator.max_len_20(self.form['version'])):
            inputError['version'] = "version can should be below 20 digit"
            self.form['error'] = True
        elif (DataValidator.isnumb(self.form['version'])):
            inputError['version'] = "Incorrect version,Id should be number"
            self.form['error'] = True
        else:
            if (DataValidator.is_0(self.form['version'])):
                inputError['version'] = "version can not be 0 or less than 0"
                self.form['error'] = True

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNotNull(self.form["version"])):
            if (DataValidator.max_len_20(self.form['version'])):
                inputError['version'] = "version can should be below 20 digit"
                self.form['error'] = True
            elif (DataValidator.isnumb(self.form['version'])):
                inputError['version'] = "Incorrect version,version should be number"
                self.form['error'] = True
            else:
                if (DataValidator.is_0(self.form['version'])):
                    inputError['version'] = "version can not be 0 or less than 0"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['name'])):
            if (DataValidator.max_len_50(self.form['name'])):
                inputError['name'] = "Name can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['name'])):
                    inputError['name'] = "Name contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['cid'])):
            pass

        if DataValidator.isNotNull(self.form['openDate']):
            if DataValidator.isDate(self.form['openDate']):
                inputError[
                    'openDate'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
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
        res={"mesg":""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Project.objects.last().id
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
            params["name"] = json_request.get("name", None)
            params["cid"] = json_request.get("cid", None)
            params["openDate"] = json_request.get("openDate", None)
            params["version"] = json_request.get("version", None)
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
                res["LastId"] = Project.objects.last().id
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

        print("ORS API Project ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.name = self.form["name"]
        obj.category = preload_list[index]["category"]
        obj.openDate = self.form["openDate"]
        obj.version = self.form["version"]
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
                dup = Project.objects.exclude(id=self.form['id']).filter(name=self.form["name"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Project Name already exists"
                else:
                    r = self.form_to_model(Project())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Project.objects.filter(name=self.form["name"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Project Name already exists"
                else:
                    r = self.form_to_model(Project())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Project
    def get_service(self):
        return ProjectService()
