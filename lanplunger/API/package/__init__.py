#!/usr/bin/env python3
from flask_restful import Resource


class Package(Resource):

    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.dbcur = kwargs['dbcur']

    def get(self, package_id=None):

        sql = """ Select Top 1000000 tblSoftwareUni.SoftID,
                    tblSoftwareUni.SoftwarePublisher,
                    tblSoftwareUni.SoftwareName,
                    tblSoftwareUni.Approved,
                    tblSoftwareUni.OSType,
                    tblSoftwareUni.Added
                  From tblSoftwareUni  
                  where SoftID = ?
        """
        self.dbcur.execute(sql, package_id)
        userdata = self.dbcur.fetchone()
        if userdata is not None:
            return {
                "result": "OK",
                "rc": 0,
                "user": {
                    'SoftwareID': userdata[0],
                    'SoftwarePublisher': userdata[1],
                    'SoftwareName': userdata[2],
                    'Approved': userdata[3],
                    'OSType': userdata[4],
                    'Added': userdata[5],
                }
            }
        else:
            return {"result": "Failed", "package": None, 'rc': 1, "msg": "No package found."}

    @staticmethod
    def put(package_id):
        return {"result": "%s not updated for safety reasons." % package_id, 'rc': 1}

    @staticmethod
    def delete(package_id):
        return {"result": "%s not deleted for safety reasons." % package_id, 'rc': 1}
