#!/usr/bin/env python3
from flask_restful import Resource
from lanplunger import auth,logger

class User(Resource):

    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.dbcur = kwargs['dbcur']
        self.dbcon = kwargs['dbcon']

    @auth.login_required
    def get(self, user_id=None):

        sql = """
                Select Top 1000000 htblusers.UserID,
                  htblusers.UserName,
                  htblusers.UserDomain,
                  htblusers.Email,
                  tblADusers.DisplayName,
                  htblusers.Department,
                  tblADusers.FirstName,
                  tblADusers.LastName

                From htblusers
                  Left Outer Join htblagents On htblusers.userid = htblagents.userid
                  Left Outer Join tblADusers On htblusers.username = tblADusers.Username
                where htblusers.UserName <> ''
        """

        if user_id is None:
            self.dbcur.execute(sql)
        else:
            sql += 'and htblusers.UserID = ?'
            self.dbcur.execute(sql, user_id) 

        userrows = self.dbcur.fetchall()
        columns = [column[0] for column in self.dbcur.description]

        if userrows is not None:
            users = {'users': [], 'result': 'OK', 'rc': 0, 'count': len(userrows)}
            for userdata in userrows:
                user = {}
                for i in range(len(columns)):
                    columnname = columns[i]
                    user[columnname] = userdata[i]
                users['users'].append(user)
            return users
        else:
            return {"result": "Failed", "user": None, 'rc': 1, "msg": "No user found."}
        

    @staticmethod
    def put(user_id):
        return {"result": "%s not updated for safety reasons." % user_id, 'rc': 1}

    @staticmethod
    def delete(user_id):
        return {"result": "%s not deleted for safety reasons." % user_id, 'rc': 1}
