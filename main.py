def mbb_stmnt(df3,i,file1):
    df=df3
    df.columns = df.iloc[1]
    df=df[2:]
    df['NewLine']=df['ENTRY DATE'].isnull()
    df['NewLine_Date']=df['ENTRY DATE'].notnull()
    df.drop(columns=['NewLine'])
    df.loc[df['NewLine_Date'], 'index_my'] = range(1, len(df[(df['NewLine_Date'])]) + 1)
    df.groupby('index_my')['ENTRY DATE'].fillna(method='ffill')
    df['DATE_NEW']=df['ENTRY DATE'].fillna(method='ffill')
    df['INDEX_DATE_NEW']=df['index_my'].fillna(method='ffill')
    df['TRANSACTION DESCRIPTION_combined']=df[df['DATE_NEW'].notnull()].groupby(['INDEX_DATE_NEW'])['TRANSACTION DESCRIPTION'].transform(lambda x: ' '.join(x))
    df1=df[(df['NewLine_Date'])][['ENTRY DATE','TRANSACTION AMOUNT','TRANSACTION DESCRIPTION_combined']]
    df1['AMOUNT']=df1['TRANSACTION AMOUNT'].str[-1]+''+df1['TRANSACTION AMOUNT'].str[:-1]
    df1=df1[['ENTRY DATE','TRANSACTION DESCRIPTION_combined','AMOUNT']]
    df1.to_csv(str(file1)+str(i)+'.csv')
    return df1


import tabula
import pandas as pd
import glob
import os

# Get the current working directory
cwd = os.getcwd()
print("Current working directory: {0}".format(cwd))
print("Current working directory: {0}".format(os.getcwd()))
# Change the current working directory
os.chdir('mbb/')

pdf_files = []
for each_file in glob.glob('*.{}'.format('pdf')):
    file1 = each_file
    table = tabula.read_pdf(file1,pages='all')
    for i in range(0, len(table)):
        mbb_stmnt(table[i],i,file1)


