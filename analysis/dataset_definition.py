####################################################################
##Importing key modules, TPP tables, previously defined variables
####################################################################

from ehrql import (
    create_dataset, 
    create_measures,
    codelist_from_csv,
    when, 
    years,
    months,
    weeks,
    days, 
    minimum_of, 
    case, 
    show,
    INTERVAL, 
    )

#from cohortextractor import (
#    codelist_from_csv,
#    combine_codelists, 
#    codelist
#    )

from datetime import (
    date, timedelta
    )

##Importing key TPP tables
from ehrql.tables.tpp import (
    patients, 
    practice_registrations,
    clinical_events, 
    ons_deaths,
    ec,
)

##Importing in the dates we defined in "variables_dates"
from analysis.dates import (
    exposure_start_date1,
    cohort_start_date1, 
    cohort_end_date1,
)

from codelists import *


#Enabling the measures framework 
measures = create_measures()
measures.configure_disclosure_control(enabled=False)    #disabling disclosure control for demonstration

##Creating the dataset
dataset = create_dataset()


##################################################################
## Defining the population
##################################################################
## Alive on the start date for each cohort
was_alive = (((patients.date_of_death.is_null()) | (patients.date_of_death.is_after(cohort_start_date1))) & 
((ons_deaths.date.is_null()) | (ons_deaths.date.is_after(cohort_start_date1))))

## Registration:
# If age > 1 year, registered at a practice at least 90 days before the cohort start date
# If age < 1 year, registered since birth

was_registered = (((practice_registrations.for_patient_on(cohort_start_date1 - days(90))).exists_for_patient()) | 
((patients.age_on(cohort_start_date1) < 1) & ((practice_registrations.for_patient_on(cohort_start_date1)).exists_for_patient())))

# Actually defining the population
dataset.define_population(
    was_registered 
    & was_alive
)

#Configuring the dummy data
dataset.configure_dummy_data(population_size=100, legacy=True)




##################################################################
## Defining & adding variables to the dataset
##################################################################
##Practice characteristics
dataset.practice_id = practice_registrations.for_patient_on(cohort_start_date1).practice_pseudo_id
dataset.practice_region = practice_registrations.for_patient_on(cohort_start_date1).practice_nuts1_region_name 

#Age proportions
age = patients.age_on(cohort_start_date1)   ##Patient's age on index date
age_under_5 = age <5    #True or False patient is aged under 5
age_5_to_16 = (age >= 5) & (age <= 16)        #True or false patient is aged between 5 and 16 (inclusive)
age_65_to_74 = (age >= 65) & (age <= 74)
age_75_to_84 = (age >= 75) & (age <= 84)
age_85_plus = age >= 85 
dataset.age = age
dataset.age_under_5 = age_under_5
dataset.age_5_to_16 = age_5_to_16
dataset.age_65_to_74 = age_65_to_74
dataset.age_75_to_84 = age_75_to_84

#Sex
female = (patients.sex == "female")  #numerator for proportion      
dataset.sex = patients.sex
dataset.female = female 

#Patients diagnosed with COPD - numerator for proportion
copd = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(copd_snomed_clinical))
    .where(clinical_events.date.is_on_or_between(exposure_start_date1, cohort_start_date1))
    .exists_for_patient())

dataset.copd = copd

#Patients diagnosed with hypertension - numerator for proportion
hypertension = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(hypertension_snomed))
    .where(clinical_events.date.is_on_or_between(exposure_start_date1, cohort_start_date1))
    .exists_for_patient()
)


dataset.hypertension = hypertension

##Number of general practice consultations per patient in the year PRIOR to cohort start date
gp_consultations = (
    clinical_events
    .where(clinical_events.date.is_on_or_between(exposure_start_date1, cohort_start_date1)) #Specify the time period for which the clinical event exists
    .count_for_patient()    #Specify we want the count of clinical events per patient
)

dataset.gp_consultations = gp_consultations


## OUTCOME: NUMBER OF A&E ATTENDANCES DURING STUDY PERIOD (PER PATIENT PER WEEK)
##Counting the number of events per patient per week, adding them to the dataset as separate variables 
for i in range (0,20):
    week_start_date = cohort_start_date1 + timedelta(weeks = i)  #Use timedelta(weeks=i) to add the unit of `i' weeks to the week start date in each loop
    week_end_date = week_start_date + timedelta(weeks = 1) #Use timedelta(week = 1) to add the unit of 1 week to the week end date in each loop  
    variable_name = f"ae_count_w{i+1}"
    event_count = (
        ec
        .where(ec.arrival_date.is_on_or_between(week_start_date, week_end_date)) #Specify the time period for which the clinical event exists
        .count_for_patient()    #Specify we want the count of clinical events per patient
    )
    setattr(dataset, variable_name, event_count )   #Using set attribute to add the variables to the data


#event_count = (
#        clinical_events
#        .where(clinical_events.date.is_on_or_between(week_start_date, week_end_date)) #Specify the time period for which the clinical event exists
#        .count_for_patient()    #Specify we want the count of clinical events per patient
#    )






##Pass this dataset through to STATA
##Then create proportion variables 

##################################################################
## Cambridge Multi-Morbidity
##################################################################


#Per person: apply the coefficient to each diagnosed ID
##################################################################
## OPENSAFELY TERMINAL EDITOR
##################################################################

##Adding/updating codelists after listing them in the codelists.txt file
#opensafely codelists update

#Measures framework
#opensafely exec ehrql:v1 generate-measures analysis/default_measures.py --output example_measure1.csv

#Regular data
#opensafely exec ehrql:v1 generate-dataset analysis/dataset_definition.py --output example_data1.csv

##################################################################
## YAML
##################################################################
#Runs all the actions in your yaml: opensafely run run_all
#Unzips any zipped outputs you've created: opensafely unzip output