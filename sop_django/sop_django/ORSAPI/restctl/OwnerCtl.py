from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Owner
from service.service.OwnerService import OwnerService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class OwnerCtl(BaseCtl):

    def preload(self, request,params={}):
        preloadList = [
            {'did': 1, 'dob': "1995-07-23"},
            {'did': 2, 'dob': "2000-05-12"},
            {'did': 3, 'dob': "2000-05-11"},
            {'did': 4, 'dob': "2000-05-10"},
            {'did': 5, 'dob': "2005-05-09"},
            {'did': 6, 'dob': "2000-05-08"}

        ]

        return JsonResponse({"preloadList":preloadList})

    def preload1(self, request, params={}):
        preloadList =[
            {'vid': 1, 'vehicleId':'23'},
            {'vid': 2, 'vehicleId':'34'},
            {'vid': 3, 'vehicleId':'45'},
            {'vid': 4, 'vehicleId':'56'},
            {'vid': 5, 'vehicleId':'11'}

        ]
        return JsonResponse({"preloadList1": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['name'] = requestForm["name"]
        # self.form['dob'] = requestForm["dob"]
        # self.form['vehicleId'] = requestForm["vehicleId"]
        self.form['insuranceAmount'] = requestForm["insuranceAmount"]
        self.form['did'] = requestForm["did"]
        self.form['vid'] = requestForm["vid"]

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

        if (DataValidator.isNull(self.form['insuranceAmount'])):
            self.form["error"] = True
            inputError["insuranceAmount"] = "insuranceAmount can not be null"
        elif (DataValidator.is_0(self.form['insuranceAmount'])):
            self.form["error"] = True
            inputError["insuranceAmount"] = "insuranceAmount can not be zero or less"
        else:
            if (DataValidator.max_len_10(self.form['insuranceAmount'])):
                inputError['insuranceAmount'] = "insuranceAmount can be only 10 digit"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['vid'])):
            self.form["error"] = True
            inputError["vid"] = "vehicleId can not be null"

        if (DataValidator.isNull(self.form['did'])):
            self.form["error"] = True
            inputError["did"] = "dob  can not be null"

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]


        if (DataValidator.isNotNull(self.form['name'])):
            if (DataValidator.max_len_50(self.form['name'])):
                inputError['name'] = "name can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['name'])):
                    inputError['name'] = "name contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form["insuranceAmount"])):
            if (DataValidator.max_len_10(self.form['insuranceAmount'])):
                inputError['insuranceAmount'] = "insuranceAmount can should be above 10 digit"
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
        json_request = json.loads(request.body)
        if (json_request):
            params["dob"] = json_request.get("dob", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Owner.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        res = {}
        json_request = json.loads(request.body)
        json_request['id'] = 0
        # json_request['pid'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["name"] = json_request.get("name", None)
            params["did"] = json_request.get("did", None)
            params["vid"] = json_request.get("vid", None)
            params["insuranceAmount"] = json_request.get("insuranceAmount", None)

            params["pageNo"] = json_request.get("pageNo", None)
        self.request_to_form(json_request)
        if (self.input_validation1()):
            print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            res["error"] = True
            res["mesg"] = "No record found"
        else:
            c = self.get_service().search1(params)
            # res = {"mesg": ""}
            if (c != None):
                res["data"] = c["data"]
                if res["data"] == []:
                    res["mesg"] = "No record found"
                res["MaxId"] = c["MaxId"]
                res["index"] = c["index"]
                res["LastId"] = Owner.objects.last().id
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
        preload_response = self.preload1(None).content.decode()
        preload_data = json.loads(preload_response)
        preload_list = preload_data["preloadList1"]

        preload_response = self.preload(None).content.decode()
        preload_data = json.loads(preload_response)
        preload_list1 = preload_data["preloadList"]

        index = self.find_dict_index(preload_list, 'vid', self.form['vid'])

        index1 = self.find_dict_index(preload_list1, 'did', self.form['did'])



        print("ORS API Owner ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.dob = preload_list1[index1]['dob']
        obj.name = self.form["name"]
        obj.insuranceAmount = self.form["insuranceAmount"]
        obj.vehicleId = preload_list[index]['vehicleId']
        obj.vid = self.form["vid"]
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
                dup = Owner.objects.exclude(id=self.form['id']).filter(name=self.form["name"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Name already exists"
                else:
                    r = self.form_to_model(Owner())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Owner.objects.filter(name=self.form["name"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Title already exists"
                else:
                    r = self.form_to_model(Owner())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Owner
    def get_service(self):
        return OwnerService()
