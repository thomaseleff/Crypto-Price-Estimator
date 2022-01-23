# --------------------------------------------------
#   Python Utility Module
# --------------------------------------------------
#   Author   : Tom Eleff
#   Version  : 1_1
#   Date     : 04APR21
# --------------------------------------------------

import os

# --------------------------------------------------
# Define Logging Utility Functions
# --------------------------------------------------


def create_log(configDict, revision, date):
    # configDict           : Config Variable Dictionary
    # date                 : Current Date

    # Manage Log File
    if os.path.isfile(configDict['logPath'] + r'\PythonLog.txt'):
        # Delete Log
        os.remove(configDict['logPath'] + r'\PythonLog.txt')

    # Recreate Log
    write_log(configDict,
              '+--------------------------------'
              + '--------------------------------'
              + '--------------------------------'
              + '--------------------------------+ \n')
    write_log(configDict,
              '|                                     '
              + '                CRYPTO PRICE ESTIMATOR'
              + '                                 '
              + '                    | \n')
    write_log(configDict,
              '+--------------------------------'
              + '--------------------------------'
              + '--------------------------------'
              + '--------------------------------+ \n')
    write_log(configDict,
              '    Revision    : [' + revision + '] \n')
    write_log(configDict,
              '    Date        : [' + str(date) + '] \n')


def write_log(configDict, string):
    # configDict           : Config Variable Dictionary
    # string               : String to Output to Log

    with open(configDict['logPath'] + r'\PythonLog.txt', 'a+') as logFile:
        logFile.write(string)
        print(string)


def output_header(configDict, reqName, webURL):
    # configDict           : Config Variable Dictionary
    # reqName              : Provider Agency Name
    # webURL               : Website URL

    write_log(configDict,
              '\n')
    write_log(configDict,
              '\n')
    write_log(configDict,
              '+--------------------------------'
              + '--------------------------------+ \n')
    write_log(configDict,
              '|   ' + reqName
              + ' ' * int(65 - len('|   ' + reqName)) + '| \n')
    write_log(configDict,
              '+--------------------------------'
              + '--------------------------------+ \n')
    if webURL is not None:
        write_log(configDict,
                  '    Info        : ['
                  + webURL + '] \n')


def output_list(configDict, varLst):
    # configDict           : Config Variable Dictionary
    # varLst               : Geography List

    write_log(configDict,
              '\n')
    if len(varLst) == 1:
        write_log(configDict,
                  '        [' + varLst[0] + '] \n')
    elif len(varLst) < 6:
        write_log(configDict,
                  '        ' + str(varLst) + ' \n')
    else:
        for Item in varLst:
            if varLst.index(Item) == 0:
                outputString = Item + ', '
            elif (varLst.index(Item) % 5 == 4 or
                  varLst.index(Item) + 1 == len(varLst)):
                outputString = outputString + Item
            else:
                outputString = outputString + Item + ', '
            if varLst.index(Item) % 5 == 4:
                if varLst.index(Item) == 4:
                    write_log(configDict,
                              '        [' + outputString + '\n')
                elif varLst.index(Item)+1 == len(varLst):
                    write_log(configDict,
                              '        ' + outputString + '] \n')
                else:
                    write_log(configDict,
                              '        ' + outputString + '\n')
                outputString = ' '
            elif varLst.index(Item) + 1 == len(varLst):
                write_log(configDict,
                          '        ' + outputString + '] \n')
                outputString = ' '

# --------------------------------------------------
# Define Config Utility Functions
# --------------------------------------------------


def write_config(configDict, paramDict):
    with open(configDict['logPath'] + '/conf.txt', 'w') as file:
        for key in paramDict:
            val = paramDict[key]
            file.write(key + '|' + str(val) + '\n')


def read_config(configDict):
    global paramDict

    paramDict = {}

    with open(configDict['logPath'] + '/conf.txt', 'r') as file:
        for line in file:
            (key, val) = line.split('|')
            val = str(val).strip('\n')
            try:
                paramDict[key] = int(val)
            except ValueError:
                if val.upper() == 'TRUE':
                    paramDict[key] = True
                elif val.upper() == 'FALSE':
                    paramDict[key] = False
                elif '[' in val.upper():
                    paramDict[key] = [x.strip('\'') for x
                                      in val.strip('[]').split(',')]
                else:
                    paramDict[key] = str(val).strip('\n')

            if paramDict[key] == 'nan':
                write_log(configDict,
                          ('\nERROR: Missing Value Assignment for Config Variable ['+key+'].\
                           Please Provide Correct Value Assignment for ['+key+']\
                           within conf.txt.'))
    print(paramDict)
    return paramDict
