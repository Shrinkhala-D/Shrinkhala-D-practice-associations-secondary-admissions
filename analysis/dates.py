##This script defines the date variables that will later be used to define our pre-COVID and post-COVID cohorts

##Importing neccessary modules
from ehrql import (
    days,
    case,
    when,
    minimum_of,
)

from datetime import date, timedelta

##Importing key TPP tables
from ehrql.tables.tpp import ( 
    patients, 
    ons_deaths,
)

##Defining the date variables
exposure_start_date1 = date(2017, 10, 1)       #"2017-10-01" 
cohort_start_date1 = date(2018, 10, 1)      #"2018-10-01"
cohort_end_date1 = date(2020, 2, 28)        #"2020-02-28"

