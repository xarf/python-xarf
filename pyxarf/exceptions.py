'''
:copyright: (c) 2014 by abusix GmbH
:license: Apache2, see LICENSE.txt for more details.

some custom exception handlers

'''

class GeneralError(Exception):
    '''
    default exception class

    '''
    pass

class ValidationError(Exception):
    '''
    gets raised on validation exceptions

    '''
    pass

class MissingParameterError(Exception):
    '''
    gets raised when a parameter is missing

    '''
    def __init__(self, message, missing_parameters):
        '''
        subclassing exception class to pass the missing parameters
        through the exception object to the calling application

        :param message: original error message
        :type message: str
        :param missing_parameters: list of missing parameters
        :type missing_parameters: list

        '''
        Exception.__init__(self, message)
        self.missing_parameters = missing_parameters