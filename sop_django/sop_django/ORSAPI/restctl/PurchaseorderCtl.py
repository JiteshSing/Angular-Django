from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Purchaseorder
from service.service.PurchaseorderService import PurchaseorderService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class PurchaseorderCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'pid': 1, 'product': "Mobile"},
            {'pid': 2, 'product': "Tablet"},
            {'pid': 3, 'product': "Charger"},
            {'pid': 4, 'product': "Laptop"},

        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['totalQuantity'] = requestForm["totalQuantity"]
        self.form['pid'] = requestForm["pid"]
        self.form['orderDate'] = requestForm["orderDate"]
        self.form['totalCost'] = requestForm["totalCost"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form["totalQuantity"])):
            self.form["error"] = True
            inputError["totalQuantity"] = "totalQuantity can not be null"
        elif (DataValidator.max_len_20(self.form['totalQuantity'])):
            inputError['totalQuantity'] = "totalQuantity can should be below 20 digit"
            self.form['error'] = True
        elif (DataValidator.isnumb(self.form['totalQuantity'])):
            inputError['totalQuantity'] = "Incorrect,totalQuantity should be number"
            self.form['error'] = True
        else:
            if (DataValidator.is_0(self.form['totalQuantity'])):
                inputError['totalQuantity'] = "totalQuantity can not be 0 or less than 0"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['pid'])):
            self.form["error"] = True
            inputError["pid"] = "Product can not be null"

        if DataValidator.isNull(self.form['orderDate']):
            inputError['orderDate'] = "Date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['orderDate']):
                inputError[
                    'orderDate'] = "Incorrect Date format, should be DD-MM-YYYY format and orderDate should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["totalCost"])):
            self.form["error"] = True
            inputError["totalCost"] = "totalCost can not be null"
        elif (DataValidator.max_len_20(self.form['totalCost'])):
            inputError['totalCost'] = "totalCost can should be below 20 digit"
            self.form['error'] = True
        elif (DataValidator.isnumb(self.form['totalCost'])):
            inputError['totalCost'] = "Incorrect,totalCost should be number"
            self.form['error'] = True
        else:
            if (DataValidator.is_0(self.form['totalCost'])):
                inputError['totalCost'] = "totalCost can not be 0 or less than 0"
                self.form['error'] = True

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNotNull(self.form["totalQuantity"])):
            if (DataValidator.max_len_20(self.form['totalQuantity'])):
                inputError['totalQuantity'] = "totalQuantity can should be below 20 digit"
                self.form['error'] = True
            elif (DataValidator.isnumb(self.form['totalQuantity'])):
                inputError['totalQuantity'] = "Incorrect, totalQuantity should be number"
                self.form['error'] = True
            else:
                if (DataValidator.is_0(self.form['totalQuantity'])):
                    inputError['totalQuantity'] = "totalQuantity can not be 0 or less than 0"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['pid'])):
            pass

        if DataValidator.isNotNull(self.form['orderDate']):
            if DataValidator.isDate(self.form['orderDate']):
                inputError[
                    'orderDate'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form["totalCost"])):
            if (DataValidator.max_len_20(self.form['totalCost'])):
                inputError['totalCost'] = "totalCost can should be below 20 digit"
                self.form['error'] = True
            elif (DataValidator.isnumb(self.form['totalCost'])):
                inputError['totalCost'] = "Incorrect, totalCost should be number"
                self.form['error'] = True
            else:
                if (DataValidator.is_0(self.form['totalCost'])):
                    inputError['totalCost'] = "totalCost can not be 0 or less than 0"
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
            params["orderDate"] = json_request.get("orderDate", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Purchaseorder.objects.last().id
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
            params["totalQuantity"] = json_request.get("totalQuantity", None)
            params["pid"] = json_request.get("pid", None)
            params["orderDate"] = json_request.get("orderDate", None)
            params["totalCost"] = json_request.get("totalCost", None)
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
                res["LastId"] = Purchaseorder.objects.last().id
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

        index = self.find_dict_index(preload_list, 'pid', self.form['pid'])

        print("ORS API Purchaseorder ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.totalQuantity = self.form["totalQuantity"]
        obj.product = preload_list[index]["product"]
        obj.orderDate = self.form["orderDate"]
        obj.totalCost = self.form["totalCost"]
        obj.pid = self.form["pid"]
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
                dup = Purchaseorder.objects.exclude(id=self.form['id']).filter(orderDate=self.form["orderDate"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "orderDate already exists"
                else:
                    r = self.form_to_model(Purchaseorder())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Update orderDated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Purchaseorder.objects.filter(orderDate=self.form["orderDate"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "orderDate already exists"
                else:
                    r = self.form_to_model(Purchaseorder())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Purchaseorder
    def get_service(self):
        return PurchaseorderService()
