import pandas as pd
tst = pd.read_excel('booking202019.xlsx', sheet_name=0, header=None, skiprows=3)
tst = tst.apply(lambda x: x.dropna().reset_index(drop=True), axis=1)

tst = tst.loc[~(tst[0].str.startswith('Booking Report') |
tst[0].str.startswith('By date as per Government Code') |
tst[0].str.startswith('Page') |
tst[0].str.startswith('Booking#')).astype(bool) ]
tst = tst.iloc[:-1,:]


i=0
concat = []
while i < tst.shape[0]:
    if type(tst.iloc[i,0])==str and tst.iloc[i,0].startswith('FJ'):
        suspect_data = tst.iloc[i]
    elif type(tst.iloc[i,0])==str and tst.iloc[i,0].startswith('Booked'):
        booking_data = tst.iloc[i]
    elif tst.iloc[i].notnull().sum()>0:
        row = pd.DataFrame(pd.concat([tst.iloc[i],suspect_data,booking_data],axis=0).reset_index(drop=True)).transpose()
        concat.append(row)
    i += 1
data = pd.concat(concat)
data = data.loc[:,data.notnull().any()]

data.columns = ['Code', 'VC/FC', 'Felony/Misdemeanor', 'Description', 'Other1', 'Other2', 'Other3', 'Other4',
                'Booking#', 'Arrested Date', 'Gender', 'Height', 'Weight', 'Hair', 'Eye', 'Race', 'Other5', 'Other6', 'Other7', 'Other8',
                'Booked Date', 'Release Time', 'Outcome', 'Arresting Officer', 'Location1', 'Location2', 'Location3']

data['Location'] = data.apply(lambda x: f"{x['Location1']} {x['Location2']} {x['Location3'] if type(x['Location3'])==str else ''}".replace("Arrest Location =",""),axis=1)
data['Officer Name'] = data['Arresting Officer'].str.replace('Arresting Officer = ','')

data = data.drop(['Arresting Officer', 'Location1', 'Location2', 'Location3'],axis=1)
data.to_csv('FortBraggBookings.csv',index=False)