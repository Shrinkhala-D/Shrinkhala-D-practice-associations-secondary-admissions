
##PACKAGES
library(dplyr)
library(tidyr)
library(readr)

#Importing data
dataset <- read_csv("output/dataset.csv")  # Generated via "dataset" framework, patient-level data
example_measure1 <- read_csv("output/example_measure1.csv")  # Generated via "measures" framework, practice-level data


#Selecting vars we'll merge in from dataset.csv - "practice_id" & "practice_region" 
dataset_b <- dataset %>%
  select(practice_id, practice_region) %>%
  distinct()  # Remove duplicates in case multiple patients have the same practice_region

# Merge dataset to measures data (practice-level)
merged_data <- example_measure1 %>%
  left_join(dataset_b, by = "practice_id")

#TBC
#Reshape dataset to be wide, per practice
#wide_data <- merged_data %>%
#  pivot_wider(
#    names_from = variable,  # Column that defines new wide column names
#    values_from = value     # Column that contains the values to spread
#  )


#View merged dataset 
print(merged_data)

# Save the final dataset as a new CSV file
write_csv(merged_data, "output/merged_data.csv")


#First, transform the measures data so it's one row PER PRACTICE
#Then, merge the practice-level vars from the main dataset into the measures data?
#Do a plot.



#Old code

#df_input <- read_csv(
#  here::here("output", "dataset.csv.gz"),
#  col_types = cols(patient_id = col_integer(),age = col_double())
#)
#plot_age <- ggplot(data=df_input, aes(df_input$age)) + geom_histogram()

#ggsave(
#  plot= plot_age,
#  filename="report.png", path=here::here("output"),
#)