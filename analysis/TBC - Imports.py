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