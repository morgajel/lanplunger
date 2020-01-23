#!/usr/bin/env python3
from flask_restful import Resource


class Ticket(Resource):

    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.dbcur = kwargs['dbcur']

    def get(self, ticket_id=None):

        sql = """ 
        """
        self.dbcur.execute(sql, ticket_id)
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
            return {"result": "Failed", "ticket": None, 'rc': 1, "msg": "No ticket found."}

    @staticmethod
    def put(ticket_id):
        return {"result": "%s not updated for safety reasons." % ticket_id, 'rc': 1}

    @staticmethod
    def delete(ticket_id):
        return {"result": "%s not deleted for safety reasons." % ticket_id, 'rc': 1}
