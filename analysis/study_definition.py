from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

index_date = "2021-05-14"

## Codelists
ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_6",
)
ethnicity_codes_16 = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_16",
)
    #vacc codelist
    #cases codelist
    #testing codelist
smoking = codelist_from_csv(
    "codelists/opensafely-smoking.csv",
    system="ctv3",
    column="CTV3Code",
    category_column="Category",
)
asthma_dx = codelist_from_csv(
    "codelists/opensafely-asthma.csv", system="ctv3", column="CTV3ID"
)
chronic_respiratory_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-respiratory-disease.csv",
    system="ctv3",
    column="CTV3ID",
)
hypertension_dx = codelist_from_csv(
    "codelists/opensafely-hypertension.csv", system="ctv3", column="CTV3ID"
)
## STUDY DEFINITION
study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between(
        "2021-05-14", "2021-10-01"
    ),

    age=patients.age_as_of(
        "2021-05-14",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    # sex 
sex=patients.sex(
    return_expectations={
        "rate": "universal",
        "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    #deprivation
imd=patients.address_as_of(
        index_date,
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"100": 0.1, "200": 0.2, "300": 0.7}},
        },
    ),
# region
    region=patients.registered_practice_as_of(
        index_date,
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.2,
                    "South East": 0.2,
                },
            },
        },
    ),
# ethnicity 6 categories
ethnicity=patients.with_these_clinical_events(
    ethnicity_codes,
        returning="category",
        find_last_match_in_period=True,
        include_date_of_match=True,
        return_expectations={
            "category": {"ratios": {"1": 0.2, "2":0.2, "3":0.2, "4":0.2, "5": 0.2}},
            "incidence": 0.75,
        },
    ),
   ethnicity_16=patients.with_these_clinical_events(
        ethnicity_codes_16,
        returning="category",
        find_last_match_in_period=True,
        include_date_of_match=True,
        return_expectations={
            "category": {
                "ratios": {
                    "1": 0.0625,
                    "2": 0.0625,
                    "3": 0.0625,
                    "4": 0.0625,
                    "5": 0.0625,
                    "6": 0.0625,
                    "7": 0.0625,
                    "8": 0.0625,
                    "9": 0.0625,
                    "10": 0.0625,
                    "11": 0.0625,
                    "12": 0.0625,
                    "13": 0.0625,
                    "14": 0.0625,
                    "15": 0.0625,
                    "16": 0.0625,
                }
            },
            "incidence": 0.75,
        },
    ),

# # vaccination <- yes vaccination is vaccinated 2 weeks before admission, to get which proportion were vaccinated 2 weeks before
#     # First COVID vaccination administration codes
#     covadm1_dat=patients.with_vaccination_record(
#         returning="date",
#         tpp={
#             "target_disease_matches": "SARS-2 CORONAVIRUS",
#         },
#         emis={
#             "procedure_codes": codelists.covadm1,
#         },
#         find_first_match_in_period=True,
#         on_or_before="index_date", ### admissions date
#         on_or_after="2021-05-14",
#         date_format="YYYY-MM-DD",
#     ),
#     # Second COVID vaccination administration codes
#     covadm2_dat=patients.with_vaccination_record(
#         returning="date",
#         tpp={
#             "target_disease_matches": "SARS-2 CORONAVIRUS",
#         },
#         emis={
#             "procedure_codes": codelists.covadm2,
#         },
#         find_last_match_in_period=True,
#         on_or_before="index_date",
#         on_or_after="covadm1_dat + 19 days",
#         date_format="YYYY-MM-DD",
#     ),
# ## comorbidities 
#     BMI
bmi=patients.most_recent_bmi(
        between=["2010-02-01", "2020-01-31"],
        minimum_age_at_measurement=16,
        include_measurement_date=True,
        include_month=True,
        return_expectations={
            "date": {"earliest": "2010-02-01", "latest": "2020-01-31"},
            "float": {"distribution": "normal", "mean": 35, "stddev": 10},
            "incidence": 0.95,
        },
    ),
#     smoking
smoking_status_date=patients.with_these_clinical_events(
        smoking,
        on_or_before="2020-01-31",
        return_last_date_in_period=True,
        include_month=True,
    ),
#     asthma
#  asthma=patients.categorised_as(
#         {
#             "0": "DEFAULT",
#             "1": """
#                 (
#                   recent_asthma_code OR (
#                     asthma_code_ever AND NOT
#                     copd_code_ever
#                   )
#                 ) AND (
#                   prednisolone_last_year = 0 OR 
#                   prednisolone_last_year > 4
#                 )
#             """,
#             "2": """
#                 (
#                   recent_asthma_code OR (
#                     asthma_code_ever AND NOT
#                     copd_code_ever
#                   )
#                 ) AND
#                 prednisolone_last_year > 0 AND
#                 prednisolone_last_year < 5
                
#             """,
#         },
#         return_expectations={"category": {"ratios": {"0": 0.8, "1": 0.1, "2": 0.1}},},
#         recent_asthma_code=patients.with_these_clinical_events(
#             asthma_dx, between=["2017-02-01", "2020-01-31"],
#         ),
#         asthma_code_ever=patients.with_these_clinical_events(asthma_dx),
#         copd_code_ever=patients.with_these_clinical_events(
#             chronic_respiratory_disease_codes
#         ),
# #Chronic resp disease
# chronic_respiratory_disease=patients.with_these_clinical_events(
#         chronic_respiratory_disease_codes,
#         return_first_date_in_period=True,
#         include_month=True,
#     ),
#     hypertension
    hypertension=patients.with_these_clinical_events(
        hypertension_dx, return_first_date_in_period=True, include_month=True,
        return_expectations={"date": {"latest": "2020-01-31"}},
    ),
)

# #     preg (compare by months)
#         preg_36wks_date=patients.with_these_clinical_events(
#             codelists.preg,
#             returning="date",
#             find_last_match_in_period=True,
#             between=["index_date - 252 days", "index_date - 1 day"],
#             date_format="YYYY-MM-DD",
#         ),
#     ),   
#      # Chronic heart disease codes
# chd_group=patients.with_these_clinical_events(
#         codelists.chd_cov,
#         returning="binary_flag",
#         on_or_before="elig_date - 1 day",
#     ),

#     # Chronic kidney disease diagnostic codes
# ckd_group=patients.satisfying(
#         """
#             ckd OR
#             (ckd15_date AND 
#             (ckd35_date >= ckd15_date) OR (ckd35_date AND NOT ckd15_date))
#         """,
    
# #     diabetes
#     type1_diabetes=patients.with_these_clinical_events(
#         diabetes_t1_codes,
#         on_or_before="2020-01-31",
#         return_first_date_in_period=True,
#         include_month=True,
#     ),
#     type2_diabetes=patients.with_these_clinical_events(
#         diabetes_t2_codes,
#         on_or_before="2020-01-31",
#         return_first_date_in_period=True,
#         include_month=True,
#     ),
#     unknown_diabetes=patients.with_these_clinical_events(
#         diabetes_unknown_codes,
#         on_or_before="2020-01-31",
#         return_first_date_in_period=True,
#         include_month=True,
#     ),

 
#      diabetes_type=patients.categorised_as(
#         {
#             "T1DM":
#                 """
#                         (type1_diabetes AND NOT
#                         type2_diabetes) 
#                     OR
#                         (((type1_diabetes AND type2_diabetes) OR 
#                         (type1_diabetes AND unknown_diabetes AND NOT type2_diabetes) OR
#                         (unknown_diabetes AND NOT type1_diabetes AND NOT type2_diabetes))
#                         AND 
#                         (insulin_lastyear_meds > 0 AND NOT
#                         oad_lastyear_meds > 0))
#                 """,
#             "T2DM":
#                 """
#                         (type2_diabetes AND NOT
#                         type1_diabetes)
#                     OR
#                         (((type1_diabetes AND type2_diabetes) OR 
#                         (type2_diabetes AND unknown_diabetes AND NOT type1_diabetes) OR
#                         (unknown_diabetes AND NOT type1_diabetes AND NOT type2_diabetes))
#                         AND 
#                         (oad_lastyear_meds > 0))
#                 """,
#             "UNKNOWN_DM":
#                 """
#                         ((unknown_diabetes AND NOT type1_diabetes AND NOT type2_diabetes) AND NOT
#                         oad_lastyear_meds AND NOT
#                         insulin_lastyear_meds) 
                   
#                 """,
#             "NO_DM": "DEFAULT",
#         },

#         return_expectations={
#             "category": {"ratios": {"T1DM": 0.03, "T2DM": 0.2, "UNKNOWN_DM": 0.02, "NO_DM": 0.75}},
#             "rate" : "universal"

#         },

 
#         oad_lastyear_meds=patients.with_these_medications(
#             oad_med_codes, 
#             between=["2019-02-01", "2020-01-31"],
#             returning="number_of_matches_in_period",
#         ),
#         insulin_lastyear_meds=patients.with_these_medications(
#             insulin_med_codes,
#             between=["2019-02-01", "2020-01-31"],
#             returning="number_of_matches_in_period",
#         ),
#     ),
    
    

# #     dementia
# dementia=patients.with_these_clinical_events(
#         dementia, return_first_date_in_period=True, include_month=True,
#         return_expectations={"date": {"latest": "2020-01-31"}},
#     ),

# # Chronic Neurological Disease including Significant Learning Disorder
#     cns_group=patients.with_these_clinical_events(
#         codelists.cns_cov,
#         returning="binary_flag",
#         on_or_before="elig_date - 1 day",
# #     Learning Disabilities
#   learning_disability = patients.with_these_clinical_events(
#     learning_disability_codes,
#     on_or_before = "index_date",
#     returning = "binary_flag",
#     return_expectations = {"incidence": 0.2}
#   ),
   
# #  immunosuppressed
#     immuno_group=patients.satisfying(
#         "immrx OR immdx", 
#         # immunosuppression diagnosis codes
#         immdx=patients.with_these_clinical_events(
#             codelists.immdx_cov,
#             returning="binary_flag",
#             on_or_before="elig_date - 1 day",
#         ),
# #     immuno-suppressant medications
#      immrx=patients.with_these_medications(
#             codelists.immrx,
#             returning="binary_flag",
#             between=["elig_date - 6 months", "elig_date - 1 day"],
#         ),
#     ),

# # covid cases
# # admission due to covid
# covid_admission_date=patients.admitted_to_hospital(
#         returning= "date_admitted" ,  # defaults to "binary_flag"
#         with_these_diagnoses=covid_codelist,  # optional
#         on_or_after="2021-05-14",
#         find_first_match_in_period=True,  
#         date_format="YYYY-MM-DD",  
#         return_expectations={"date": {"earliest": "2021-05-14"}, "incidence" : 0.25},
#    ),
#     covid_admission_primary_diagnosis=patients.admitted_to_hospital(
#         returning="primary_diagnosis",
#         with_these_diagnoses=covid_codelist,  # optional
#         on_or_after="2020-05-14",
#         find_first_match_in_period=True,  
#         date_format="YYYY-MM-DD", 
#         return_expectations={"date": {"earliest": "2021-05-14"},"incidence" : 0.25,
#             "category": {"ratios": {"U071":0.5, "U072":0.5}},
#         },
#     ),
# )
