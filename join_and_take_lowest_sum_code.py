import pandas as pd

# LOAD DATA AND CODE TABLE
data = pd.read_csv('fbpd_19_cleaned.csv')
codes = pd.read_csv('le_code.csv')

# REFORMAT CODE TABLE TO MATCH DATA
codes['code_section_cleaned']=codes['Code\n Section'].str.replace(' ','')
codes['Sum_Code']=codes['Sum\n Code']
codes['Offense_Level']=codes['Off\nLevel']

# TAKE ONY THE LOWEST SUM CODE FOR EACH CODE
codes_clean = codes[['code_section_cleaned', 'Offense_Level','Sum_Code']].drop_duplicates().dropna()
codes_clean = codes_clean.loc[codes_clean.groupby(['code_section_cleaned','Offense_Level'])['Sum_Code'].idxmin()]

# SOME DATA CLEANUP
data.loc[(data['Code']=='853.7'),'Felony/Misdemeanor']='M'
data.loc[(data['Code']=='23152(A)'),'Felony/Misdemeanor']='M'
data.loc[(data['Code']=='12022.1'),'Felony/Misdemeanor']='F'

# JOIN DATA AND CODES
tst = data.merge(codes_clean, left_on=['Code','Felony/Misdemeanor'], right_on=['code_section_cleaned','Offense_Level'], how='left')
# SUBSET ONLY WHEN THE SUM CODE IS PRESENT
tst.loc[tst['Sum_Code'].isnull(),'Sum_Code'] = -1

def sum_code_fix(x):
    if x['Felony/Misdemeanor']=='I':
        return 99
    if x['Felony/Misdemeanor']=='F':
        if x['Code']=='273.5':
            return 6
        if x['Code']=='666':
            return 9
        if x['Code'] in ['1203.2','1203.2(A)','12022.1']:
            return 28
    if x['Felony/Misdemeanor']=='M':
        if x['Code']=='1203.2(A)':
            return 67
        if x['Code'] in ['23578', '23540']:
            return 51
        if x['Code'] in ['20002','20002(A)']:
            return 52
        if x['Code'] in ['484','484(A)/488','666/484(A)','666/484','6646/484']:
            return 31
        if x['Code']=='11550':
            return 36
        if x['Code']=='23103':
            return 53
        if x['Code']=='6081':
            return 60
        if x['Code'].startswith('9.68.') or x['Code'].startswith('09.68.') or (x['Code']=='1170.12'):
            return 100
    return x['Sum_Code']


tst['Sum_Code_Fix'] = tst.apply(sum_code_fix, axis=1)

# TAKE ONLY THE ROW WITH THE LOWEST SUM CODE
subset_tst = tst.loc[tst.groupby('Booking#')['Sum_Code_Fix'].idxmin()]

# MAKE SURE 1 OUTPUT PER BOOKING
assert subset_tst.shape[0]==tst['Booking#'].unique().shape[0]

# SAVE TO FILE
subset_tst.to_csv('fbpd_19_subset_worst_offense.csv',index=False)


# BELOW WAS NEEDED TO HELP THINGS
only_one = (tst.groupby('Booking#').size()).reset_index()
only_one = only_one.loc[only_one[0]==1,'Booking#']

# ALSO TAKE ANY WHERE THERE's A SINGLE CHARGE
usable = (subset_tst['Sum_Code_Fix']!=-1) | subset_tst['Booking#'].isin(only_one)
subset_tst = subset_tst.loc[usable]

special_attention = tst.loc[~tst['Booking#'].isin(subset_tst['Booking#'])]
special_attention = special_attention.loc[special_attention['Sum_Code_Fix']==-1]

special_attention.to_csv('fbpd_19_special_attention.csv',index=False)

cheap = tst
cheap.loc[cheap['Sum_Code_Fix']==-1,'Sum_Code_Fix']=1000
cheap_tst = cheap.loc[cheap.groupby('Booking#')['Sum_Code_Fix'].idxmin()]
