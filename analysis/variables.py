##This file creates the variables we'll use to populate the regular dataset & the measures dataset 

####################################################################
##Importing key modules, TPP tables, previously defined variables
####################################################################
from module_table_imports import *

##Importing in the dates we defined in "dates.py"
from analysis.dates import (
    exposure_start_date1,
    cohort_start_date1, 
    cohort_end_date1,
)

##Importing in the codelists 
from codelists import *



##################################################################
## Defining & adding variables to the dataset
##################################################################

##Conditions needed to define the population to generate the dataset
## Alive on the start date for each cohort
was_alive = (((patients.date_of_death.is_null()) | (patients.date_of_death.is_after(cohort_start_date1))) & 
((ons_deaths.date.is_null()) | (ons_deaths.date.is_after(cohort_start_date1))))

## Registration:
# If age > 1 year, registered at a practice at least 90 days before the cohort start date
# If age < 1 year, registered since birth

was_registered = (((practice_registrations.for_patient_on(cohort_start_date1 - days(90))).exists_for_patient()) | 
((patients.age_on(cohort_start_date1) < 1) & ((practice_registrations.for_patient_on(cohort_start_date1)).exists_for_patient())))


##Practice characteristics
practice_id = practice_registrations.for_patient_on(cohort_start_date1).practice_pseudo_id
practice_region = practice_registrations.for_patient_on(cohort_start_date1).practice_nuts1_region_name 



#Age proportions
age = patients.age_on(cohort_start_date1)   ##Patient's age on index date
age_under_5 = age <5    #True or False patient is aged under 5
age_5_to_16 = (age >= 5) & (age <= 16)        #True or false patient is aged between 5 and 16 (inclusive)
age_65_to_74 = (age >= 65) & (age <= 74)
age_75_to_84 = (age >= 75) & (age <= 84)
age_85_plus = age >= 85 


#Sex
female = (patients.sex == "female")  #numerator for proportion      

#Patients diagnosed with COPD - numerator for proportion
copd = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(copd_snomed_clinical))
    .where(clinical_events.date.is_on_or_between(exposure_start_date1, cohort_start_date1))
    .exists_for_patient())



#Patients diagnosed with hypertension - numerator for proportion
hypertension = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(hypertension_snomed))
    .where(clinical_events.date.is_on_or_between(exposure_start_date1, cohort_start_date1))
    .exists_for_patient()
)

##Number of general practice consultations per patient in the year PRIOR to cohort start date
gp_consultations = (
    clinical_events
    .where(clinical_events.date.is_on_or_between(exposure_start_date1, cohort_start_date1)) #Specify the time period for which the clinical event exists
    .count_for_patient()    #Specify we want the count of clinical events per patient
)


## OUTCOME: NUMBER OF A&E ATTENDANCES DURING STUDY PERIOD (PER PATIENT PER WEEK)
#Variable capturing the TOTAL number of AE attendances per patient over the study period (later used as numeratore for measure)
ae_count = (ec.where(ec.arrival_date.is_on_or_between(cohort_end_date1, cohort_end_date1)).count_for_patient())








###Code for a variable counting the number of instances of a thing per patientover a specific time period
#event_count = (
#        clinical_events
#        .where(clinical_events.date.is_on_or_between(week_start_date, week_end_date)) #Specify the time period for which the clinical event exists
#        .count_for_patient()    #Specify we want the count of clinical events per patient
#    )

