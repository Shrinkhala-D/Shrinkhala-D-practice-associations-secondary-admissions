####################################################################
##Importing key modules, TPP tables, previously defined variables
####################################################################
from module_table_imports import *

##Importing in the dates we defined in "dates,py"
from analysis.dates import (
    exposure_start_date1,
    cohort_start_date1, 
    cohort_end_date1,
)

##Importing in the variables we defined in "variables.py"
from variables import *



####################################################################
##Enabling & configuring the measures framework 
####################################################################
measures = create_measures()
measures.configure_disclosure_control(enabled=False)    #disabling disclosure control for demonstration

measures.configure_dummy_data(population_size=100, legacy = True)

##Using INTERVAL - to define our "interval"
#Filters the relevant table to only include the patients registered during the current interval
#In this case, relevant table = practice registrations
count_in_interval = practice_registrations.where(
    practice_registrations.start_date.is_during(INTERVAL)
)

#Defining defaults in measures
#Vars with the same denominator (total registered patients):
    #age, sex, obesity, ethnic, mostdep IMD, copd, hyp
    #NOTE: copd, hypertension, the denom will be patients aged 20 year or older 

measures.define_defaults(
    denominator =  was_registered & was_alive, 
    intervals = years(1).starting_on(exposure_start_date1),
    group_by= {
       "practice_id": practice_registrations.for_patient_on(cohort_start_date1).practice_pseudo_id  
    }
)
#"2017-10-31"




####################################################################
## Creating variables in the measures framework 
####################################################################

#Age proportions
measures.define_measure(
    name = "prop_under5", 
    numerator = age_under_5
)

measures.define_measure(
    name = "prop_5_to_16", 
    numerator = age_5_to_16
)

measures.define_measure(
    name = "prop_65_to_74", 
    numerator = age_65_to_74
)

measures.define_measure(
    name = "prop_75_to_84", 
    numerator = age_75_to_84
)

measures.define_measure(
    name = "prop_85_plus", 
    numerator = age_85_plus
)

#Proportion female
measures.define_measure(
    name = "prop_female", 
    numerator = female
)


#MEASURES FOR CAMBRIDGE COMORBIDITY SCORE 
#Prop diagnosed with various diseases...
measures.define_measure(
    name = "prop_copd", 
    numerator = copd
)   

measures.define_measure(
    name = "prop_hypertension", 
    numerator = hypertension
)   


##OUTCOME - weekly rate of A&E attendances, per practice
#First, identify everyone with an A&E admission in the time frame


measures.define_measure(
    name="ae_count_w",
    numerator = ae_count, 
    denominator = was_registered & was_alive,
    group_by = {
        "practice_id": practice_registrations.for_patient_on(cohort_start_date1).practice_pseudo_id
    },
    intervals = weeks(20).starting_on(cohort_start_date1)
)

#measures.define_measure(
#    name="female_count_w",
#    numerator = is_female,
#    denominator = was_registered & was_alive, 
#    group_by = {
#        "practice_id": practice_registrations.for_patient_on(cohort_start_date1).practice_pseudo_id
#    },
#    intervals=weeks(4).starting_on("2018-10-01"),
#)







#CODE BLOCKS

###Code to create a variable counting the number of A&E admissions per week per patient
#for i in range (0,20):
#    week_start_date = cohort_start_date1 + timedelta(weeks = i)  #Use timedelta(weeks=i) to add the unit of `i' weeks to the week start date in each loop
#    week_end_date = week_start_date + timedelta(weeks = 1) #Use timedelta(week = 1) to add the unit of 1 week to the week end date in each loop  
#    variable_name = f"ae_count_w{i+1}"
#    event_count = (
#        ec
#        .where(ec.arrival_date.is_on_or_between(week_start_date, week_end_date)) #Specify the time period for which the clinical event exists
#        .count_for_patient()    #Specify we want the count of clinical events per patient
#    )
#    setattr(dataset, variable_name, event_count )   #Using set attribute to add the variables to the data

###Code trying to loop through measures - code doesn't work just yet
#age_under_5,
#age_5_to_16,
#age_65_to_74,
#age_75_to_84,
#age_85_plus,

#age_groups = {
#    "prop_under_5": age_under_5,
#    "prop_5_to_16": age_5_to_16,
#    "prop_65_to_74": age_65_to_74,
#    "prop_75_to_84": age_75_to_84,
#    "prop_85_plus": age_85_plus,
#}

#for age_label, age_condition in age_groups.items():
#    measures.define_measure(
#        name = f"{age_label}",
#        numerator = {age_condition}
#    )

###Basic code for creating/defining a measure
#measures.define_measure(
#    name="female_count_w",
#    numerator = is_female,
#    denominator = was_registered & was_alive, 
#    group_by = {
#        "practice_id": practice_registrations.for_patient_on(cohort_start_date).practice_pseudo_id
#    },
#    intervals=weeks(4).starting_on("2018-10-01"),
#)