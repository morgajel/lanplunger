#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""`main` is the top level module for this application."""

from flask import Flask, render_template, request, jsonify, abort, make_response
import logging
import os
import datetime
import traceback
import pyodbc
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
logger = logging.getLogger(__name__)


from lanplunger.API.user import User
from lanplunger.API.package import Package
from lanplunger.API.asset import Asset
from lanplunger.API.ticket import Ticket
from lanplunger.API.dept import Dept


SQL_HOST = os.environ["SQL_HOST"]
SQL_PORT = os.environ["SQL_PORT"]
SQL_DB = os.environ["SQL_DB"]
SQL_USER = os.environ["SQL_USER"]
SQL_PASS = os.environ["SQL_PASS"]





def create_app():
    myapp = Flask(__name__)
    api = Api(myapp)

    ms_driver = 'ODBC Driver 17 for SQL Server'

    myapp.dbcon = pyodbc.connect(driver=ms_driver,
                                 port=SQL_PORT,
                                 server=SQL_HOST,
                                 uid=SQL_USER,
                                 pwd=SQL_PASS
                                 )
    myapp.dbcur = myapp.dbcon.cursor()

    api.add_resource(User,
                     '/users/<int:user_id>',
                     '/users',
                     endpoint='user',
                     resource_class_kwargs={'dbcur': myapp.dbcur, 'dbcon': myapp.dbcon}
                     )
    api.add_resource(Package,
                     '/pkg/<int:id>',
                     '/pkg',
                     endpoint='pkg',
                     resource_class_kwargs={'dbcur': myapp.dbcur, 'dbcon': myapp.dbcon}
                     )
    api.add_resource(Asset,
                     '/asset/<int:id>',
                     '/asset',
                     endpoint='asset',
                     resource_class_kwargs={'dbcur': myapp.dbcur, 'dbcon': myapp.dbcon}
                     )

    return myapp


app = create_app()


@auth.get_password
def get_password(username):

    if username == 'testuser':
        return 'testuser'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
def index_page():
    """This is the first page anyone sees."""

    return render_template('index.html')


@app.route('/status')
@auth.login_required
def status_page():
    """This is the first page anyone sees."""
    return render_template('status.html')

@app.route('/metrics')
@auth.login_required
def metrics_page():
    """This is the first page anyone sees."""
    return render_template('metrics.html')

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(404)
def page_not_found(error):
    """Return a custom 404 error."""

    print(' =======================')
    print('Exception:', error)
    time = str(datetime.datetime.now())
    return render_template('400.html', request=request, time=time), 404


@app.errorhandler(500)
def page_error(error):
    """Return a custom 500 error. Only hit when debugging is off."""

    print(' =======================')
    print('problem with ', request.url)
    time = str(datetime.datetime.now())
    print('Exception:', error)
    traceback.print_exc()

    return render_template('500.html', request=request, e=error, time=time), 500


if __name__ == '__main__':
    app.run()
