from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Market
from service.service.MarketService import MarketService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class MarketCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'oid': 1, 'orderType': "Market"},
            {'oid': 2, 'orderType': "Limit"},
            

        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['quantity'] = requestForm['quantity']
        self.form['oid'] = requestForm["oid"]
        self.form['purchaseDate'] = requestForm["purchaseDate"]
        self.form['purchasePrice'] = requestForm["purchasePrice"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form['quantity'])):
            self.form["error"] = True
            inputError["quantity"] = "quantity can not be null"
        elif (DataValidator.max_len_20(self.form['quantity'])):
            inputError['quantity'] = "quantity can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isnumb(self.form['quantity'])):
                inputError['quantity'] = "quantity contains only number"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['oid'])):
            self.form["error"] = True
            inputError["oid"] = "orderType can not be null"

        if DataValidator.isNull(self.form['purchaseDate']):
            inputError['purchaseDate'] = "purchaseDate can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['purchaseDate']):
                inputError[
                    'purchaseDate'] = "Incorrect Date format, should be DD-MM-YYYY format and purchaseDate should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['purchasePrice'])):
            self.form["error"] = True
            inputError["purchasePrice"] = "purchasePrice can not be null"
        elif (DataValidator.isflt(self.form['purchasePrice'])):
            inputError['purchasePrice'] = "purchasePrice can should be float digit decimal"
            self.form['error'] = True
        elif (DataValidator.max_len_5(self.form['purchasePrice'])):
            inputError['purchasePrice'] = "purchasePrice can should be below 6 digit"
            self.form['error'] = True
        else:
            if  (DataValidator.validate_two_decimal(self.form['purchasePrice'])):
             inputError['purchasePrice'] = "purchasePrice can should be upto 2 decimal places"
             self.form['error'] = True


        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNotNull(self.form["purchasePrice"])):
            if (DataValidator.max_len_5(self.form['purchasePrice'])):
                inputError['purchasePrice'] = "purchasePrice can should be below 5 digit"
                self.form['error'] = True
            elif (DataValidator.validate_two_decimal(self.form['purchasePrice'])):
                 inputError['purchasePrice'] = "purchasePrice can should be upto 2 decimal places"
                 self.form['error'] = True
            else:
                if (DataValidator.isflt(self.form['purchasePrice'])):
                    inputError['purchasePrice'] = "purchasePrice can should be upto 2 digit"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['quantity'])):
            if (DataValidator.max_len_50(self.form['quantity'])):
                inputError['quantity'] = "quantity can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isnumb(self.form['quantity'])):
                    inputError['quantity'] = "quantity contains only digit"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['oid'])):
            pass

        if DataValidator.isNotNull(self.form['purchaseDate']):
            if DataValidator.isDate(self.form['purchaseDate']):
                inputError[
                    'purchaseDate'] = "Incorrect Date format, should be DD-MM-YYYY format and purchaseDate should in past or present"
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
            res["LastId"] = Market.objects.last().id
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
            params["purchaseDate"] = json_request.get("purchaseDate", None)
            params["purchasePrice"] = json_request.get("purchasePrice", None)
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
                res["LastId"] = Market.objects.last().id
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

        print("ORS API Market ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.quantity = self.form["quantity"]
        obj.orderType = preload_list[index]["orderType"]
        obj.purchaseDate = self.form["purchaseDate"]
        obj.purchasePrice = self.form["purchasePrice"]
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
                dup = Market.objects.exclude(id=self.form['id']).filter(purchasePrice=self.form["purchasePrice"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Mobile number already exists"
                else:
                    r = self.form_to_model(Market())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Market.objects.filter(purchasePrice=self.form["purchasePrice"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Mobile number already exists"
                else:
                    r = self.form_to_model(Market())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Market
    def get_service(self):
        return MarketService()
