# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 16:14:14 2022

@author: kshah23
"""

# using flask_restful
from flask import Flask, send_file
from flask_restful import Resource, Api
import finalysis_task
  
# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

class no_op(Resource):
    def get(self, date):
        finalysis_task.corr_matrix_cal(date, 'csv')
        return send_file('iss_aapl_correlation_matrix.csv')
  
# another resource to calculate the square of a number
class get_matrix(Resource):
    def get(self, date, output_mode="csv"):
        finalysis_task.corr_matrix_cal(date, output_mode)
        if(output_mode=='html'):
            return send_file('iss_aapl_correlation_matrix.html')
        else:
            return send_file('iss_aapl_correlation_matrix.csv')
  
  
# adding the defined resources along with their corresponding urls
api.add_resource(no_op, '/<string:date>/')
api.add_resource(get_matrix, '/<string:date>/<string:output_mode>')
  
  
# driver function
if __name__ == '__main__':
    app.run(debug = True)