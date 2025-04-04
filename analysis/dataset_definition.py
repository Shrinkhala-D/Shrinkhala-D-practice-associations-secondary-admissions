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

##Importing in the variables we defined in "variables.py"
from variables import *


##################################################################
## Creating the dataset & defining the population
##################################################################
##Creating the dataset
dataset = create_dataset()

# Actually defining the population
dataset.define_population(
    was_registered 
    & was_alive
)

#Configuring the dummy data
dataset.configure_dummy_data(population_size=100, legacy=True)

#Adding all the variables we defined in variables.py to the dataset
dataset.practice_id = practice_id
dataset.practice_region = practice_region

dataset.age = age
dataset.age_under_5 = age_under_5
dataset.age_5_to_16 = age_5_to_16
dataset.age_65_to_74 = age_65_to_74
dataset.age_75_to_84 = age_65_to_74

dataset.sex = patients.sex
dataset.female = female 

dataset.copd = copd
dataset.hypertension = hypertension

dataset.gp_consultations = gp_consultations
dataset.ae_count = ae_count

##Variables counting the number of events per patient per week, adding them to the dataset as separate variables 
for i in range (0,20):
    week_start_date = cohort_start_date1 + timedelta(weeks = i)  #Use timedelta(weeks=i) to add the unit of `i' weeks to the week start date in each loop
    week_end_date = week_start_date + timedelta(weeks = 1) #Use timedelta(week = 1) to add the unit of 1 week to the week end date in each loop  
    variable_name = f"ae_count_w{i+1}"
    ae_count = (
        ec
        .where(ec.arrival_date.is_on_or_between(week_start_date, week_end_date)) #Specify the time period for which the clinical event exists
        .count_for_patient()    #Specify we want the count of clinical events per patient
    )
    setattr(dataset, variable_name, ae_count )   #Using set attribute to add the variables to the data






##################################################################
## OPENSAFELY TERMINAL EDITOR
##################################################################

###Adding/updating codelists after listing them in the codelists.txt file
#Manually adding a codelist from OPENCODELISTS to your project, using the OS terminal, then uploading/updating them
    # opensafely codelists add https://www.opencodelists.org/codelist/opensafely/covid-identification/2020-06-03/
        #^^will add the codelist to your codelists.txt file and also as a .csv in the research project
    # opensafely codelists update
        #Updates the codelists in your repo


###Measures framework
#opensafely exec ehrql:v1 generate-measures analysis/default_measures.py --output example_measure1.csv


###Regular data
#opensafely exec ehrql:v1 generate-dataset analysis/dataset_definition.py --output example_data1.csv




##################################################################
## YAML
##################################################################
#Runs all the actions in your yaml (use option -f to force yaml to re-run): opensafely run run_all
#Unzips any zipped outputs you've created: opensafely unzip output
#Running specific actions: opensafely run 