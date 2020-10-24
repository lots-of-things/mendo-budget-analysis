import pandas as pd
filename = 'Ukiah_PD_Arrests_PRA_Request.xlsx'
to_concat = []
tst = pd.read_excel(filename, sheet_name=0, header=None, skiprows=3)
tst = tst.apply(lambda x: x.dropna().reset_index(drop=True), axis=1)
to_concat.append(tst)
for i in range(1,209):
tst = pd.read_excel(filename, sheet_name=i, header=None)
tst = tst.apply(lambda x: x.dropna().reset_index(drop=True), axis=1)
to_concat.append(tst)

data = pd.concat(to_concat).reset_index(drop=True)

i=0
case_number = data.iloc[0][0]
suspect_number = 0
case_number_list = []
suspect_number_list = []
while i < data.shape[0]:
    # if data.iloc[i][0]=='SUSPECT':
    if isinstance(data.iloc[i][0],str) and '-' in data.iloc[i][0]:
        case_number = data.iloc[i][0]
        suspect_number = 0
    if isinstance(data.iloc[i][0],str) and data.iloc[i][0]=='SUSPECT':
        suspect_number += 1
    case_number_list.append(case_number)
    suspect_number_list.append(suspect_number)
    i += 1

data['case_number']=case_number_list
data['suspect_number']=suspect_number_list
output_data = data.loc[data[1].notnull()]
missing_fm = data[3].isnull()
output_data.loc[missing_fm,3]=output_data.loc[missing_fm,2]
output_data.loc[missing_fm,2]=output_data.loc[missing_fm,1]
output_data.loc[missing_fm,1]=None
output_data.columns = ['Charge', 'Felony/Misdemeanor', 'Age', 'Race', 'Case Number', 'Suspect Number']
output_data.to_csv('Ukiah_PD_Arrests_cleaned.csv',index=None)