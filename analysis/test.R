##R PACKAGES
library(dplyr)
library(tidyr)
library(readr)


#Importing data
dataset <- read_csv("output/dataset.csv")  # Generated via "dataset" framework, patient-level data
measures_exposures <- read_csv("output/measures_exposures.csv")  # Generated via "measures" framework, exposures over 1 year, practice-level data
measures_outcomes <- read_csv("output/measures_outcomes.csv") # Generated via measures "framework", weekly outcome over 20 weeks, practice-level data


###Data management on each dataset, prior to merge
#Exposures: reshaping from long to wide, so each measure is it's own separate variable (column)
            #Then sub-setting to keep all variables except for interval start date and end date

measures_exposures <- measures_exposures %>%
  pivot_wider(
    names_from = measure,  # Column that defines new wide column names
    values_from = ratio     # Column containing the values to be spread
  ) %>%
  select(practice_id,prop_under5,prop_5_to_16,prop_65_to_74,prop_75_to_84,prop_85_plus,prop_female,prop_copd,prop_hypertension)

#CHECK: That there is one row per patient


#Outcome: Adding a "week" variable to indicate which week each row represents 
measures_outcomes <- measures_outcomes %>%
  group_by(practice_id) %>%      # Group by practice
  arrange(practice_id, interval_start) %>%  # Ensure ordering by date
  mutate(week = row_number()) %>%  # Create sequential numbers
  ungroup()  # Remove grouping for further operations

#Dataset framework dataset.csv: Subset to keep: "practice_id" & "practice_region" 
dataset <- dataset %>%
  select(practice_id, practice_region)


###Merging all the datsets
#Merging the dataset frame to the wide measures exposure data (practice-level)
merged_data_a <- measures_exposures  %>%
  left_join(dataset, by = "practice_id")

##Then, merging this dataset to the measures_outcomes dataset (a 1:many merge)
merged_data <- measures_outcomes %>%
  left_join(merged_data_a, by = "practice_id")  %>% # Merge on practice_id
  rename(
    patient_ae_count = numerator,
    registered_patients = denominator
  )
#View merged dataset 
print(merged_data)

# Save the final dataset as a new CSV file
write_csv(merged_data, "output/merged_data.csv")




#Code blocks/ Old code
#Code to Reshape dataset to be wide, per practice
#wide_data <- merged_data %>%
#  pivot_wider(
#    names_from = variable,  # Column that defines new wide column names
#    values_from = value     # Column that contains the values to spread
#  )

#df_input <- read_csv(
#  here::here("output", "dataset.csv.gz"),
#  col_types = cols(patient_id = col_integer(),age = col_double())
#)
#plot_age <- ggplot(data=df_input, aes(df_input$age)) + geom_histogram()

#ggsave(
#  plot= plot_age,
#  filename="report.png", path=here::here("output"),
#)