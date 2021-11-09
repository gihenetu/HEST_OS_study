#Load in packages needed
library(tidyverse)
library(data.table)
library(janitor)
library(arsenal)
library(questionr)

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

#create tables
missing <- freq.na(cleaned_df)

table_one <- tableby(cov_vacc_d2 ~ ., data = cleaned_df) 
summary(table_one, title = "Table 1 by 2nd dose vaccination status")

table_one_one <- tableby(ethnicity ~ ., data = cleaned_df) 
summary(table_one_one, title = "Table 1.1 by ethnicity")

table_one_two <- tableby(learning_disability ~ ., data = cleaned_df) 
summary(table_one_two, title = "Table 1.2 by LD")

table_one_three <- tableby(covid_admission_primary_diagnosis ~ ., data = cleaned_df) 
summary(table_one_three, title = "Table 1.3 by Admission")

table_one_four <- tableby(died_ons_covid_flag_any ~ ., data = cleaned_df) 
summary(table_one_four, title = "Table 1.4 by Mortality")

# table_one_five <- tableby(learning_disability ~ ., data = cleaned_df) 
# summary(table_one_five, title = "Table 1.5 by COVID-19 case status")



#Read into word documents
write2word(missing, "~/Missing.doc", title="Missing values")
write2word(table_one, "~/Table1.doc", title="Table 1 by 2nd dose vaccination status")
write2word(table_one_one, "~/Table1-1.doc", title="Table 1.1 by ethnicity")
write2word(table_one_two, "~/Table1-2.doc", title="Table 1.2 by learning disability status")
write2word(table_one_three, "~/Table1-3.doc", title="Table 1.3 by admission")
write2word(table_one_four, "~/Table1-4.doc", title="Table 1.4 by mortality")
