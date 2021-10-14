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
smoking = codelist_from_csv(
    "codelists/opensafely-smoking.csv",
    system="ctv3",
    column="CTV3Code",
    category_column="Category",
)
asthma_dx = codelist_from_csv(
    "codelists/opensafely-asthma.csv", system="ctv3", column="CTV3ID"
)
chronic_cardiac_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-cardiac-disease.csv", system="ctv3", column="CTV3ID"
)
chronic_kidney_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-kidney-disease.csv", system="ctv3", column="CTV3ID"
)
chronic_liver_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-liver-disease.csv", system="ctv3", column="CTV3ID"
)
chronic_respiratory_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-respiratory-disease.csv",
    system="ctv3",
    column="CTV3ID",
)
other_cancer_codes = codelist_from_csv(
    "codelists/opensafely-cancer-excluding-lung-and-haematological.csv",
    system="ctv3",
    column="CTV3ID",
)
lung_cancer_codes = codelist_from_csv(
    "codelists/opensafely-lung-cancer.csv", system="ctv3", column="CTV3ID"
)
haem_cancer_codes = codelist_from_csv(
    "codelists/opensafely-haematological-cancer.csv", system="ctv3", column="CTV3ID"
)
stroke = codelist_from_csv(
    "codelists/opensafely-stroke.csv", system="ctv3", column="CTV3ID"
)
dementia = codelist_from_csv(
    "codelists/opensafely-dementia.csv", system="ctv3", column="CTV3ID"
)
chronic_neuro_disease = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-cns_cov.csv",
    system="snomed",
    column="code",
)
learning_disability_codes = codelist_from_csv(
    "codelists/opensafely-learning-disabilities.csv", system="ctv3", column="CTV3Code"
)
hypertension_dx = codelist_from_csv(
    "codelists/opensafely-hypertension.csv", system="ctv3", column="CTV3ID"
)
diabetes_codes = codelist_from_csv(
    "codelists/opensafely-diabetes.csv", system="ctv3", column="CTV3ID"
)
preg = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-preg.csv",
    system="snomed",
    column="code",
)
immdx_cov = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-immdx_cov.csv",
    system="snomed",
    column="code",
)
immrx = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-immrx.csv",
    system="snomed",
    column="code",
)
# # COVID codelists
    #vacc codelists
    # First COVID vaccination administration codes
covadm1 = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-covadm1.csv",
    system="snomed",
    column="code",
)
# Second COVID vaccination administration codes
covadm2 = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-covadm2.csv",
    system="snomed",
    column="code",
)
    #testing and cases codelist
covid_codelist = codelist_from_csv(
    "codelists/opensafely-covid-identification.csv",
    system="icd10",
    column="icd10_code",
)
    #admissions <- not sure if there is a codelist to connect to here?
    #deaths
covid_codelist = codelist(["U071", "U072"], system="icd10")
covidconf_codelist = codelist(["U071"], system="icd10")
# High Risk from COVID-19 code
shield = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-shield.csv",
    system="snomed",
    column="code",
)
# Lower Risk from COVID-19 codes
nonshield = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-nonshield.csv",
    system="snomed",
    column="code",
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
## COVID-19 variables
# # covid testing
    sgss_covid19_date=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        returning="date",
        find_first_match_in_period=True,
        date_format="YYYY-MM-DD",
        on_or_after=index_date,
        return_expectations={
            "date": {"earliest": index_date, "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.05,
        },
    ),
# # covid cases
    sgss_covid19_pos_test=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        returning="date",
        find_first_match_in_period=True,
        date_format="YYYY-MM-DD",
        on_or_after=index_date,
        return_expectations={
            "date": {"earliest": index_date, "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.05,
        },
    ),
# # covid deaths
   died_date_cpns=patients.with_death_recorded_in_cpns(
        returning="date_of_death",
        include_month=True,
        include_day=True,
    ),
    died_ons_covid_flag_any=patients.with_these_codes_on_death_certificate(
        covid_codelist,
        match_only_underlying_cause=False,
        return_expectations={"date": {"earliest": "2020-03-01"}},
    ),
    died_ons_covid_flag_underlying=patients.with_these_codes_on_death_certificate(
        covid_codelist,
        match_only_underlying_cause=True,
        return_expectations={"date": {"earliest": "2020-03-01"}},
    ),
    died_ons_covidconf_flag_underlying=patients.with_these_codes_on_death_certificate(
        covidconf_codelist,
        match_only_underlying_cause=True,
        return_expectations={"date": {"earliest": "2020-03-01"}},
    ),
    died_date_ons=patients.died_from_any_cause(
        returning="date_of_death",
        include_month=True,
        include_day=True,
        return_expectations={"date": {"earliest": "2020-03-01"}},
    ),
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
  patient_index_date=patients.admitted_to_hospital(
        returning="date_discharged",
        with_these_diagnoses=covid_codelist,
        on_or_after=index_date,
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"date": {"earliest": index_date}},
    ),
    exposure_hospitalisation=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_diagnoses=covid_codelist,
        on_or_after=index_date,
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"date": {"earliest": index_date}},
    ),
# vaccination <- yes vaccination is vaccinated 2 weeks before admission, to get which proportion were vaccinated 2 weeks before
    # First COVID vaccination administration codes
    covadm1_dat=patients.with_vaccination_record(
        returning="date",
        tpp={
            "target_disease_matches": "SARS-2 CORONAVIRUS",
        },
        emis={
            "procedure_codes": covadm1,
        },
        find_first_match_in_period=True,
        # on_or_before="index_date",
        # on_or_after="2021-05-14",
        date_format="YYYY-MM-DD",
    ),
    # Second COVID vaccination administration codes
    covadm2_dat=patients.with_vaccination_record(
        returning="date",
        tpp={
            "target_disease_matches": "SARS-2 CORONAVIRUS",
        },
        emis={
            "procedure_codes": covadm2,
        },
        find_last_match_in_period=True,
        on_or_before= index_date,
        on_or_after="covadm1_dat + 19 days",
        date_format="YYYY-MM-DD",
    ),
    # Those COVID-19 shielding
    shield_dat=patients.with_these_clinical_events(
        shield,
        returning="date",
        find_last_match_in_period=True,
        on_or_before=index_date,
        date_format="YYYY-MM-DD",
    ),
    # People that are not shielding
    nonshield_dat=patients.with_these_clinical_events(
        nonshield,
        returning="date",
        find_last_match_in_period=True,
        on_or_before=index_date,
        date_format="YYYY-MM-DD",
    ),
## COMORBIDITIES 
#    BMI
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
## Asthma
asthma=patients.with_these_clinical_events(
        asthma_dx,
        returning = "binary_flag",
        return_first_date_in_period=True,
        include_month=True,
    ),
# #Chronic respiratory disease
chronic_respiratory_disease=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes,
        returning = "binary_flag",
        return_first_date_in_period=True,
        include_month=True,
    ),
#     hypertension
    hypertension=patients.with_these_clinical_events(
        hypertension_dx, 
        return_first_date_in_period=True, 
        include_month=True,
        return_expectations={"date": {"latest": "2020-01-31"}},
    ),
#     preg (compare by months)
        preg_36wks_date=patients.with_these_clinical_events(
            preg,
            returning="date",
            find_last_match_in_period=True,
            # between=["index_date - 252 days", "index_date - 1 day"],
            date_format="YYYY-MM-DD",
        ),
        # Chronic heart disease codes
chronic_cardiac_disease=patients.with_these_clinical_events(
        chronic_cardiac_disease_codes,
        returning= "binary_flag",
        on_or_before= index_date,
    ),
diabetes=patients.with_these_clinical_events(
        diabetes_codes,
        returning= "binary_flag",
        on_or_before = index_date,
    ),
    # Dementia
dementia=patients.with_these_clinical_events(
        dementia, 
        return_first_date_in_period=True, 
        include_month=True,
        return_expectations={"date": {"latest": "2020-01-31"}},
    ),
# Chronic Neurological Disease including Significant Learning Disorder
cnd=patients.with_these_clinical_events(
        chronic_neuro_disease,
        returning="binary_flag",
        on_or_before=index_date,
        ),
#     Learning Disabilities
  learning_disability = patients.with_these_clinical_events(
    learning_disability_codes,
    on_or_before = index_date,
    returning = "binary_flag",
    return_expectations = {"incidence": 0.2}
  ),
#  immunosuppressed
    immuno_group=patients.satisfying(
        "immrx OR immdx", 
        # immunosuppression diagnosis codes
        immdx=patients.with_these_clinical_events(
            immdx_cov,
            returning="binary_flag",
            on_or_before= index_date,
        ),
#     immuno-suppressant medications
     immrx=patients.with_these_medications(
            immrx,
            returning="binary_flag",
            on_or_before= index_date,
        ),
    ),
 )
  

    
#################### Do we need these? ####################################
#     # Chronic kidney disease diagnostic codes
# ckd_group=patients.satisfying(
#         """
#             ckd OR
#             (ckd15_date AND 
#             (ckd35_date >= ckd15_date) OR (ckd35_date AND NOT ckd15_date))
#         """,
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