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



"""The Python function mbb_stmnt takes three parameters: df3, i, and file1. Here’s a step-by-step explanation of what the function does:
It starts by creating a copy of the dataframe df3 into df.
It sets the dataframe’s column names to the values of the second row (df.iloc[1]).
It then trims the first two rows from the dataframe.
Two new columns are created:
NewLine: A boolean column where each value is True if the corresponding ENTRY DATE is null, otherwise False.
NewLine_Date: A boolean column where each value is True if the corresponding ENTRY DATE is not null, otherwise False.
The NewLine column is dropped from the dataframe (although this line doesn’t actually affect df because the drop method isn’t used with inplace=True or reassigned to df).
A new column index_my is created to enumerate the rows where NewLine_Date is True.
The ENTRY DATE column is forward-filled within each group defined by index_my (although this line doesn’t actually affect df because the result isn’t assigned back to df).
Two new columns are created by forward-filling the ENTRY DATE and index_my columns:
DATE_NEW: Forward-filled ENTRY DATE.
INDEX_DATE_NEW: Forward-filled index_my.
A new column TRANSACTION DESCRIPTION_combined is created by concatenating all TRANSACTION DESCRIPTION values within each group defined by INDEX_DATE_NEW.
A new dataframe df1 is created with only the rows where NewLine_Date is True and only the columns ENTRY DATE, TRANSACTION AMOUNT, and TRANSACTION DESCRIPTION_combined.
A new column AMOUNT is created in df1 by appending the last character of TRANSACTION AMOUNT to the front of the rest of the string.
The dataframe df1 is then trimmed to only include the columns ENTRY DATE, TRANSACTION DESCRIPTION_combined, and AMOUNT.
Finally, df1 is saved to a CSV file named with the file1 and i parameters, and df1 is returned.

Here’s a breakdown of what each part of the script does:

Import necessary libraries: The script imports tabula, pandas, glob, and os libraries. tabula is used for extracting tables from PDFs, pandas for data manipulation, glob for file pathnames matching, and os for operating system dependent functionality.
Get the current working directory: It prints the current working directory using os.getcwd().
Change the current working directory: The script changes the current working directory to a subdirectory named ‘mbb/’.
Find all PDF files: It uses glob.glob to find all files in the current directory with a .pdf extension and stores them in the pdf_files list.
Process each PDF file: For each PDF file found, it does the following:
Reads tables from the PDF using tabula.read_pdf.
Iterates over each table extracted from the PDF.
Calls the mbb_stmnt function for each table, passing the table, the index of the table within the PDF, and the filename as arguments.

"""
