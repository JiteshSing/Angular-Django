from service.models import Purchaseorder
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Purchaseorder business logics
'''


class PurchaseorderService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_purchaseorder where 1=1"
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("----------", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'totalQuantity','product', 'orderDate','totalCost','pid')
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        for x in result:
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        print("MMMMMMMMMM", params.get("MaxId"))
        return res

    def search1(self, params):
        pageNo = (params["pageNo"] - 1) * self.pageSize
        print("-------pageNo-->>", pageNo)
        sql = "select * from sos_purchaseorder where 1!=1"
        val1 = params.get("totalQuantity", None)
        val2 = params.get("orderDate", None)
        val3 = params.get("totalCost", None)
        val4 = params.get("pid", None)

        print("-----val-->>", val1)
        if DataValidator.isNotNull(val1):
            sql += " or totalQuantity like '" + str(val1) + "%%'"
        if DataValidator.isNotNull(val2):
            sql += " or orderDate = '" + str(val2) + "' "
        if DataValidator.isNotNull(val3):
            sql += " or totalCost like '" + str(val3) + "%%' "

        if DataValidator.isNotNull(val4):
            sql += " or pid =  '" + str(val4) + "' "


            print("-------sql-->>", sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'totalQuantity','product', 'orderDate','totalCost','pid')
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        for x in result:
            # print("--------with column-->>",{columnName[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>", params['MaxId'])
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Purchaseorder

