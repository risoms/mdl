# See "bias.pdf" file for documentation of this script.

#***************** VARIABLES YOU MAY NEED TO CHANGE ***********************
data_path <- "C:/Users/ras3228/Box Sync/Box Sync/MDL Lab/MDL Projects/Projects/R56 Mood and Brain Study/Data/Eye tracking data/Dot-Probe Data"
load_folder <- "unprocessed_reports"
archive_folder <- "processed_reports"
save_folder <- "cleaned_data"
n_cores <- 4
n_trial = 192
#***************************************************************************

process_dotprobe <- function(load_path, save_path, archive_path, n_trial){
  df <- read_tsv(load_path, na = ".",
                 col_types = cols_only(RECORDING_SESSION_LABEL = "c",
                                       SAMPLE_INDEX = "i",
                                       SAMPLE_MESSAGE = "c",
                                       TIMESTAMP = "n",
                                       LEFT_FIX_INDEX = "i",
                                       RIGHT_FIX_INDEX = "i",
                                       LEFT_INTEREST_AREAS = "c",
                                       RIGHT_INTEREST_AREAS = "c",
                                       LFaceStim = "c",
                                       RFaceStim = "c",
                                       DotStim = "c",
                                       ACC = "l"))

  # determine which eye was not measured
  no_eye <- "RIGHT"
  if(all(is.na(df$LEFT_FIX_INDEX))) no_eye <- "LEFT"
  # drop columns for unmeasured eye
  df <- df %>% select(-starts_with(no_eye)) %>%
  # create trial number label
    arrange(TIMESTAMP) %>%
    mutate(trial = label_trial(sample = SAMPLE_INDEX,
                                marker = SAMPLE_MESSAGE,
                                event = "FaceStimOnset")) %>%
  # drop drift corrections
    filter(!is.na(trial))

  #check to make sure that the number of trials matches n_trails
  if(max(df$trial) != n_trial)
    stop(paste("Expecting ", n_trial, "; found ", check$`max(trial)`,
               sep = ""))

  # separate trial metadata from sample-measurement data
  itrak_data <- df %>% select(id = RECORDING_SESSION_LABEL,
                              trial,
                              message = SAMPLE_MESSAGE,
                              time = TIMESTAMP,
                              fixation = contains("FIX"),
                              gaze_direction = contains("AREA")) %>%
    mutate(gaze_direction = factor(gaze_direction,
                                   levels = c("[]", "[ 1 ]", "[ 2 ]"),
                                   labels = c("Center", "Left", "Right")))
  trial_info <- df %>%
    mutate(dot_location = gsub(".$", "", DotStim),
           emo_location = ifelse(grepl("NE", LFaceStim), "Right", "Left"),
           congruent = dot_location == emo_location,
           emo_valence = ifelse(grepl("HA", LFaceStim) |
                                  grepl("HA", RFaceStim), "Happy", "Sad")) %>%
    select(id = RECORDING_SESSION_LABEL,
           trial,
           left_face = LFaceStim,
           right_face = RFaceStim,
           emo_valence,
           dot_location,
           emo_location,
           congruent,
           accurate = ACC) %>% distinct()

  # get sample frequency
  freq <- get_freq(itrak_data$time)

  # get RT
  RT <- itrak_data %>% select(id, trial, message, time) %>%
    filter(message %in% c("Ending Recording", "FaceStimOffset")) %>%
    group_by(id, trial) %>% summarize(RT = (time[2] - time[1] - 500) / 1000)

  # assign missing values to incorrect trials
  RT$RT[!trial_info$accurate] <- NA

  # assign missing values to outliers
  ## first eliminate trials with RTs less than 0.2 s or more than 1.5 s
  ## then eliminate trials more than 3 MADs from the median
  RT$RT[is_outlier(RT$RT, abs_lim = c(.2, 1.5), mad_lim = 3)] <- NA

  # join RT data to trial data
  trial_data <- left_join(trial_info, RT, by = c("id", "trial"))

  # get TLBS
  rt_happy <- trial_data$RT
  rt_happy[trial_data$emo_valence == "Sad"] <- NA
  tlbs_happy <- get_tlbs(rt_happy,
                         congruent = trial_data$congruent)
  rt_sad <- trial_data$RT
  rt_sad[trial_data$emo_valence == "Happy"] <- NA
  tlbs_sad <- get_tlbs(rt_sad, congruent = trial_data$congruent)
  trial_data$TLBS <- tlbs_happy
  trial_data$TLBS[trial_data$emo_valence == "Sad"] <-
    tlbs_sad[trial_data$emo_valence == "Sad"]

  # get gaze direction at time of dot probe
  final_fix <- itrak_data %>% filter(message == "FaceStimOffset") %>%
    mutate(final_bias = ifelse(trial_data$emo_location == gaze_direction,1,-1),
           final_bias = ifelse(gaze_direction == "Center", 0, final_bias)) %>%
  select(id, trial, final_bias)

  # group itrak data by trial
  itrak_data <- itrak_data %>%
    group_by(trial) %>%
    # zero time to the "FaceStimOnset" marker
    mutate(time = zero_onset(time, message, "FaceStimOnset")) %>%
    ungroup() %>%
    # reduce data to the interval when the faces are presented
    clip_trials(trial, time, start = 2, stop = 1000) %>%
    # reduce data to fixation periods
    filter(!is.na(fixation)) %>%
    # join to emo_location
    left_join(trial_data %>% select(id, trial, emo_location)) %>%
    mutate(emo_fixation = gaze_direction == emo_location,
           neu_fixation = gaze_direction != emo_location &
             gaze_direction != "Center")
  #record number of valid fixations contained within a trial
  fixation_times <- itrak_data %>%
    group_by(id, trial) %>%
    summarize(total_fixation = n()/freq,
              emo_fixation = sum(emo_fixation)/freq,
              neu_fixation = sum(neu_fixation)/freq)
  #record first face to receive fixation
  first_face <- itrak_data %>% filter(gaze_direction != "Center") %>%
    group_by(id, trial) %>%
    summarize(initial_bias = ifelse(emo_fixation[1], 1, -1))
  #join to trial data and compute bias score
  trial_data <- left_join(trial_data, fixation_times, by = c("id", "trial")) %>%
    left_join(first_face, by = c("id", "trial")) %>%
    left_join(final_fix, by = c("id", "trial")) %>%
    mutate(initial_bias = ifelse(is.na(initial_bias), 0, initial_bias),
           total_bias = emo_fixation - neu_fixation)
  #write trial data
  write_csv(trial_data,
            paste(save_path, "/", trial_data$id[1], ".csv", sep = ""))
  #move report from unprocessed to processed
  file.rename(load_path,
              paste(archive_path, "/", trial_data$id[1], ".tsv", sep = ""))
  trial_data
}

#=======================MAIN========================
library(tidyverse); library(itrak); library(parallel)
load_path <- paste(data_path, load_folder, sep = "/")
load_paths <- paste(load_path, list.files(load_path), sep = "/")
archive_path <- paste(data_path, archive_folder, sep = "/")
save_path <- paste(data_path, save_folder, sep = "/")
if(length(load_paths) > 1){
  cl <- makeCluster(n_cores)
  clusterEvalQ(cl, library(tidyverse))
  clusterEvalQ(cl, library(itrak))
  gaze_bias <- parLapply(cl, load_paths, process_dotprobe,
                         save_path = save_path, archive_path = archive_path,
                         n_trial = n_trial)
  stopCluster(cl)
} else {
  gaze_bias <- process_dotprobe(load_paths, save_path, archive_path, n_trial)
}

