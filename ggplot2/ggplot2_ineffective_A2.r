library(ggplot2)
library(dplyr)
library(readr)

# Load data
df <- read_csv("weather.csv")

# Data cleaning and transformation
df <- df %>%
  mutate(`Date.Full` = trimws(`Date.Full`)) %>%
  filter(!is.na(`Date.Full`), 
         !is.na(`Data.Temperature.Max Temp`), 
         !is.na(`Data.Temperature.Min Temp`)) %>%
  mutate(
    `Data.Temperature.Max Temp` = as.numeric(`Data.Temperature.Max Temp`),
    `Data.Temperature.Min Temp` = as.numeric(`Data.Temperature.Min Temp`)
  )

# Select first 20 unique dates
selected_dates <- unique(df$`Date.Full`)[1:20]
df_subset <- df %>% filter(`Date.Full` %in% selected_dates)

# Create the plot
ggplot(df_subset, aes(x = `Data.Temperature.Min Temp`, 
                           y = `Data.Temperature.Max Temp`)) +
  geom_point(size = 1, alpha = 0.8, color = "steelblue") +
  facet_wrap(~ `Date.Full`, ncol = 5) +
  theme_minimal(base_size = 10) +
  theme(
    strip.text = element_text(size = 8),
    axis.title = element_text(size = 10)
  ) +
  labs(
    x = "Data.Temperature.Min Temp",
    y = "Data.Temperature.Max Temp"
  )
