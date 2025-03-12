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


####################################################################
##Uploading the codelists from the .csv files
####################################################################
#Note: We previously already imported the .csv files using code in the opensafely terminal


copd_snomed_clinical = codelist_from_csv(
    "codelists/user-elsie_horne-copd_snomed.csv", 
    #system="snomed", 
    column="code"
)

copd_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-copd_icd10.csv",
    #system="icd10",
    column="code"
)

hypertension_snomed = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv",
    column="code"
)

hypertension_icd10 = codelist_from_csv(
    "codelists/user-elsie_horne-hypertension_icd10.csv",
    column="code"
)

hypertension_drugs = codelist_from_csv(
    "codelists/user-elsie_horne-hypertension_drugs_dmd.csv",
    column="code"
)



