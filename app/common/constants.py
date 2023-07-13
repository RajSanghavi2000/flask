import os

APP_NAME = 'microservice-template'

""" APIS """
SAMPLE_API = '/v1/persons'

""" Health check APIS """
APP_READINESS_API = '/k8/readiness'
APP_LIVENESS_API = '/k8/liveness'
APP_TERMINATION_API = '/k8/termination'

""" Logger """
LOG_FOLDER_LOCATION = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'data', 'logs'))
LOG_FILE_LOCATION = '{0}/log'.format(LOG_FOLDER_LOCATION)

ERROR_MSG_TEMPLATE = 'File: {file_name} : {file_line_no} \n Error: {err} \n Error Description: {err_info} \n Traceback: {traceback} \n API: {path} \n Info: {info}'

