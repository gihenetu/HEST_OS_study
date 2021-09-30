from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA


study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2021-09-29"
    ),

age=patients.age_as_of(
        "2021-09-14",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
)

###### 
# admit_date <- "2021-05-14"
# change index_date to admit_date <- from 14 may 
# ineq dimensions 
    # age <- 18 plus all adults
    # sex 
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    # ethnicity 
            #16 categories
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

   
        #6 categories
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
    # deprivation 
        imd=patients.address_as_of(
        "2020-02-01",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"100": 0.1, "200": 0.2, "300": 0.7}},
        },
    ),
    
# vaccination <- yes vaccination is vaccinated 2 weeks before admission, to get which proportion were vaccinated 2 weeks before
    # First COVID vaccination administration codes
    covadm1_dat=patients.with_vaccination_record(
        returning="date",
        tpp={
            "target_disease_matches": "SARS-2 CORONAVIRUS",
        },
        emis={
            "procedure_codes": codelists.covadm1,
        },
        find_first_match_in_period=True,
        on_or_before="index_date", ### admissions date
        on_or_after="2021-05-14",
        date_format="YYYY-MM-DD",
    ),
    # Second COVID vaccination administration codes
    covadm2_dat=patients.with_vaccination_record(
        returning="date",
        tpp={
            "target_disease_matches": "SARS-2 CORONAVIRUS",
        },
        emis={
            "procedure_codes": codelists.covadm2,
        },
        find_last_match_in_period=True,
        on_or_before="index_date",
        on_or_after="covadm1_dat + 19 days",
        date_format="YYYY-MM-DD",
    ),
## comorbidities 
    # preg (compare by months)
    # BMI
#     smok
#     diab
#     hypert
#     dementia
#     LD
    
#     immuno-suppressant medications
    
# covid testing
# covid cases
# admission due to covid
covid_admission_date=patients.admitted_to_hospital(
        returning= "date_admitted" ,  # defaults to "binary_flag"
        with_these_diagnoses=covid_codelist,  # optional
        on_or_after="2021-05-14",
        find_first_match_in_period=True,  
        date_format="YYYY-MM-DD",  
        return_expectations={"date": {"earliest": "2021-05-14"}, "incidence" : 0.25},
   ),
    covid_admission_primary_diagnosis=patients.admitted_to_hospital(
        returning="primary_diagnosis",
        with_these_diagnoses=covid_codelist,  # optional
        on_or_after="2020-05-14",
        find_first_match_in_period=True,  
        date_format="YYYY-MM-DD", 
        return_expectations={"date": {"earliest": "2021-05-14"},"incidence" : 0.25,
            "category": {"ratios": {"U071":0.5, "U072":0.5}},
        },
    ),
# region
    region=patients.registered_practice_as_of(
        "2020-02-01",
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
# local authority
# first dose by 14 may
