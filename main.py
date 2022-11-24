from fileFunction import *

def convertData(strData, strType = 'str'):
    valData = strData

    try:
        if strType == 'date':
            valData = datetime.strptime(strData, '%d.%m.%y')
        elif strType == 'float':
            valData = float(strData)
    except:
        print(f'Bad format for {strType}: ',strData)

    return valData


activity = input('Enter the number of activity (1) - Add data, (2) = Get data:')

if activity == 1:
    file_name = input('Enter file name:')

    if len(file_name) > 0:
        loadDataFromFile(file_name)
else:
    date_from = input('Enter start of period:')
    date_to = input('Enter start of period:')
    aggregateData = input('Enter "y" for aggregate data: ')

    getTransactions(convertData(date_from, 'date'), convertData(date_to, 'date'), aggregateData == 'y')