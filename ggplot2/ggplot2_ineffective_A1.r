library(ggplot2)
library(dplyr)
library(readr)
library(scales)

# Load data
df <- read_csv("weather.csv")

# Data cleaning and transformation
df <- df %>%
  mutate(`Date.Full` = trimws(`Date.Full`)) %>%
  filter(!is.na(`Date.Full`), 
         !is.na(`Station.Code`),
         !is.na(`Data.Temperature.Max Temp`), 
         !is.na(`Data.Temperature.Min Temp`), 
         !is.na(`Data.Precipitation`)) %>%
  mutate(
    `Data.Temperature.Max Temp` = as.numeric(`Data.Temperature.Max Temp`),
    `Data.Temperature.Min Temp` = as.numeric(`Data.Temperature.Min Temp`),
    `Data.Precipitation` = as.numeric(`Data.Precipitation`),
    precip_for_color = ifelse(`Data.Precipitation` == 0, 0.01, `Data.Precipitation`)
  )

# Select first 20 station codes
selected_stations <- unique(df$`Station.Code`)[1:20]
df_subset <- df %>% filter(`Station.Code` %in% selected_stations)

# Build the plot
ggplot(df_subset, aes(x = `Data.Temperature.Min Temp`, 
                           y = `Data.Temperature.Max Temp`, 
                           color = precip_for_color)) +
  geom_point(size = 1, alpha = 0.8) +
  facet_wrap(~ `Station.Code`, ncol = 5) +
  scale_color_gradientn(
    colors = c("black", "blue"),
    trans = "log",
    name = "Precipitation"
  ) +
  theme_minimal(base_size = 10) +
  theme(
    strip.text = element_text(size = 8),
    axis.title = element_text(size = 10)
  ) +
  labs(
    x = "Data.Temperature.Min Temp",
    y = "Data.Temperature.Max Temp"
  )
