# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 12:11:27 2021

@author: Dell
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from functools import reduce


xlsx = pd.ExcelFile('Masked_dataset.xlsx')
all_batteries = pd.read_excel(xlsx,'All Batteries')
pd_demographics=pd.read_excel(xlsx,'PD_Demographics')
mdt_workflow= pd.read_excel(xlsx,'MDT_Workflow')
et_motor= pd.read_excel(xlsx,'ET_Motor')
pd_postop_outcomes= pd.read_excel(xlsx,'PD_Postop_outcomes')
all_physio_outcomes= pd.read_excel(xlsx,'All_Physio_outcomes')
neuropsych_outcomes= pd.read_excel(xlsx,'Neuropsych_outcomes')

all_batteries.drop_duplicates(subset=['MRN'],keep='last',inplace=True)
pd_demographics.drop_duplicates(subset=['Mater MRN'],keep='last',inplace=True)
mdt_workflow.drop_duplicates(subset=['MMUH MRN'],keep='last',inplace=True)
et_motor.drop_duplicates(subset=['MRN'],keep='last',inplace=True)
pd_postop_outcomes.drop_duplicates(subset=['MMUH MRN'],keep='last',inplace=True)
all_physio_outcomes.drop_duplicates(subset=['MRN'],keep='last',inplace=True)
neuropsych_outcomes.drop_duplicates(subset=['MRN'],keep='last',inplace=True)

all_batteries.rename({'MMUH MRN':'MRN'},axis=1,inplace=True)
all_batteries.rename({'Unnamed: 7':'Comments'},axis=1,inplace=True)
pd_demographics.rename({'Mater MRN':'MRN'},axis=1,inplace=True)
mdt_workflow.rename({'MMUH MRN':'MRN'},axis=1,inplace=True)
et_motor.rename({'MMUH MRN':'MRN'},axis=1,inplace=True)
pd_postop_outcomes.rename({'MMUH MRN':'MRN'},axis=1,inplace=True)

# all_batteries.drop('Unnamed: 0')
# pd_demographics.drop('Unnamed: 0')
# mdt_workflow.drop('Unnamed: 0')
# et_motor.drop('Unnamed: 0')
# pd_postop_outcomes.drop('Unnamed: 0')
# all_physio_outcomes.drop('Unnamed: 0')
# neuropsych_outcomes.drop('Unnamed: 0')

# all_batteries.set_index(['MRN'],inplace=True)
# pd_demographics.set_index(['MRN'],inplace=True)
# mdt_workflow.set_index(['MRN'],inplace=True)
# et_motor.set_index(['MRN'],inplace=True)
# pd_postop_outcomes.set_index(['MRN'],inplace=True)
# all_physio_outcomes.set_index(['MRN'],inplace=True)
# neuropsych_outcomes.set_index(['MRN'],inplace=True)

frames=[all_batteries,pd_demographics,mdt_workflow,et_motor,pd_postop_outcomes,all_physio_outcomes,neuropsych_outcomes]
m1=all_batteries.merge(pd_demographics, left_on='MRN', right_on='MRN',suffixes=['_battery','_pd_demographics'],how='outer')
m2=m1.merge(mdt_workflow, left_on='MRN', right_on='MRN',suffixes=['_battery','_mdt'],how='outer')
m3=m2.merge(et_motor, left_on='MRN', right_on='MRN',suffixes=['_battery','_motor'],how='outer')
m4=m3.merge(pd_postop_outcomes, left_on='MRN', right_on='MRN',suffixes=['_battery','_PD_postop'],how='outer')
m5=m4.merge(all_physio_outcomes, left_on='MRN', right_on='MRN',suffixes=['_battery','_physio'],how='outer')
m6=m5.merge(neuropsych_outcomes, left_on='MRN', right_on='MRN',suffixes=['_battery','_neuro'],how='outer')
m6.sort_values(by = 'MRN',inplace=True)
del m1
del m2
del m3
del m4
del  m5
m6 = m6.loc[:,~m6.columns.duplicated()]
m6.replace(np.nan, 'Not available',inplace=True)
m6.reset_index(drop=True,inplace=True)
pd.options.display.float_format = "{:,.2f}".format
#%% 
'Streamlit Design'
st.header("Individual Patient Information Visualisation")
st.write("This application shows the data of one individual patient based on the MRN Number given by the user.")
st.subheader(" School of Electronics Engineering, University College Dublin and The Mater Misericordiae University Hospital")
st.warning("Security Warning.")
password=st.sidebar.text_input("Please enter the password :", "password")
if password=='MaterUCD':
    
    mrn = st.sidebar.text_input("Enter the MRN no of the patient:", "0019")
    mrn=int(mrn)
    if mrn in m6.MRN:
        st.success("MRN has been found")
        n=m6.index[m6['MRN'] == mrn]
        n=n[0]
        Patient_demographic_details=st.sidebar.checkbox("Patient Demographic Details")
        Patient_contact_details=st.sidebar.checkbox("Patient Contact Details")
        MDT_Workflow_details=st.sidebar.checkbox("MDT Work up")
        ET_Motor_details=st.sidebar.checkbox("ET Motor Workup")
        PD_Postop_details=st.sidebar.checkbox("PD Post-op Outcomes")
        Physio_details=st.sidebar.checkbox("Physio Outcomes")
        Neuro_details=st.sidebar.checkbox("Neuro Outcomes")
        st.subheader('Patient Details')
        st.write('Information from sheet all batteries, use patient no 22')
        st.write('Name: John/Jane Doe')
        st.write('Age: '+str(m6.iloc[n]['Age'])+' Date of Birth:'+str(m6.iloc[n]['DOB_battery']))
        st.write('Biological Sex: '+m6.iloc[n]['Biological Sex'])
        st.write('Disgnosis : '+m6.iloc[n]['Diagnosis_battery']+'                       Manufacturer:'+m6.iloc[n]['Manufacturer'])
        st.write('Battery details:'+str(m6.iloc[n]['V'])+"                                 "+m6.iloc[n]['Details']+" "+m6.iloc[n]['Comments'])
        st.write('_____________________________________________________________________________________________________________________________')
        if Patient_demographic_details:
            st.subheader('Patient Demographic Details')
            st.write('Try patient no: 98')
            st.write('Year of Diagnosis : '+str(m6.iloc[n]['Year Dx'])+'                   Age at Diagnosis:  '+str(m6.iloc[n]['Age Dx']))
            st.write('Year of DBS : '+str(m6.iloc[n]['Year of DBS'])+'                     Age at DBS :  '+str(m6.iloc[n][17]))
            st.write('Year of Diagnosis to DBS: '+str(m6.iloc[n]['Yrs Dx to DBS'])+" Years")
            st.write('Surgical Site: '+m6.iloc[n]['Surgical site'])
            st.write('_____________________________________________________________________________________________________________________________')
        
        
        if Patient_contact_details:
            st.subheader("Patient Contact Details")   
            st.write('Contact: '+m6.iloc[n]['Contact'])
            st.write('Email: '+m6.iloc[n]['email'])
            st.write('Address: '+m6.iloc[n]['part address '])
            st.write('County: '+m6.iloc[n]['County']+'  Province : '+m6.iloc[n]['Province'])
            st.write('Insurer : '+m6.iloc[n]['Insurer'])
            st.write('_____________________________________________________________________________________________________________________________')
        
        if MDT_Workflow_details:
            st.subheader("MDT Workflow Details")
            st.write('Try Patient no 19')
            if type(m6.iloc[n]['New DBS Clinic'])!=str:
                st.write('New DBS Clinic : '+m6.iloc[n]['New DBS Clinic'].strftime("%m/%d/%Y"))
            else:
                st.write('New DBS Clinic : Not Available ')
            st.write('TAS Approval status : '+str(m6.iloc[n]['TAS approval']))
            st.write('MRI Brain : '+str(m6.iloc[n]['MRI brain']))
            st.write('Neuropsychology work up status : '+str(m6.iloc[n]['Neuropsychology']))
            st.write('SALT : '+str(m6.iloc[n]['SALT']))
            st.write('Physio status : '+str(m6.iloc[n]['Physio']))
            st.write('Levadopa Challenge Status : '+str(m6.iloc[n]['L-Dopa Challenge']))
            st.write('MDT Discussion Status: '+str(m6.iloc[n]['MDT Discussion']))
            st.write('General Status: '+str(m6.iloc[n]['Unnamed: 12']))
            st.write('Surgical OPD: '+str(m6.iloc[n]['Surgical OPD']))
            st.write('Surgeryd Date: '+str(m6.iloc[n]['Surgery']))
            if type(m6.iloc[n]['Physio'])!=str and type(m6.iloc[n]['Neuropsychology'])!=str and type(m6.iloc[n]['SALT'])!=str:
                mdt_df=m6.iloc[n][28:31]
                mdt_data=go.Scatter(x=mdt_df.values,y=mdt_df.index)
                layout = go.Layout(title='Test Timeline', xaxis=dict(title='Date'),yaxis=dict(title='Tests'))
                fig = go.Figure(data=[mdt_data], layout=layout)
                st.plotly_chart(fig)
            st.write('_____________________________________________________________________________________________________________________________')
            
        if ET_Motor_details:
            st.subheader("ET Motor Details")
            st.write('Try patient no 204 and 215')
            if type(m6.iloc[n]['Date'])!=str:
                st.write('Date of test : '+str(m6.iloc[n]['Date']))
            else:
                st.write('Date of test : Not Available')
            st.write()
            st.write('Hours taken for QUEST:   '+str(m6.iloc[n]['QUEST Hours']))
            et_motor_data=pd.DataFrame([m6.iloc[n]['FTMTRS'],m6.iloc[n]['QUEST'],m6.iloc[n]['QUEST Health'],m6.iloc[n]['QUEST QOL']],columns=['Values'],index=['FTMTRS','QUEST','Quest Health','Quest QOL'])
            #st.dataframe(et_motor_data.applymap(str))
            if type(et_motor_data['Values'][2])==str:
                et_motor_data=et_motor_data.applymap(str)
                st.dataframe(et_motor_data.transpose())
            else:
                st.bar_chart(et_motor_data)
            del et_motor_data
            st.write('_____________________________________________________________________________________________________________________________')
        
        
        if PD_Postop_details:
            st.subheader("PD Post-op Details")
            st.write('Try Patient no 241')
            if type(m6.iloc[n]['Surgical date'])!=str:
                st.write('Date of Surgery : '+m6.iloc[n]['Surgical date'].strftime("%m/%d/%Y"))
            else:
                st.write('Date of SUrgery : Not Available ')
            st.write('Age at Surgery:   '+str(m6.iloc[n]['Age at surgery']))
            st.write('Target:   '+str(m6.iloc[n]['Target']))
            test=['UPDRS I', 'UPDRS II']
            if m6.iloc[n]['UPDRS I.2']!='Not available':
                fig = go.Figure(data=[
                    go.Bar(name='Baseline', x=test, y=m6.iloc[n][67:69].replace('Not available',0)),
                    go.Bar(name='6months', x=test, y=m6.iloc[n][82:84].replace('Not available',0)),
                    go.Bar(name='1year', x=test, y=m6.iloc[n][100:102].replace('Not available',0))
                    ])
                st.plotly_chart(fig)
            elif m6.iloc[n]['UPDRS I.1']!='Not available':
                fig = go.Figure(data=[
                    go.Bar(name='Baseline', x=test, y=m6.iloc[n][67:69].replace('Not available',0)),
                    go.Bar(name='6months', x=test, y=m6.iloc[n][82:84].replace('Not available',0))
                    ])
                st.plotly_chart(fig)
            elif m6.iloc[n]['UPDRS I']!='Not available':
                fig = go.Figure(data=[
                    go.Bar(name='Baseline', x=test, y=m6.iloc[n][67:69].replace('Not available',0))                ])
                st.plotly_chart(fig)
                
            st.write('_____________________________________________________________________________________________________________________________')
        
        if Physio_details:
             st.subheader("Physio Details")
             st.write("Try patient no 96")
             test=['Gait 5TSTS', 'Gait TUAG']
             if m6.iloc[n]['1 year post opDate']!='Not available':
                st.write('1 year post op carried out on:' +m6.iloc[n]['1 year post opDate'].strftime("%m/%d/%Y"))
                if m6.iloc[n]['6 months post opDate']=='Not available':
                    st.write('6 months post op carried out on: Not available')
                else:
                    st.write('6 months post op carried out on:' +m6.iloc[n]['6 months post opDate'].strftime("%m/%d/%Y"))
                if m6.iloc[n]['SurgeryDate']=='Not available':
                    st.write('Surgery carried out on: Not Available')
                else:
                    st.write('Surgery carried out on:' +m6.iloc[n]['SurgeryDate'].strftime("%m/%d/%Y"))
                if m6.iloc[n]['Pre-OpDate']=='Not available':
                    st.write('Pre op Work up date Not available')
                else:
                    st.write('pre op work up carried out on:' +m6.iloc[n]['Pre-OpDate'].strftime("%m/%d/%Y"))
                fig = go.Figure(data=[
                    go.Bar(name='Baseline', x=test, y=m6.iloc[n][124:126].replace('Not available',0)),
                    go.Bar(name='6 months', x=test, y=m6.iloc[n][138:140].replace('Not available',0)),
                    go.Bar(name='1 year', x=test, y=m6.iloc[n][151:153].replace('Not available',0))
                    ])
                st.plotly_chart(fig)
             elif m6.iloc[n]['6 months post opDate']!='Not available':
                st.write('6 months post op carried out on:' +m6.iloc[n]['6 months post opDate'].strftime("%m/%d/%Y"))
                if m6.iloc[n]['SurgeryDate']=='Not available':
                    st.write('Surgery carried out on: Not Available')
                else:
                    st.write('Surgery carried out on:' +m6.iloc[n]['SurgeryDate'].strftime("%m/%d/%Y"))
                if m6.iloc[n]['Pre-OpDate']=='Not available':
                    st.write('Pre op Work up date Not available')
                else:
                    st.write('pre op work up carried out on:' +m6.iloc[n]['Pre-OpDate'].strftime("%m/%d/%Y"))
                fig = go.Figure(data=[
                    go.Bar(name='Baseline', x=test, y=m6.iloc[n][124:126].replace('Not available',0)),
                    go.Bar(name='6 months', x=test, y=m6.iloc[n][138:140].replace('Not available',0))
                    ])
                st.plotly_chart(fig)
             elif m6.iloc[n]['Pre-OpDate']!='Not available':
                st.write('pre op work up carried out on:' +m6.iloc[n]['Pre-OpDate'].strftime("%m/%d/%Y"))
                fig = go.Figure(data=[
                    go.Bar(name='Baseline', x=test, y=m6.iloc[n][124:126].replace('Not available',0))
                    ])
                st.plotly_chart(fig)
             else:
                st.write('No Information Available for the patient ')
             st.write('_____________________________________________________________________________________________________________________________')
             
        if Neuro_details:
            st.subheader("Neuro Details")
            if type(m6.iloc[n]['T1 date'])!=str:
                st.write('T1 date : '+m6.iloc[n]['Pre-OpDate'].strftime("%m/%d/%Y"))
                st.bar_chart(m6.iloc[n][181:183])
                st.write(m6.iloc[n][178:198].transpose())
            else:
                st.write('T1 Date : Not Available ')
            st.write('_____________________________________________________________________________________________________________________________')
    else:
        st.error("MRN not found in the database provided, please try again")
else:
    st.write('Sorry wrong password')
