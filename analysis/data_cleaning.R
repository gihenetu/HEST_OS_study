library('tidyverse')

cleaned_df <- read_csv(
  here::here("output", "input.csv"),
  col_types = cols(
  patient_id = col_integer(),
  sgss_covid19_date = col_date(format = ""),
  sgss_covid19_pos_test = col_date(format = ""),
  died_date_cpns = col_date(format = ""),
  died_date_ons = col_date(format = ""),
  patient_index_date = col_date(format = ""),
  exposure_hospitalisation = col_date(format = ""),
  covadm1_dat = col_date(format = ""),
  age = col_double(),
  sex = col_character(),
  imd = col_double(),
  region = col_character(),
  stp = col_character(),
  ethnicity = col_double(),
  ethnicity_16 = col_double(),
  died_ons_covid_flag_any = col_double(),
  died_ons_covid_flag_underlying = col_double(),
  died_ons_covidconf_flag_underlying = col_double(),
  covid_admission_date = col_double(),
  covid_admission_primary_diagnosis = col_character(),
  cov_vacc_d1 = col_double(),
  cov_vacc_d2 = col_double(),
  shield_dat = col_double(),
  nonshield_dat = col_double(),
  hh_id = col_double(),
  hh_size = col_double(),
  bmi = col_double(),
  smoking_status = col_double(),
  asthma = col_double(),
  chronic_respiratory_disease = col_double(),
  hypertension = col_double(),
  preg_36wks_date = col_double(),
  chronic_cardiac_disease = col_double(),
  diabetes = col_double(),
  dementia = col_double(),
  cnd = col_double(),
  learning_disability = col_double(),
  immuno_group = col_double())) %>%
filter(region == "London") %>%
filter(age >= 18) %>%
write_rds(
  here::here("output", "cleaned_df.RDS")
)