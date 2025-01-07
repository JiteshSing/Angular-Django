from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Order
from service.service.OrderService import OrderService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class OrderCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'oid': 1, 'product': "cloths"},
            {'oid': 2, 'product': "books"},
            {'oid': 3, 'product': "food"},

        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['quantity'] = requestForm['quantity']
        self.form['oid'] = requestForm["oid"]
        self.form['date'] = requestForm["date"]
        self.form['amount'] = requestForm["amount"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form['quantity'])):
            self.form["error"] = True
            inputError["quantity"] = "quantity can not be null"
        else:
            if (DataValidator.max_len_10(self.form['quantity'])):
                inputError['quantity'] = "quantity can be only 10 digit"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['oid'])):
            self.form["error"] = True
            inputError["oid"] = "product can not be null"

        if DataValidator.isNull(self.form['date']):
            inputError['date'] = "date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['date']):
                inputError[
                    'date'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['amount'])):
            self.form["error"] = True
            inputError["amount"] = "amount can not be null"
        
        else:
            if (DataValidator.max_len_10(self.form['amount'])):
                inputError['amount'] = "amount can be only 10 digit"
                self.form['error'] = True

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNotNull(self.form["amount"])):
            if (DataValidator.max_len_10(self.form['amount'])):
                inputError['amount'] = "amount can should be below 10 digit"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form["quantity"])):
            if (DataValidator.max_len_10(self.form['quantity'])):
                inputError['quantity'] = "quantity can should be below 10 digit"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form['oid'])):
            pass

        if DataValidator.isNotNull(self.form['date']):
            if DataValidator.isDate(self.form['date']):
                inputError[
                    'date'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
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
            params["quantity"] = json_request.get("quantity", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Order.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        json_request = json.loads(request.body)
        json_request['id'] = 0
        # json_request['oid'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["quantity"] = json_request.get("quantity", None)
            params["oid"] = json_request.get("oid", None)
            params["date"] = json_request.get("date", None)
            params["amount"] = json_request.get("amount", None)
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
                res["LastId"] = Order.objects.last().id
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

        index = self.find_dict_index(preload_list, 'oid', self.form['oid'])

        print("ORS API Order ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.quantity = self.form["quantity"]
        obj.product = preload_list[index]["product"]
        obj.date = self.form["date"]
        obj.amount = self.form["amount"]
        obj.oid = self.form["oid"]
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
                dup = Order.objects.exclude(id=self.form['id']).filter(quantity=self.form["quantity"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Order Name already exists"
                else:
                    r = self.form_to_model(Order())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Order.objects.filter(quantity=self.form["quantity"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Order Name already exists"
                else:
                    r = self.form_to_model(Order())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Order
    def get_service(self):
        return OrderService()
