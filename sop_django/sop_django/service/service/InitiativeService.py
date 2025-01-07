from service.models import Initiative
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Initiative business logics
'''


class InitiativeService(BaseService):

    def get_model(self):
        return Initiative

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_initiative where 1=1"
        # val = params.get("number", None)
        # if DataValidator.isNotNull(val):
        #     sql += " and number like '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("----------", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','initiativeName','type','startDate','number','tid')
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
        sql = "select * from sos_initiative where 1!=1"
        val4 = params.get("tid", None)
        val2 = params.get("startDate", None)
        val1 = params.get("initiativeName", None)
        val3 = params.get("number", None)

        print("-----val-->>", val1)

        if DataValidator.isNotNull(val1):
            sql += " or initiativeName =  '" + val1 + "' "

            print("-------sql-->>", sql)

        if DataValidator.isNotNull(val4):
            sql += " or tid = '" + str(val4) + "' "
        if DataValidator.isNotNull(val2):
            sql += " or startDate = '" + val2 + "' "
        # else:
        #     if(DataValidator.isDate(val3)):
        #      sql += " and startDate = '"+val3+"' "
        if DataValidator.isNotNull(val3):
            sql += " or number =  '" + str(val3) + "' "


        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','initiativeName','type','startDate','number','tid')
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
        return Initiative

