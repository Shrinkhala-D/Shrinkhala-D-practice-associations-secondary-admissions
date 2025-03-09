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

##Importing in the numerator variables & other key objects we defined in "dataset_definition"
from analysis.dataset_definition import (
    was_registered,
    was_alive,
    age_under_5,
    age_5_to_16,
    age_65_to_74,
    age_75_to_84,
    age_85_plus,
    female,
    copd,
    hypertension,
    gp_consultations
)

#Enabling the measures framework 
measures = create_measures()
measures.configure_disclosure_control(enabled=False)    #disabling disclosure control for demonstration

#TBC: configuring the dummy measures data 


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

##VARIABLES CREATED USING MEASURES FRAMEWORK 

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

#Prop diagnosed with various diseases...
measures.define_measure(
    name = "prop_copd", 
    numerator = copd
)   

measures.define_measure(
    name = "prop_hypertension", 
    numerator = hypertension
)   

#Trying to loop through measures - code doesn't work just yet
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


#measures.define_measure(
#    name="female_count_w",
#    numerator = is_female,
#    denominator = was_registered & was_alive, 
#    group_by = {
#        "practice_id": practice_registrations.for_patient_on(cohort_start_date).practice_pseudo_id
#    },
#    intervals=weeks(4).starting_on("2018-10-01"),
#)