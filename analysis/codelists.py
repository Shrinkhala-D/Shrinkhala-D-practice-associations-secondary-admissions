##CODELISTS
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



