from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Customer
from service.service.CustomerService import CustomerService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class CustomerCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'cid': 1, 'importance': "High"},
            {'cid': 2, 'importance': "Medium"},
            {'cid': 3, 'importance': "Low"},

        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['clientName'] = requestForm['clientName']
        self.form['cid'] = requestForm["cid"]
        self.form['location'] = requestForm["location"]
        self.form['contactNumber'] = requestForm["contactNumber"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form['clientName'])):
            self.form["error"] = True
            inputError["clientName"] = "clientName can not be null"
        elif (DataValidator.max_len_50(self.form['clientName'])):
            inputError['clientName'] = "clientName can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['clientName'])):
                inputError['clientName'] = "clientName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['cid'])):
            self.form["error"] = True
            inputError["cid"] = "importance can not be null"

        if (DataValidator.isNull(self.form['location'])):
            self.form["error"] = True
            inputError["location"] = "location can not be null"
        elif (DataValidator.max_len_50(self.form['location'])):
            inputError['location'] = "location can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['location'])):
                inputError['location'] = "location contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['contactNumber'])):
            self.form["error"] = True
            inputError["contactNumber"] = "contactNumber can not be null"
        elif (DataValidator.ismobilecheck(self.form['contactNumber'])):
            inputError['contactNumber'] = "contactNumber can should be start with 9,8,7,6 digit and 10 digit max"
            self.form['error'] = True
        else:
            if (DataValidator.max_len_10(self.form['contactNumber'])):
                inputError['contactNumber'] = "contactNumber can be only 10 digit"
                self.form['error'] = True


        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNotNull(self.form["contactNumber"])):
            if (DataValidator.max_len_10(self.form['contactNumber'])):
                inputError['contactNumber'] = "contactNumber can should be below 10 digit"
                self.form['error'] = True
            else:
                if (DataValidator.ismobilecheck(self.form['contactNumber'])):
                    inputError['contactNumber'] = "contactNumber can should be start with 9,8,7,6 digit"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['clientName'])):
            if (DataValidator.max_len_50(self.form['clientName'])):
                inputError['clientName'] = "clientName can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['clientName'])):
                    inputError['clientName'] = "clientName contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['cid'])):
            pass

        if (DataValidator.isNotNull(self.form['location'])):
            if (DataValidator.max_len_50(self.form['location'])):
                inputError['location'] = "location can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['location'])):
                    inputError['location'] = "location contains only letters"
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
            params["clientName"] = json_request.get("clientName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Customer.objects.last().id
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
            params["clientName"] = json_request.get("clientName", None)
            params["cid"] = json_request.get("cid", None)
            params["location"] = json_request.get("location", None)
            params["contactNumber"] = json_request.get("contactNumber", None)
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
                res["LastId"] = Customer.objects.last().id
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

        print("ORS API Customer ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.clientName = self.form["clientName"]
        obj.importance = preload_list[index]["importance"]
        obj.location = self.form["location"]
        obj.contactNumber = self.form["contactNumber"]
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
                dup = Customer.objects.exclude(id=self.form['id']).filter(contactNumber=self.form["contactNumber"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "contactNumber already exists"
                else:
                    r = self.form_to_model(Customer())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Customer.objects.filter(contactNumber=self.form["contactNumber"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "contactNumber  already exists"
                else:
                    r = self.form_to_model(Customer())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Customer
    def get_service(self):
        return CustomerService()
