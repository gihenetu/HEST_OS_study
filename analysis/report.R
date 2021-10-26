library('tidyverse')

df_input <- read_csv(here::here("output", "cleaned_df.csv"))
# df_input <- read_csv(
#   here::here("output", "input.csv"),
#   col_types = cols(patient_id = col_integer(),age = col_double())
# ) %>%
# filter(region=="London") %>%
# filter(age >= 18)

plot_age <- ggplot(data=df_input, aes(df_input$age)) + geom_histogram()

ggsave(
  plot= plot_age,
  filename="descriptive.png", path=here::here("output"),
)