"""
Class Name: ErrorCheck
Developed by: Md Muttayem Al Mueem
Reviewed By: Avinash Shetty

"""
from framework.model.utility.sdoLib import SDOLib
from framework import api


class ErrorCheck:
    """
    This is an error detection class, which can detect particular error screen
    """

    def __init__(self, errorCode=None):
        self.errorCode = errorCode
        self.errorText = 'Error' + str(self.errorCode)
        self.sdoLib = SDOLib()
        self.found = None
        self.listOfErrorCodes = [
            'Error100',
            'Error0100',
            'Error101',
            'Error102',
            'Error201',
            'Error204',
            'Error500',
            'Error601',
            'Error11630',
            'Error14700'
        ]

    def errorResult(self):
        """
        This method provide the actual error code and error message on the screen.
        The available error code are Error100/101/102/201/204/500/601/11630/14700
        @return: boolean value True/False
        """
        self.sdoLib.setScreen("errorScreens", screenPath="/MUEEM THESIS/errorScreens")
        self.sdoLib.executeSDO()
        result = self.sdoLib.getResults()
        verifyStatus = False

        if self.errorCode is None:
            for error in self.listOfErrorCodes:
                if result[error] == result['ExpectedText'][error][0]:
                    self.found = error
                    if result['ExpectedText'][self.found + 'Msg'][0] == result[self.found + 'Msg']:
                        verifyStatus = True
                        print('Expected result : ', result['ExpectedText'][self.found][0], '\n', 'Actual result : ',
                              result[self.found], '\n', 'Actual Message : ', result[self.found + 'Msg'])
                        return verifyStatus
        else:
            if self.errorText in self.listOfErrorCodes:
                verifyStatus = True
                print('Expected result : ', result['ExpectedText'][self.errorText][0], '\n', 'Actual result : ',
                      result[self.errorText], '\n', 'Actual Message : ', result[self.errorText + 'Msg'])
                return verifyStatus
            else:
                print('Enter a valid error code. Available error codes are ' + '/'.join(
                    ['{0}'.format(k) for k in self.listOfErrorCodes]))
                return verifyStatus

    @staticmethod
    def getErrorCode():
        """
        This method can provide the actual error code from any error screen
        @return: boolean value True/False, error code
        """
        verifyStatus = False
        errorCodeRect = (3348, 90, 432, 172)
        region = api.ocrRegion("", "errorCode", rect=errorCodeRect, verify=False)
        sdo = api.screenDefinition()
        sdo.Regions.append(region)
        returnSDO = sdo.Match()[0][1]
        resultText = returnSDO.Regions[0].ResultText
        if "Code" in resultText:
            verifyStatus = True
        return verifyStatus, resultText if verifyStatus else "This is not an error screen"
