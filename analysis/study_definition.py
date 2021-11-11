from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

from codelists import *

index_date = "2021-05-14"
end_study_period = "2021-10-01"

## STUDY DEFINITION
study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    age=patients.age_as_of(
        index_date,
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    population=patients.satisfying(
        """
        registered
        AND
        region='London'
        AND 
        age >= 18
        """,
            registered=patients.registered_with_one_practice_between(
            index_date, end_study_period,
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
    ),
    # sex 
sex=patients.sex(
    return_expectations={
        "rate": "universal",
        "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    #deprivation
        imd=patients.categorised_as(
            {
                "0": "DEFAULT",
                "1": """
                        index_of_multiple_deprivation >=1
                    AND index_of_multiple_deprivation < 32844*1/5
                    """,
                "2": """
                        index_of_multiple_deprivation >= 32844*1/5
                    AND index_of_multiple_deprivation < 32844*2/5
                    """,
                "3": """
                        index_of_multiple_deprivation >= 32844*2/5
                    AND index_of_multiple_deprivation < 32844*3/5
                    """,
                "4": """
                        index_of_multiple_deprivation >= 32844*3/5
                    AND index_of_multiple_deprivation < 32844*4/5
                    """,
                "5": """
                        index_of_multiple_deprivation >= 32844*4/5
                    AND index_of_multiple_deprivation < 32844
                    """,
            },
            index_of_multiple_deprivation=patients.address_as_of(
                index_date,
                returning="index_of_multiple_deprivation",
                round_to_nearest=100,
            ),
            return_expectations={
                "rate": "universal",
                "category": {
                    "ratios": {
                        "0": 0.05,
                        "1": 0.19,
                        "2": 0.19,
                        "3": 0.19,
                        "4": 0.19,
                        "5": 0.19,
                    }
                },
            },
        ),
# ICS (formerly known as STP)
 stp=patients.registered_practice_as_of(
        index_date,
        returning="stp_code",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "STP1": 0.1,
                    "STP2": 0.1,
                    "STP3": 0.1,
                    "STP4": 0.1,
                    "STP5": 0.1,
                    "STP6": 0.1,
                    "STP7": 0.1,
                    "STP8": 0.1,
                    "STP9": 0.1,
                    "STP10": 0.1,
                }
            },
        },
    ),
ethnicity = patients.categorised_as(
            {"0": "DEFAULT",
            "1": "eth='1' OR (NOT eth AND ethnicity_sus='1')", 
            "2": "eth='2' OR (NOT eth AND ethnicity_sus='2')", 
            "3": "eth='3' OR (NOT eth AND ethnicity_sus='3')", 
            "4": "eth='4' OR (NOT eth AND ethnicity_sus='4')",  
            "5": "eth='5' OR (NOT eth AND ethnicity_sus='5')",
            }, 
            return_expectations={
            "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
            "incidence": 0.4,
            },
        
            eth=patients.with_these_clinical_events(    
                ethnicity_codes,
                returning="category",
                find_last_match_in_period=True,
                include_date_of_match=False,
                return_expectations={
                    "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
                    "incidence": 0.75,
                },
            ),

        # fill missing ethnicity from SUS
            ethnicity_sus=patients.with_ethnicity_from_sus(
                returning="group_6",  
                use_most_frequent_code=True,
                return_expectations={
                    "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
                    "incidence": 0.4,
                },
            ),
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
    sgss_covid19_any_test=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        returning="date",
        find_first_match_in_period=True,
        date_format="YYYY-MM-DD",
        on_or_after=index_date,
        return_expectations={
            "date": {"earliest": index_date, "latest" : end_study_period},
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
            "date": {"earliest": index_date, "latest" : end_study_period},
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
        return_expectations={"date": {"earliest": index_date}},
    ),
    died_ons_covid_flag_underlying=patients.with_these_codes_on_death_certificate(
        covid_codelist,
        match_only_underlying_cause=True,
        return_expectations={"date": {"earliest": index_date}},
    ),
    died_ons_covidconf_flag_underlying=patients.with_these_codes_on_death_certificate(
        covidconf_codelist,
        match_only_underlying_cause=True,
        return_expectations={"date": {"earliest": index_date}},
    ),
    died_date_ons=patients.died_from_any_cause(
        returning="date_of_death",
        include_month=True,
        include_day=True,
        return_expectations={"date": {"earliest": index_date}},
    ),
# admission due to covid
covid_admission_date=patients.admitted_to_hospital(
        returning= "binary_flag", 
        with_these_diagnoses=covid_codelist,
        on_or_after= index_date,
        find_first_match_in_period=True,  
        date_format="YYYY-MM-DD",  
        return_expectations={"date": {"earliest": index_date}, "incidence" : 0.25},
   ),
    covid_admission_primary_diagnosis=patients.admitted_to_hospital(
        returning="primary_diagnosis",
        with_these_diagnoses=covid_codelist,
        on_or_after= index_date,
        find_first_match_in_period=True,  
        date_format="YYYY-MM-DD", 
        return_expectations={"date": {"earliest": index_date},"incidence" : 0.25,
            "category": {"ratios": {"U071":0.5, "U072":0.5}},
        },
    ),
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
        date_format="YYYY-MM-DD",
    ),
    cov_vacc_d1=patients.with_vaccination_record(
        returning="binary_flag",
        tpp={
            "target_disease_matches": "SARS-2 CORONAVIRUS",
        },
        emis={
            "procedure_codes": covadm1,
        },
        find_first_match_in_period=True,
        date_format="YYYY-MM-DD",
    ),
    # Second COVID vaccination administration codes
    cov_vacc_d2=patients.with_vaccination_record(
        returning="binary_flag",
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
        returning="binary_flag",
        find_last_match_in_period=True,
        on_or_before=index_date,
        date_format="YYYY-MM-DD",
    ),
    # People that are not shielding
    nonshield_dat=patients.with_these_clinical_events(
        nonshield,
        returning="binary_flag",
        find_last_match_in_period=True,
        on_or_before=index_date,
        date_format="YYYY-MM-DD",
    ),
##HOUSEHOLD SIZE
    hh_id=patients.household_as_of(
        "2020-02-01",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 1000, "stddev": 200},
            "incidence": 1,
        },
    ),

    hh_size=patients.household_as_of(
        "2020-02-01",
        returning="household_size",
        return_expectations={
            "int": {"distribution": "normal", "mean": 8, "stddev": 1},
            "incidence": 1,
        }
    ),
## COMORBIDITIES 
#    BMI
bmi=patients.most_recent_bmi(
        between=["2010-02-01", end_study_period],
        minimum_age_at_measurement=16,
        include_measurement_date=False,
        # include_month=True,
        return_expectations={
            "date": {"earliest": "2010-02-01", "latest": end_study_period},
            "float": {"distribution": "normal", "mean": 35, "stddev": 10},
            "incidence": 0.95,
        },
    ),
#     smoking
smoking_status=patients.with_these_clinical_events(
        smoking,
        returning = "binary_flag",
        on_or_before= index_date,
        return_last_date_in_period=False,
        # include_month=True,
    ),
## Asthma
asthma=patients.with_these_clinical_events(
        asthma_dx,
        returning = "binary_flag",
        on_or_before = index_date,
        return_first_date_in_period=False,
    ),
# #Chronic respiratory disease
chronic_respiratory_disease=patients.with_these_clinical_events(
        chronic_respiratory_disease_codes,
        returning = "binary_flag",
        on_or_before = index_date,
        return_first_date_in_period=False,
    ),
#     hypertension
    hypertension=patients.with_these_clinical_events(
        hypertension_dx, 
        returning = "binary_flag",
        return_first_date_in_period=False, 
        return_expectations={"date": {"earliest": index_date}},
    ),
#     preg (compare by months)
        preg_36wks=patients.with_these_clinical_events(
            preg,
            returning="binary_flag",
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
        returning="binary_flag",
        on_or_before = index_date,
    ),
# Chronic Neurological Disease including Significant Learning Disorder
cnd=patients.with_these_clinical_events(
    chronic_neuro_disease,
    returning="binary_flag",
    on_or_before=index_date,
    ),
#   Learning Disabilities
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