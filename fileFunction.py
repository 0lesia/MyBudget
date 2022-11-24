from datetime import *
from dbFunction import *
import locale

def loadDataFromFile(fileName):
    fh = open(fileName)
    countLine = 0
    create_db()

    for line in fh:

        lineData = line.strip().split(';')
        if len(lineData) < 5 or lineData[0] == 'Date':
            continue

        try:
            dateT = datetime.strptime(lineData[0], '%d.%m.%y')
        except:
            print('Bad date format', lineData[0])
            continue

        try:
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
            amountT = locale.atof(lineData[4].strip(" RUB").replace('\xa0', ''))

        except:
            print('Bad amount format', lineData[4])
            continue

        sourceT = lineData[2]
        categoryT = lineData[3]
        commentT = lineData[1]

        #print(dateT, sourceT, categoryT, amountT, commentT)
        addTransaction(dateT, sourceT, categoryT, amountT, commentT)
        countLine = countLine + 1

    print('Successfully uploaded lines', countLine)