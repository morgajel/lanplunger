#!/usr/bin/env python3
from flask_restful import Resource


class Dept(Resource):

    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.dbcur = kwargs['dbcur']

    def get(self, dept_id=None):

        sql = """
            """
        self.dbcur.execute(sql, dept_id)
        deptdata = self.dbcur.fetchone()
        if deptdata is not None:
            return {
                "result": "OK",
                "rc": 0,
                "dept": {
                    'DeptID': deptdata[0],
                    'DeptName': deptdata[1],
                    'DeptDomain': deptdata[2],
                    'Email': deptdata[3],
                    'DisplayName': deptdata[4],
                    'Department': deptdata[5],
                    'Firstname': deptdata[6],
                    'Lastname': deptdata[7]
                }
            }
        else:
            return {"result": "Failed", "dept": None, 'rc': 1, "msg": "No dept found."}

    @staticmethod
    def put(dept_id):
        return {"result": "%s not updated for safety reasons." % dept_id, 'rc': 1}

    @staticmethod
    def delete(dept_id):
        return {"result": "%s not deleted for safety reasons." % dept_id, 'rc': 1}
