# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:43:19 2020

@author: admin
"""

import pandas as pd
from datetime import date

df = pd.read_csv('D:\GitHub\Glassdoor_Jobs\glassdoor_jobs.csv')

# salary cleaning
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided' in x.lower() else 0)

df = df[df['Salary Estimate']!= '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_kd = salary.apply(lambda x:x.replace('K','').replace('$',''))

min_hr = minus_kd.apply(lambda x:x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))

df['average salary'] = (df.min_salary +df.max_salary)/2

# company name
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3],axis=1)

# state names
df['jobs_state'] = df['Location'].apply(lambda x : x.split(',')[1])
df.jobs_state.value_counts()

# same state
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)

# age of company
df['age'] = df.Founded.apply(lambda x: x if x < 1 else int(date.today().year) - x)

skill_dict = {'python_yn' : ['python'],
              'R_yn' : ['r studio','r-studio'],
              'spark' : ['spark'],
              'aws' : ['aws'],
              'excel' : ['excel'],
              'tableau' : ['tableau'],
              'jmp' : ['jmp'],
              'power_bi' :['power bi','powerbi']}

for key,value in skill_dict.items():
    df[key] = df['Job Description'].apply(lambda x : 1 if any(ele in x.lower() for ele in value) else 0)
    print(df[key].value_counts())
    
df.columns

df_out = df.drop(['Unnamed: 0'],axis=1)

df_out.to_csv('D:\GitHub\Glassdoor_Jobs\salary_data_cleaned.csv',index = False)



