from service.models import Position
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Position business logics
'''


class PositionService(BaseService):

    def get_model(self):
        return Position

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_position where 1=1"
        # val = params.get("condition", None)
        # if DataValidator.isNotNull(val):
        #     sql += " and condition like '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("----------", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','designation','openingDate','requiredExperience','condition','cid')
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
        sql = "select * from sos_position where 1!=1"
        val4 = params.get("cid", None)
        val2 = params.get("openingDate", None)
        val1 = params.get("designation", None)
        val3 = params.get("requiredExperience", None)

        print("-----val-->>", val1)

        if DataValidator.isNotNull(val1):
            sql += " or designation like '" + str(val1) + "%%'"
        if DataValidator.isNotNull(val2):
            sql += " or openingDate = '" + str(val2) + "' "
        if DataValidator.isNotNull(val4):
            sql += " or cid = '" + str(val4) + "' "

        if DataValidator.isNotNull(val3):
            sql += " or requiredExperience =  '" + str(val3) + "' "

        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','designation','openingDate','requiredExperience','condition','cid')
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        count = 0
        for x in result:
            # print("--------with column-->>",{columnName[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>", params['MaxId'])
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Position

