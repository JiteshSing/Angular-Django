from service.models import Project
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Project business logics
'''


class ProjectService(BaseService):

    def get_model(self):
        return Project

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_Project where 1=1"
        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            sql += " and name = '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("----------", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'name', 'category', 'openDate', 'version','cid')
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
        sql = "select * from sos_Project where 1!=1"
        val1 = params.get("name", None)
        val2 = params.get("cid", None)
        val3 = params.get("openDate", None)
        val4 = params.get("version", None)

        print("-----val-->>", val1)

        if DataValidator.isNotNull(val1):
            sql += " or name like  '" + val1 + "%%' "

            print("-------sql-->>", sql)

        if DataValidator.isNotNull(val2):
            sql += " or cid = '" + str(val2) + "' "
        if DataValidator.isNotNull(val3):
            sql += " or openDate = '" + val3 + "' "
        # else:
        #     if(DataValidator.isDate(val3)):
        #      sql += " and date = '"+val3+"' "
        if DataValidator.isNotNull(val4):
            sql += " or version like  '" + val4 + "%%' "


        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'name', 'category', 'openDate', 'version','cid')
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
        return Project

