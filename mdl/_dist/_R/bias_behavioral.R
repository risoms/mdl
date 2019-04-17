rm(list=ls())
#******************************************************************** Imports
#install.packages("jtools")
library(parallel); library(tidyverse); library(itrak);
#**************************************************************** Definitions
suppressPackageStartupMessages(library(tidyverse))
data_path <- "~/Desktop/R33-analysis-master/output"
load_path <- paste(data_path, "1_process/data/behavioral", sep = "/")
tlbs_path <- paste(data_path, "2_tlbs/behavioral", sep = "/")
summary_path <- paste(data_path, "3_bias", sep = "/")
n_cores <- 4
n_trial <- 198
load_directory <- paste(load_path, list.files(load_path), sep = "/")
#*********************************************************************************************
#**************************************************************************************** TLBS
#run dotprobe
process_dotprobe <- function(path, save_path, n_trial){
  df <- read_csv(path, na = c(".", ""), guess_max = 999999,
                 col_types = cols_only(participant = col_character(), #participant
                                       TrialNum = col_double(),
                                       type = col_character(),
                                       event = col_character(),
                                       trialType = col_character(),
                                       Key_Resp.rt = col_number(),
                                       Key_Resp.acc = col_double(), #Key_Resp.acc
                                       LEmotion = col_character(), #LStim
                                       REmotion = col_character(), #RStim
                                       DotLoc = col_character() #DotStim
                                       ))
  #convert acc to logicial
  df$Key_Resp.acc  <- as.logical(as.integer(df$Key_Resp.acc))
  
  #rename variables
  #colnames(df)[colnames(df) == 'TrialNum'] <- 'trial'
  colnames(df)[colnames(df) == 'Key_Resp.rt'] <- 'RT'
  
  # separate trial metadata from sample-measurement data
  itrak_data <- df %>% 
    select(id = participant, trial = TrialNum, event = event, trialType, RT = RT)
  
  #get summary of trial level info
  trial_info <- df %>%
    ##add new variables
    mutate(dot_location = gsub(".$", "", DotLoc),
           emo_location = ifelse(LEmotion == "Neutral", "Right", "Left"),
           congruent = dot_location == emo_location) %>%
    
    ##select variables
    select(id = participant, trial = TrialNum, dot_location, trialType,
           emo_location, congruent, accurate = Key_Resp.acc) %>% distinct()
  
  # get RT
  RT <- df %>% 
    select(id = participant, trial = TrialNum, RT = RT, trialType) %>% 
    ##get unique trials
    distinct(trial, .keep_all = TRUE) %>%
    ##select variables
    select(id, trial, RT)
  # set rt as decimal value
  RT$RT <- RT$RT / 1000
  
  # assign missing values to incorrect trials
  RT$RT[!trial_info$accurate] <- NA
  
  # assign missing values to outliers
  ## first eliminate trials with RTs less than 0.2 s or more than 1.5 s
  ## then eliminate trials more than 3 MADs from the median
  RT$RT[is_outlier(RT$RT, abs_lim = c(.2, 1.5), mad_lim = 3)] <- NA
  
  # join RT data to trial data
  trial_data <- left_join(trial_info, RT, by = c("id", "trial")) %>%
    mutate(TLBS = get_tlbs(RT, congruent))
  
  #write trial data
  write_csv(trial_data,paste(save_path, "/", trial_data$id[1], ".csv", sep = ""))
  df
}
#************************************************************* Run Analysis
cl <- makeCluster(n_cores)
clusterEvalQ(cl, library(tidyverse))
clusterEvalQ(cl, library(itrak))
tlbs <- parLapply(cl, load_directory, process_dotprobe, save_path = tlbs_path, n_trial = n_trial)
stopCluster(cl)
#*********************************************************************************************
#*************************************************************************** Gaze Bias Summary
df_bias <- function(file_name, tlbs_folder, groupby){
  read_csv(file_name, col_types = cols_only(id = col_character(),
                                           trial = col_double(),
                                           trialType = col_character(),
                                           congruent = col_logical(),
                                           RT = col_double(),
                                           TLBS = col_double(),
                                           initial_bias = col_double(),
                                           final_bias = col_double(),
                                           total_bias = col_double())) %>%
    #mutate trial as integer
    mutate(trial = as.integer(trial)) %>%
    #group by nested value
    group_by(.dots = groupby) %>%
    #calculate values
    summarize(dp_bias = get_bs(RT, congruent),
              n_dp_valid = sum(!is.na(RT)),
              pct_dp_toward = sum(!is.na(TLBS) & TLBS > 0) / sum(!is.na(RT)),
              mean_dp_toward = mean(TLBS[!is.na(TLBS) & TLBS > 0]),
              mean_dp_away = -1 * mean(TLBS[!is.na(TLBS) & TLBS < 0]),
              var_dp_bias = sd(TLBS, na.rm = TRUE)
    )
}
#*************************************************************** nested by subject
groupby=list('id')
tlbs_directory <- paste(tlbs_path, list.files(tlbs_path), sep = "/")
subject_bias_summary <- map(tlbs_directory, df_bias, groupby=groupby) %>%
  reduce(bind_rows) %>% ungroup() %>%
  mutate_if(is.numeric, function(x) ifelse(is.nan(x), 0, x))
#identify whether nested by subject-level or trialType
subject_bias_summary$nested <- 'subject'
#create blank trialType for later merging
subject_bias_summary$trialType <- '.'
#*************************************************************** nested by subject, trialtype
groupby=list('id','trialType')
tlbs_directory <- paste(tlbs_path, list.files(tlbs_path), sep = "/")
trial_bias_summary <- map(tlbs_directory, df_bias, groupby=groupby) %>%
  reduce(bind_rows) %>% ungroup() %>%
  mutate_if(is.numeric, function(x) ifelse(is.nan(x), 0, x))
#drop any NA values
trial_bias_summary <- trial_bias_summary[!is.na(trial_bias_summary$trialType),]
#identify whether nested by subject-level or trialType
trial_bias_summary$nested <- 'trialType'
#************************************************************** Combine Tables, export to csv
bias_summary <- rbind(subject_bias_summary, trial_bias_summary)
write_csv(bias_summary, paste(summary_path, "/behavioral_bias", ".csv", sep = ""))
