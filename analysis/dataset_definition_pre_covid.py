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
)

##Importing in the dates we defined in "variables_dates"
from analysis.dates import (
    exposure_start_date,
    cohort_start_date,
    cohort_end_date
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
was_alive = (((patients.date_of_death.is_null()) | (patients.date_of_death.is_after(cohort_start_date))) & 
((ons_deaths.date.is_null()) | (ons_deaths.date.is_after(cohort_start_date))))

## Registration:
# If age > 1 year, registered at a practice at least 90 days before the cohort start date
# If age < 1 year, registered since birth

was_registered = (((practice_registrations.for_patient_on(cohort_start_date - days(90))).exists_for_patient()) | 
((patients.age_on(cohort_start_date) < 1) & ((practice_registrations.for_patient_on(cohort_start_date)).exists_for_patient())))

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

##Defining key variables in the dataset
dataset.practice_id = practice_registrations.for_patient_on(cohort_start_date).practice_pseudo_id
dataset.practice_region = practice_registrations.for_patient_on(cohort_start_date).practice_nuts1_region_name 
age = patients.age_on(cohort_start_date)
dataset.age = age
dataset.sex = patients.sex


## NUMBER OF CLINICAL EVENTS PER PATIENT PER WEEK
##Counting the number of events per patient per week, adding them to the dataset as separate variables 
for i in range (0,52):
    week_start_date = cohort_start_date + timedelta(weeks = i)  #Use timedelta(weeks=i) to add the unit of `i' weeks to the week start date in each loop
    week_end_date = week_start_date + timedelta(weeks = 1) #Use timedelta(week = 1) to add the unit of 1 week to the week end date in each loop  
    variable_name = f"event_count_w{i+1}"
    event_count = (
        clinical_events
        .where(clinical_events.date.is_on_or_between(week_start_date, week_end_date)) #Specify the time period for which the clinical event exists
        .count_for_patient()    #Specify we want the count of clinical events per patient
    )
    setattr(dataset, variable_name, event_count )   #Using set attribute to add the variables to the data


##VARIABLES CREATED USING MEASURES FRAMEWORK

##Using INTERVAL - to define our "interval"
#Filters the relevant table to only include the patients registered during the current interval
#In this case, relevant table = practice registrations
count_in_interval = practice_registrations.where(
    practice_registrations.start_date.is_during(INTERVAL)
)

#Defining defaults in measures --> Probably should be in another file!?
#How many variables all have the same denominator = total registered patients?
#age, sex, obesity, ethnic, mostdep IMD
measures.define_defaults(
    denominator =  was_registered & was_alive, 
    intervals = years(1).starting_on("2017-10-31"),
    group_by= {
       "practice_id": practice_registrations.for_patient_on(cohort_start_date).practice_pseudo_id  
    }
)

##Defining numerators 
#Proportion of female patients in the practice
is_female = (patients.sex == "female")  #numerator for proportion
                                        #denominator for proportion will be the study population: was_registered & was_alive
#dataset.is_female = is_female           #also adding "is_female" as a variable to the dataset to test that it's a usable object 

#Proportion of patients aged <5 years 
age_under_5 = age <5
dataset.age_under_5 = age_under_5

#Proportion of patients diagnosed with COPD
has_copd = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(copd_snomed_clinical))
    .where(clinical_events.date.is_on_or_between(exposure_start_date, cohort_start_date))
    .exists_for_patient())

# dataset.copd = has_copd   
measures.define_measure(
    name = "prop_copd", 
    numerator = has_copd
)

measures.define_measure(
    name = "prop_female", 
    numerator = is_female
)

measures.define_measure(
    name = "prop_under5", 
    numerator = age_under_5
)

#measures.define_measure(
#   name = "prop_copd",
#   numerator = has_copd,
#   denominator = was_registered & was_alive, 
#   group_by = {
#   "practice_id": practice_registrations.for_patient_on(cohort_start_date).practice_pseudo_id
#    },
#    intervals=years(1).starting_on("2017-10-31")
#)

#measures.define_measure(
#    name="female_count_w",
#    numerator = is_female,
#    denominator = was_registered & was_alive, 
#    group_by = {
#        "practice_id": practice_registrations.for_patient_on(cohort_start_date).practice_pseudo_id
#    },
#    intervals=weeks(4).starting_on("2018-10-01"),
#)


##Pass this dataset through to STATA
##Then create proportion variables 

##################################################################
## Cambridge Multi-Morbidity
##################################################################


#Per person: apply the coefficient to each diagnosed ID
##################################################################
## OPENSAFELY TERMINAL EDITOR
##################################################################

#Measures framework
#opensafely exec ehrql:v1 generate-measures analysis/dataset_definition_pre_covid.py --output example_measure1.csv

#Regular data
#opensafely exec ehrql:v1 generate-dataset analysis/dataset_definition_pre_covid.py --output example_data1.csv

##Adding/updating codelists after listing them in the codelists.txt file
#opensafely codelists update