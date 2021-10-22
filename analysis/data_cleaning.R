library('tidyverse')

df_input <- read_csv(
  here::here("output", "input.csv"),
  col_types = cols(
  patient_id = col_integer(),
  age = col_double(),
  sgss_covid19_date = col_date(format = ""),
  sgss_covid19_pos_test = col_date(format = ""),
  died_date_cpns = col_date(format = ""),
  died_date_ons = col_date(format = ""),
  patient_index_date = col_date(format = ""),
  exposure_hospitalisation = col_date(format = ""),
  covadm1_dat = col_date(format = ""),
  sex = col_character(),
  region = col_character(),
  stp = col_character(),
  covid_admission_primary_diagnosis = col_character()
)

)
cleaned <- filter(df_input, region == "London")



write_csv(
  here::here("output", "cleaned_df.csv")
)