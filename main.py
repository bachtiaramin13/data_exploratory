import pandas as pd 
import matplotlib.pyplot as plt

data = pd.read_csv('salary.csv', encoding='utf-8')

data['Money'] = data['Salary'].str.slice(start=0,stop=1)
data['Period'] = data['Salary'].str.split("/", n=1, expand=True)[1]
data['Quantity'] = data['Salary'].str.split("/", n=1, expand=True)[0].str.slice(start=1)
data['Quantity'] = data['Quantity'].str.replace(',', '')  
td= data.loc[data["Money"]=="A"].index
df = data.drop(td, axis=0)
df['Quantity'] = df['Quantity'].astype(float)
df['Period'].unique()
df['Quantity'].loc[df['Period']=='mo'] = df['Quantity'] * 12
df['Quantity'].loc[df['Period']=='hr'] = df['Quantity'] * 12 * 40
df['Money'].unique()
df['Quantity'].loc[df['Money']=='₹'] = df['Quantity'] * 0.013
df['Quantity'].loc[df['Money']=='£'] = df['Quantity'] * 1.11
df.loc[df['Salaries Reported'].isna()]

print(df)
print('===========================================================')
print('Introductory Details About Data :')
df.dropna(subset=['Salaries Reported'], inplace=True)
df.loc[df['Company Name'].isna()]
df['Company Name']= df['Company Name'].fillna('Other')
df.info()
print('\n')
df['Quantity'] = df['Quantity'] / df['Salaries Reported']
df.drop(['Salaries Reported','Salary', 'Money', 'Period'], axis=1, inplace=True)
df.head()
print('===========================================================')
print('Statistical Insight :')
print(df.describe())
print('===========================================================')
print('Data Cleaning :')
print(df.isnull().sum())
print('\n')
print(df.dropna(axis=0,inplace=True) )
df['Quantity'].fillna(value=df['Quantity'].mean(), inplace = True)
df.duplicated().sum()  
df.drop_duplicates(inplace=True)
print('===========================================================')
print('Data Visualization :')
df['Field'] = 'Other'
wData =  df['Job Title'].str.contains("Data")
wScience = df['Job Title'].str.contains("Science")
wScientist = df['Job Title'].str.contains("Scientist")
wMachine = df['Job Title'].str.contains("Machine")
wLearning = df['Job Title'].str.contains("Learning")
wEngineer = df['Job Title'].str.contains("Engineer")
wEngineering = df['Job Title'].str.contains("Engineering")
wAnalyst = df['Job Title'].str.contains("Analyst")

df['Field'].loc[wData & (wScience | wScientist) & ~wMachine] = 'Data Science'
df['Field'].loc[wData & (wEngineer | wEngineering)] = 'Data Engineering'
df['Field'].loc[wMachine & wLearning & ~(wData & wScientist)] = 'Machine Learning'
df['Field'].loc[wData & wAnalyst & ~(wMachine | wScientist)] = 'Data Analysis'

df['Level'] = 'Mid'

wJunior =  df['Job Title'].str.contains("Junior")
wTrainee = df['Job Title'].str.contains("Trainee")
wConsultant = df['Job Title'].str.contains("Consultant")
wSenior = df['Job Title'].str.contains("Senior")
wLead = df['Job Title'].str.contains("Lead")
wManager = df['Job Title'].str.contains("Manager")

df['Level'].loc[wJunior | wTrainee] = 'Junior'
df['Level'].loc[wConsultant] = 'Consultant'
df['Level'].loc[wSenior] = 'Senior'
df['Level'].loc[wManager| wLead] = 'Manager'
mean_by_field = df.groupby(['Field'])[['Quantity']].agg('mean').sort_values('Quantity', ascending=True).reset_index()
plt.bar(mean_by_field['Field'], mean_by_field['Quantity'])
plt.xlabel('')
plt.ylabel('Yearly Salary (dollars)')
plt.title('Average Yearly Salary by Field')
plt.xticks(rotation='45')
plt.show()


