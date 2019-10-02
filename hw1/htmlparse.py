from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from datetime import timedelta

from dateutil.parser import parse


def getRowCount(soupTableObj):
    rows = soupTableObj.find_all('tr')

    table_row = 0
    for trow in rows:
        tcols = trow.find_all('td')
        if len(tcols) > 0:
            table_row = table_row + 1
    return table_row

def getColCount(soupTableObj):

    table_cols = 0

    rowList = soupTableObj.find_all('tr')
    for row in rowList:
        myCols = row.find_all('td')
        if table_cols > 0:
            break
        if table_cols == 0:
            table_cols = table_cols + len(myCols)
            print(myCols)
    return table_cols

def getColumnNames(soupTableObj):

    colNames = []
    rowList = soupTableObj.find_all('tr')
    for row in rowList:
        myCols = row.find_all('td')
        thTagList = row.find_all('th')
        if len(thTagList) == len(myCols) and len(colNames) == 0:
            for th in thTagList:
                colNames.append(th.get_text())
        if len(colNames) > 0:
            break
    return colNames


def myRawTableBuilder(soupTableObj):
    myTable = []
    n_columns = getColCount(soupTableObj)
    soupRowList = soupTableObj.find_all('tr')
    for soupRow in soupRowList:
        # Get list of columns
        soupCellList = soupRow.find_all('td')

        # Check that the number of columns is correct
        if n_columns != len(soupCellList):
            print("n_columns=%d, len(soupCellList)=%d" % (n_columns, len(soupCellList)))
            raise Exception("Expected column count does not match acutal column count")

        # Initialize table row
        tableRow = []

        # Fill in row
        for soupCell in soupCellList:
            tableRow.append(soupCell.get_text())

        # Add row to table
        myTable.append(tableRow)

    # Return finished table
    return myTable


# Takes a beautiful soup object of an html table and returns a pandas dataframe of that table
def myDataframeBuilder(soupTableObj):
    # Get table row and column count
    n_rows = getRowCount(soupTableObj)
    n_columns = getColCount(soupTableObj)

    # Get column names
    columnNames = getColumnNames(soupTableObj)

    # Initialize dataframe
    df = pd.DataFrame(columns=columnNames, index=range(0, n_rows))

    # Make table from data cells (assume this is a list of lists)
    table = myRawTableBuilder(soupTableObj)

    # Fill in dataframe
    for i in range(n_rows):
        for j in range(n_columns):
            df.iat[i, j] = table[i][j]

    # Return fully constructed dataframe
    return (df)


def get_temperature(fromMonth, fromDay, fromYear, toMonth, toDay, toYear, station):
    target_url = f"http://www.georgiaweather.net/index.php?variable=HI&site={station}"

    html = requests.post(target_url, data=[('fromMonth', fromMonth),
                                           ('fromDay', fromDay),
                                           ('fromYear', fromYear),
                                           ('toMonth', toMonth),
                                           ('toDay', toDay),
                                           ('toYear', toYear)
                                           ]).text

    soup = BeautifulSoup(html)
    res = soup.find_all('table')

    # Processing
    df = myDataframeBuilder(res[1])
    df = df.iloc[6:, :4]
    df.columns = df.iloc[0]
    df = df.drop(6).reset_index(drop=True)
    df['Max Temperature[&degF]'] = df['Max Temperature[&degF]'].apply(lambda x: float(x))
    df['Min Temperature[&degF]'] = df['Min Temperature[&degF]'].apply(lambda x: float(x))
    df['Rain (in)'] = df['Rain (in)'].apply(lambda x: float(x))

    # Date processing
    datelist = df['Date']
    date_result_list = []
    for idx, datestring in enumerate(datelist):
        date_time = datetime.strptime(datelist[0] + f' {fromYear}', '%b %d %Y') + timedelta(idx)
        date_result_list.append(date_time)
    df['Date'] = pd.Series(date_result_list)

    return df


df = get_temperature('August', 1, 2018, 'August', 30, 2019, 'WATUGA')