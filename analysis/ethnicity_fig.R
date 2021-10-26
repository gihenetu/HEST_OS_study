library('tidyverse')

df_input <- read_rds(here::here("output", "cleaned_df.RDS")) %>%
# df_input <- read_csv(
#   here::here("output", "input.csv"),
#   col_types = cols(patient_id = col_integer(),ethnicity = col_double())
# ) %>% 
filter(region == "London") %>%
filter(age >= 18)

plot_ethnicity <- ggplot(data=df_input, aes(df_input$ethnicity)) + geom_histogram()

ggsave(
  plot= plot_ethnicity,
  filename="eth_descriptive.png", path=here::here("output"),
)