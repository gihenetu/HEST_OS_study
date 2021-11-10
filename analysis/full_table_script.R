#Load in packages needed
library(tidyverse)
library(data.table)
library(janitor)
library(gtsummary)

#Load in data and clean variables
input <- read_csv(
  here::here("output", "input.csv"))

cleaned_input <- input %>%
  mutate(imd=factor(imd, levels=c(1,2,3,4,5), labels=c("1 - Most deprived", "2", "3", "4", "5 - Least deprived"))) %>%
  mutate(ethnicity=factor(ethnicity, levels=c(1,2,3,4,5), labels=c("White", "Mixed", "Asian", "Black", "Other"))) %>%
  mutate(ethnicity_16=factor(ethnicity_16, levels=c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), labels=c("1","2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"))) %>%
  mutate(died_ons_covid_flag_any=factor(died_ons_covid_flag_any, levels = c(0,1), labels=c("No", "Yes"))) %>%
  mutate(died_ons_covid_flag_underlying=factor(died_ons_covid_flag_underlying, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(died_ons_covidconf_flag_underlying=factor(died_ons_covidconf_flag_underlying, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(covid_admission_date=factor(covid_admission_date, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(cov_vacc_d1=factor(cov_vacc_d1, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(cov_vacc_d2=factor(cov_vacc_d2, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(shield_dat=factor(shield_dat, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(nonshield_dat=factor(nonshield_dat, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(smoking_status=factor(smoking_status, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(asthma=factor(asthma, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(chronic_respiratory_disease=factor(chronic_respiratory_disease, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(hypertension=factor(hypertension, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(preg_36wks=factor(preg_36wks, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(chronic_cardiac_disease=factor(chronic_cardiac_disease, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(diabetes=factor(diabetes, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(dementia=factor(dementia, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(cnd=factor(cnd, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(learning_disability=factor(learning_disability, levels=c(0,1), labels=c("No", "Yes"))) %>%
  mutate(immuno_group=factor(immuno_group, levels=c(0,1), labels=c("No", "Yes")))

#Restrict to data needed
cleaned_df <- cleaned_input[c(9:11, 13:24, 26:38)]

##create tables
#Table 1 by 2nd dose vaccination status
table1 <- cleaned_df %>%
  tbl_summary(
    by = cov_vacc_d2,
    statistic = list(all_continuous() ~ "{mean} ({sd})",
                     all_categorical() ~ "{n} / {N} ({p}%)"),
    digits = all_continuous() ~ 2,
    missing_text = "(Missing)"
  )

#Table 1.1 by ethnicity
table11 <- cleaned_df %>%
  tbl_summary(
    by = ethnicity,
    statistic = list(all_continuous() ~ "{mean} ({sd})",
                     all_categorical() ~ "{n} / {N} ({p}%)"),
    digits = all_continuous() ~ 2,
    missing_text = "(Missing)"
  )

#Table 1.2 by LD
table12 <- cleaned_df %>%
  tbl_summary(
    by = learning_disability,
    statistic = list(all_continuous() ~ "{mean} ({sd})",
                     all_categorical() ~ "{n} / {N} ({p}%)"),
    digits = all_continuous() ~ 2,
    missing_text = "(Missing)"
  )

#Table 1.3 by Admission
table13 <- cleaned_df %>%
  tbl_summary(
    by = covid_admission_primary_diagnosis,
    statistic = list(all_continuous() ~ "{mean} ({sd})",
                     all_categorical() ~ "{n} / {N} ({p}%)"),
    digits = all_continuous() ~ 2,
    missing_text = "(Missing)"
  )

#Table 1.4 by Mortality
table14 <- cleaned_df %>%
  tbl_summary(
    by = died_ons_covid_flag_any,
    statistic = list(all_continuous() ~ "{mean} ({sd})",
                     all_categorical() ~ "{n} / {N} ({p}%)"),
    digits = all_continuous() ~ 2,
    missing_text = "(Missing)"
  )

#Read into html files
table1 %>%
  as_gt() %>%
  gt::gtsave(filename = "table1.html")

table11 %>%
  as_gt() %>%
  gt::gtsave(filename = "table1-1.html")

table12 %>%
  as_gt() %>%
  gt::gtsave(filename = "table1-2.html")

table13 %>%
  as_gt() %>%
  gt::gtsave(filename = "table1-3.html")

table14 %>%
  as_gt() %>%
  gt::gtsave(filename = "table1-4.html")





