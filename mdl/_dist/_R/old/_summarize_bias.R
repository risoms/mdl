rm(list=ls())
#******************************************************************** Imports
library(parallel); library(tidyverse); library(itrak);
#**************************************************************** Definitions
suppressPackageStartupMessages(library(tidyverse))
data_path <- "~/Desktop/R33-analysis-master/output"
load_path <- paste(data_path, "1_py/data", sep = "/")
tlbs_path <- paste(data_path, "2_tlbs", sep = "/")
gaze_path <- paste(data_path, "3_gazebias", sep = "/")
n_cores <- 4
n_trial <- 198
load_directory <- paste(load_path, list.files(load_path), sep = "/")
#*********************************************************************************************
#**************************************************************************************** TLBS
#run dotprobe
process_dotprobe <- function(load_path, save_path, n_trial){
  df <- read_csv(load_path, na = c(".", ""), guess_max = 999999,
                 col_types = cols_only(participant = col_character(), #participant
                                       TrialNum = col_integer(),
                                       sampleNum = col_integer(), #sampleNum
                                       timestamp = col_number(), #timestamp
                                       event = col_character(),
                                       marker = col_character(),
                                       trialType = col_character(),
                                       RT = col_number(),
                                       Key_Resp.acc = col_logical(), #Key_Resp.acc
                                       sg_fix_index = col_number(), #RIGHT_FIX_INDEX
                                       sg_fix_roi = col_character(), #RIGHT_INTEREST_AREAS
                                       LEmotion = col_character(), #LStim
                                       REmotion = col_character(), #RStim
                                       DotLoc = col_character() #DotStim
                                       ))
  
  # separate trial metadata from sample-measurement data
  itrak_data <- df %>% 
    select(id = participant, trial = TrialNum, time = timestamp, fixation = sg_fix_index,
  gaze_direction = sg_fix_roi, event = event, trialType, marker = marker, RT = RT) %>%
    ##convert categories "", 1, 2 to "Center", "Left", "Right"
    mutate(gaze_direction = factor(gaze_direction, levels = c("1", "2"), 
                                   labels = c("Left", "Right")))
  #get summary of trial level info
  trial_info <- df %>%
    ##add new variables
    mutate(dot_location = gsub(".$", "", DotLoc),
           emo_location = ifelse(LEmotion == "Neutral", "Right", "Left"),
           congruent = dot_location == emo_location) %>%
    
    ##select variables
    select(id = participant, trial = TrialNum, dot_location, trialType,
           emo_location, congruent, accurate = Key_Resp.acc) %>% distinct()
  
  # get sample frequency
  freq <- get_freq(itrak_data$time)
  
  # get RT
  RT <- itrak_data %>% 
    ##get unique trials
    distinct(trial, .keep_all = TRUE) %>%
    ##select variables
    select(id, trial, RT, trialType)
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
  
  # get gaze direction at time of dotprobe
  final_fix <- itrak_data %>% 
    filter(marker == "Dotloc Onset") %>%
    inner_join(trial_data, by = c("id", "trial")) %>%
    mutate(final_bias = ifelse(emo_location == gaze_direction, 1, -1),
           final_bias = ifelse(is.na(gaze_direction), 0, final_bias)) %>%
    select(id, trial, trialType, final_bias)
  
  itrak_data <- itrak_data %>%
    ## reduce data to the interval when the faces are presented
    filter(event == "Stim") %>%
    ## reduce data to fixation periods
    filter(!is.na(fixation)) %>%
    ## join to emo_location
    left_join(trial_data %>% select(id, trial, emo_location),
              by = c("id", "trial")) %>%
    mutate(emo_fixation = gaze_direction == emo_location & !is.na(gaze_direction),
           neu_fixation = gaze_direction != emo_location & !is.na(gaze_direction))
  #record number of valid fixations contained within a trial
  fixation_times <- itrak_data %>%
    group_by(id, trial) %>%
    dplyr::summarize(total_fixation = n()/freq,
              emo_fixation = sum(emo_fixation)/freq,
              neu_fixation = sum(neu_fixation)/freq)
  #record first face to receive fixation
  first_face <- itrak_data %>% 
    filter(!is.na(gaze_direction)) %>%
    group_by(id, trial) %>%
    dplyr::summarize(initial_bias = ifelse(emo_fixation[1], 1, -1))
  #join to trial data and compute bias score
  trial_data <- left_join(trial_data, fixation_times, by = c("id", "trial")) %>%
    left_join(first_face, by = c("id", "trial")) %>%
    left_join(final_fix, by = c("id", "trial")) %>%
    mutate(initial_bias = ifelse(is.na(initial_bias), 0, initial_bias),
           total_bias = emo_fixation - neu_fixation)
  #write trial data
  write_csv(trial_data,paste(save_path, "/", trial_data$id[1], ".csv", sep = ""))
  trial_data
}
#************************************************************* Run Analysis
cl <- makeCluster(n_cores)
clusterEvalQ(cl, library(tidyverse))
clusterEvalQ(cl, library(itrak))
gaze_bias <- parLapply(cl, load_directory, process_dotprobe, save_path = tlbs_path, n_trial = n_trial)
stopCluster(cl)
#*********************************************************************************************
#*************************************************************************** Gaze Bias Summary
summarize_bias <- function(file_name, tlbs_folder){
  read_csv(file_name, col_types = cols_only(id = col_character(),
                                           trial = col_double(),
                                           trialType = col_character(),
                                           congruent = col_logical(),
                                           RT = col_double(),
                                           TLBS = col_double(),
                                           initial_bias = col_double(),
                                           final_bias = col_double(),
                                           total_bias = col_double())) %>%
    mutate(trial = as.integer(trial)) %>%
    group_by(id, trialType) %>%
    summarize(dp_bias = get_bs(RT, congruent),
              n_dp_valid = sum(!is.na(RT)),
              pct_dp_toward = sum(!is.na(TLBS) & TLBS > 0) / sum(!is.na(RT)),
              mean_dp_toward = mean(TLBS[!is.na(TLBS) & TLBS > 0]),
              mean_dp_away = -1 * mean(TLBS[!is.na(TLBS) & TLBS < 0]),
              var_dp_bias = sd(TLBS, na.rm = TRUE),
              gaze_bias = mean(total_bias, na.rm = TRUE),
              init_gaze_bias = mean(initial_bias, na.rm = TRUE),
              final_gaze_bias = mean(final_bias, na.rm = TRUE),
              n_gaze_valid = sum(!is.na(total_bias)),
              n_gaze_toward = sum(!is.na(total_bias) & total_bias > 0) / sum(!is.na(total_bias)),
              pct_gaze_center = sum(!is.na(total_bias) & total_bias == 0) / sum(!is.na(total_bias)),
              mean_gaze_toward = mean(total_bias[!is.na(total_bias) & total_bias > 0]),
              mean_gaze_away = -1 * mean(total_bias[!is.na(total_bias) & total_bias < 0]),
              var_gaze_bias = sd(total_bias, na.rm = TRUE),
              dp_gaze_cor = cor(TLBS, total_bias, use = "pairwise", method = "spearman")
    )
}
#*************************************************************** Run Analysis
tlbs_directory <- paste(tlbs_path, list.files(tlbs_path), sep = "/")
bias_summary <- map(tlbs_directory, summarize_bias) %>%
  reduce(bind_rows) %>% ungroup() %>%
  mutate_if(is.numeric, function(x) ifelse(is.nan(x), 0, x))
#************************************************************** Export to csv
write_csv(bias_summary, paste(gaze_path, "/bias_summary", ".csv", sep = ""))
