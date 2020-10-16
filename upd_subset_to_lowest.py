import pandas as pd

# LOAD DATA AND CODE TABLE
data = pd.read_excel('UkiahDataOAG.xlsx')

data['Case_Number_Person'] = data['Case Number'] + ' ' + data['Age'].astype(str) + ' ' + data['Race']

# TAKE ONLY THE ROW WITH THE LOWEST SUM CODE
subset_tst = data.loc[data.groupby('Case_Number_Person')['Hierarchy'].idxmin()]

# MAKE SURE 1 OUTPUT PER BOOKING
assert subset_tst.shape[0]==data['Case_Number_Person'].unique().shape[0]

# SAVE TO FILE
subset_tst.to_csv('UkiahDataOAG_subset_worst_offense.csv',index=False)
