from service.models import Task
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Task business logics
'''


class TaskService(BaseService):

    def get_model(self):
        return Task

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_task where 1=1"
        # val = params.get("assignedTo", None)
        # if DataValidator.isNotNull(val):
        #     sql += " and assignedTo like '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("----------", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','taskTitle','details','creationDate','assignedTo','taskStatus','aid','tid')
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
        sql = "select * from sos_task where 1!=1"
        val5 = params.get("tid", None)
        val3 = params.get("creationDate", None)
        val2 = params.get("taskTitle", None)
        val4 = params.get("aid", None)
        val1 = params.get("details",None)

        print("-----val-->>", val1)

        if DataValidator.isNotNull(val2):
            sql += " or taskTitle =  '" + val2 + "' "

            print("-------sql-->>", sql)

        if DataValidator.isNotNull(val4):
            sql += " or aid = '" + str(val4) + "' "
        if DataValidator.isNotNull(val3):
            sql += " or creationDate = '" + val3 + "' "

        if DataValidator.isNotNull(val1):
            sql += " or details =  '" + val1 + "' "
        if DataValidator.isNotNull(val5):
            sql += " or tid =  '" + str(val5) + "' "


        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','taskTitle','details','creationDate','assignedTo','taskStatus','aid','tid')
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
        return Task

