rm(list=ls());
#clear cache: .rs.restartR();
#garbage collection: gc();
#******************************************************************** shortcuts
#delete variables: rm(x,z,zz,j,lm_,qq,rf)
#extract variables from plot: ggplot_build(plot)
#******************************************************************** Imports
#conda install -c r r-devtools
#install.packages("jtools")
library(tidyverse);library(corrplot);library(jtools);library(broom);library(broom.mixed);
library(lme4);library(ggplot2);library(lattice);library(car);library(lmerTest);
#**************************************************************** Definitions
suppressPackageStartupMessages(library(tidyverse))
task_type = "eyetracking"
data_path <- "~/Desktop/R33-analysis-master/output"
if (task_type == "eyetracking"){
  bias_path <- paste(data_path, "3_bias", "eyetracking_bias.csv",sep = "/")
} else {
  bias_path <- paste(data_path, "3_bias", "behavioral_bias.csv",sep = "/")
}
metadata_path <- paste(data_path, "4_analysis", "subject_metadata.csv",sep = "/")
cesd_path <- paste(data_path, "4_analysis", "cesd_rrs.csv",sep = "/")
image_path <- paste(data_path, "4_analysis",sep = "/")
#***************************************************************************************load data
# metadata
metadata_df <- read.csv(metadata_path)
# gaze_bias
gazebias_df <- read.csv(bias_path) %>% rename(participant='id')
# CESD and RRS
cesd_df <- read.csv(cesd_path)
#merge data 
df <- list(gazebias_df, cesd_df, metadata_df) %>% reduce(left_join, by = "participant")
##list variables
str(df)
#************************************************************** format data
#participant - to numeric
df$participant <- as.numeric(df$participant)

#is_eyetracking - to bool
df$is_eyetracking <- factor(df$is_eyetracking)

#os - to categorical
df$os <- factor(df$os)
categories <- unique(df$os)

#gpu_type - to categorical
df$gpu_type <- factor(df$gpu_type)
categories <- unique(df$gpu_type) 

#webcam_device - to categorical
#df$webcam_type <- factor(df$webcam_type)
#categories <- unique(df$webcam_type) 

#webcam width - to categorical
df$webcamWidth.f <- factor(df$webcamWidth)
categories <- unique(df$webcamWidth) 

#browser - to categorical
df$browser <- factor(df$browser)
categories <- unique(df$browser) 

#cesd - to categorical
df$trialType_ <- df$trialType
df$trialType <- ifelse(df$trialType == "iaps", 1, 0)

#webcam - to numeric
df$webcamWidth <- as.numeric(as.character(df$webcamWidth))

#cesd - to categorical
df$cesd_group_ <- cut(df$cesd_score, breaks=c(-Inf, 15, Inf), labels=c("low","high"))
df$cesd_group <- ifelse(df$cesd_group_ == "high", 1, 0)
categories <- unique(df$cesd_group) 
summary(df$cesd_score)
summary(df$cesd_group)

#************************************************************** Correlation
#dotprobe_bias and gaze_bias
cor(df$dp_bias, df$gaze_bias)
cor.test(df$dp_bias, df$gaze_bias)

#cesd
#dotprobe_bias and cesd_score
cor(df$dp_bias, df$cesd_score)
cor.test(df$dp_bias, df$cesd_score)

#dotprobe_bias and cesd_score
cor(df$dp_bias, df$cesd_score)
cor.test(df$dp_bias, df$cesd_score)

#matrix ##type: layout, method: visualization
##subset
matrix <- subset(df, select = c(dp_bias, gaze_bias, n_dp_valid, n_gaze_valid, cesd_group,
                                 mean_gaze_away, mean_gaze_toward, var_gaze_bias,
                                 luminance, devicePixelRatio))
##list variables
str(matrix)

#run matrix
col <- colorRampPalette(c("#BB4444", "#EE9988", "#FFFFFF", "#77AADD", "#4477AA"))
# matrix_plot = corrplot::corrplot(cor(matrix), method="color", col=col(200), type="full", diag= FALSE,
#                                  addCoef.col = "black", tl.col="black", mar=c(0,0,0,0),
#                                  cl.ratio = 0.2, cl.align = "l")
# png(filename=paste(data_path, "4_analysis","img","corr.png",sep = "/"), width = 720, height = 720, units = "px")
# plot(matrix_plot)
dev.off()
#************************************************************** density plot
##subset
dfd <- subset(df, select = c(dp_bias, gaze_bias, n_dp_valid, n_gaze_valid, cesd_group, trialType, trialType_,
                             mean_gaze_away, mean_gaze_toward, var_gaze_bias, final_gaze_bias))

p <- ggplot(dfd, aes(x=final_gaze_bias)) + 
  theme(aspect.ratio=1) + 
  geom_histogram(aes(y =..density..),
                 bins = 20,
                 fill = "#FF0000",
                 colour = "white",
                 alpha = 0.65) +
  geom_density(kernel = "gaussian", trim = FALSE, bw = "nrd")
p
#****************************************************************************************
#****************************************************************************************dwell-time
rm(list=ls());
library(tidyverse);library(jtools);library(broom);library(broom.mixed);library(ggplot2);
#-----------repeated measures anova model
#-----------load data
df_ <- read.csv(file='~/Desktop/R33-analysis-master/output/4_analysis/dwell_data.csv', header=TRUE)

#-----------set as factors
df_$aoi = factor(df_$aoi)
df_$trialType <- factor(df_$trialType)
df_$cesd_group <- factor(df_$cesd_group)
df_$participant <- factor(df_$participant)

#-----------run model
#version 1 #use if estimated effects are not balanced
lmer_ <- lmer(dwell_time ~ cesd_group + aoi + trialType + (1|participant), data=df_)
aov1 <- stats::anova(lmer_)
table1 <- broom::tidy(aov1)

#--------Estimated Marginal Means
#EMM's are based on a reference grid consisting of all combinations of factor levels, with each covariate set to its average (by default).
#https://cran.r-project.org/web/packages/emmeans/vignettes/basics.html
library(emmeans);
# Estimated Marginal Means (Least-Squares Means) of all factor levels
pair_ <- emmeans::emmeans(lmer_, c("aoi", "trialType", "cesd_group"), type = "response", adjust = "tukey")
# Comparison of Differences Between Levels of Factor
pairs(pair_)
compare_ <- summary(emmeans::as.glht(pairs(pair_)), test=adjusted("free")) %>% broom::tidy()
# plot
emmip(pair_, ~ aoi | trialType, CIs = TRUE) +
  geom_point(aes(x = factor(aoi), y = dwell_time), data = df_, pch = 2, color = "blue")
# plot 2
## https://stackoverflow.com/questions/21436230/r-ggplot2-ezplot-plotting-3x3-rm-anova-design-per-quantile-of-covariate-with-er
ggplot(df_, aes(x=aoi, y=dwell_time, colour=trialType, group=trialType, linetype=trialType, shape=trialType)) + 
  stat_summary(fun.data="mean_cl_boot", geom="errorbar", conf.int=90) + 
  stat_summary(fun.y="mean", geom="point", size=2) + 
  stat_summary(fun.y="mean", geom="line") + 
  theme_bw()
# plot 3
ggplot(df_, aes(x=aoi, y=dwell_time, fill=trialType)) + 
  facet_grid(aes(trialType)) +
  geom_boxplot() + 
  theme_bw()

#--------qqplot
ggplot(lmer_) + 
  stat_qq(aes(sample = .resid, colour = factor(trialType))) + 
  geom_abline(linetype = "dotted") + 
  theme_bw()

#--------residual vs fitted
ggplot(lmer_, aes(.fitted, .resid)) +
  #(red=0, green=1)
  geom_point(aes(colour = factor(trialType))) +
  #horizontal intercept
  geom_hline(yintercept = 0) +
  #loess smoothing curve
  geom_smooth(se = FALSE) +
  scale_color_manual(values=c("#dc3545","#5b77aa"))
  # + theme(legend.position="none")

#****************************************************************************************
#**********************************************absolute difference in stimulus/dotloc presentation time
#y: diff_stim, diff_dotloc
#----------get data
diff_path <- paste(data_path, "4_analysis/", "onset_data.csv",sep = "/")
diff_df <- read.csv(file=diff_path, header=TRUE)

#-----------model
##gender #samples too small
diff_df = diff_df[(!diff_df$gender=='other'),]
##os #samples too small
diff_df = diff_df[(!diff_df$os=='cos'),]
##race #samples too small
diff_df <- diff_df[!(diff_df$race=="Black or African American" | diff_df$race=="Two or more races" |
                     diff_df$race=="None of the above" | diff_df$race=="American Indian or Alaska Native"),]

#set as factors
#critical
diff_df$os = factor(diff_df$os)
diff_df$race <- factor(diff_df$race)
diff_df$gender <- factor(diff_df$gender)
diff_df$trialType <- factor(diff_df$trialType)
diff_df$participant <- factor(diff_df$participant)
##other
diff_df$blockNum <- factor(diff_df$blockNum)
diff_df$eye_color <- factor(diff_df$eye_color)
diff_df$gpu_type <- factor(diff_df$gpu_type)
diff_df$webcam_brand <- factor(diff_df$webcam_brand)
diff_df$monitorWidth <- factor(diff_df$monitorWidth)
diff_df$is_calibrated <- factor(diff_df$is_calibrated)
diff_df$devicePixelRatio <- factor(diff_df$devicePixelRatio)

#----------results
diff_describe <- psych::describeBy(diff_df, group=c("participant"), mat=TRUE)
unique(diff_df$race)
unique(diff_df$gender)
unique(diff_df$gpu_type)
unique(diff_df$os)
#summary(diff_df)
str(diff_df)

#----------model
f <- diff_dotloc ~ os * race * gender * trialType * luminance * 
                  TrialNum_ + (1|participant) + (TrialNum_ | participant)
#random effects: (1|participant)
##(1|participant): observations are clustered within each participant
poisson_ <- glmer.nb(f,
                 data = diff_df,
                 nAGQ=0, control=glmerControl(optimizer="nloptwrap"))
#summary(poisson_)
poisson_df = broom::tidy(poisson_)

#----------plot
#1 - category plot
# cat_plot(poisson_, pred = "trialType", modx = "os", plot.points = TRUE)

#2 - trend line
# https://medium.com/@alexhallam6.28/longitudinal-analysis-and-missing-data-a-short-example-in-r-86a7bfd9fa57
# ggplot(diff_df, mapping = aes(x = TrialNum, y = diff_dotloc)) +
#   geom_line(aes(colour=participant)) +
#   geom_point()

#3 - histogram
ggplot(diff_df, aes(diff_stim, fill = trialType)) +
  geom_histogram() + 
  scale_x_log10()

#options(scipen=999)
#****************************************************************************************
#************************************************************************************** anova
#notes: http://www.cookbook-r.com/Statistical_analysis/ANOVA/
#y: 'final_gaze_bias', 'dp_bias', 'm_rt', 'accuracy', 'm_diff_stim', 'm_diff_dotloc', 'luminance'
#x (between subjects): 'os', 'monitorWidth', 'race', 'gender'
#x (within subjects): trialType

#----------get data
diff_path <- paste(data_path, "4_analysis/", "final_data.csv",sep = "/")
df_anova <- read.csv(file=diff_path, header=TRUE)

#-----------subset
dfm <- subset(df_anova, select = c(dp_bias, gaze_bias, var_gaze_bias, final_gaze_bias,
                                  rrs_brooding, cesd_group, cesd_score,
                                  participant, nested, trialType_,
                                  race, gender,
                                  accuracy, m_rt,
                                  m_diff_stim, m_diff_dotloc,
                                  luminance, devicePixelRatio, os, monitorWidth))

#-----------collapse by trial type
#nested
dfm$nested = factor(dfm$nested)
df_ <- dfm %>% 
  filter(nested == 'trialType')

#-----------drop participants
df_ <- df_[(!df_$luminance<=0),]
df_ <- df_[(!df_$os=='cos'),]
df_ <- df_[(!df_$gender=='other'),]
df_ <- df_[!(df_$race=="Black or African American" | df_$race=="Two or more races" |
               df_$race=="None of the above" | df_$race=="American Indian or Alaska Native"),]

#-----------set as factors
df_$os = factor(df_$os)
df_$race <- factor(df_$race)
df_$gender <- factor(df_$gender)
df_$trialType <- factor(df_$trialType_)
df_$cesd_group <- factor(df_$cesd_group)
df_$participant <- factor(df_$participant)
df_$monitorWidth <- factor(df_$monitorWidth)
df_$devicePixelRatio <- factor(df_$devicePixelRatio)
###results
unique(df_$trialType)
#summary(df_)
str(df_)

#-----------model
lmer_ <- lmer(dp_bias ~ os + monitorWidth + gender + trialType +
              (1|participant), data=df_)
model <- anova(lmer_)
#tidy
#summary(model)
model_df <- broom::tidy(model)

#-----------creating robust dataframe from model (including raw data)
robust <- broom::augment(lmer_) %>% 
  subset(select = c(participant, trialType, .resid, .fitted)) %>%
  as.data.frame.matrix()

#-----------getting x,y coordinates for qqplot
gg <- ggplot(lmer_) + 
  stat_qq(aes(sample = .resid, colour = factor(cesd_group))) + 
  geom_abline(linetype = "dotted") + 
  theme_bw()

gg <- ggplot_build(gg)[["data"]][[1]] %>% 
  subset(select = c(sample, theoretical)) %>%
  as.data.frame.matrix()
#add column for merging
gg$.resid <- gg$sample

#-----------merge datasets
dt <- merge(robust, gg, by.x=".resid", by.y=".resid", all.x = TRUE)

#-----------creating predictions from model
# df_$predictions <- predict(lmer_)

#-----------assumptions
#0) balanced 
tally(lmer_,data=df_)

#1) Homogeneity of variance (homoskedasticity)
#levene test
levene_ <- leveneTest(lmer_, data=df_)
#boxplot
# boxplot(residuals(lmer_) ~ df_$race + df_$os+ df_$gender)
#plot
# plot(lmer_)
#residuals vs fitted plot 
ggplot(fortify(lmer_, df_), aes(.fitted, .resid)) +
  #(red=0, green=1)
  geom_point(aes(colour = factor(cesd_group))) +
  #horizontal intercept
  geom_hline(yintercept = 0) +
  #loess smoothing curve
  geom_smooth(se = FALSE) +
  scale_color_manual(values=c("#dc3545","#5b77aa")) +
  theme(legend.position="none")

#2) Normal distributions (normality)
#shapiro
shapiro_ <- shapiro.test(df_$residuals)
#qq plot
ggplot(lmer_) +
  stat_qq(aes(sample = .resid, colour = factor(trialType))) +
  stat_qq_line(aes(sample = .resid)) +
  scale_color_manual(values=c("#dc3545","#5b77aa")) +
  theme(legend.position="none")
#qq plot with annotation
ggplot(dt, aes(theoretical, sample, colour=factor(trialType))) +
  geom_point(size=1) +
  geom_text(aes(x=theoretical, y=sample, label=participant)) +
  stat_qq_line(aes(sample = sample)) +
  scale_color_manual(values=c("#dc3545","#5b77aa")) +
  theme(legend.position="none")

#options(scipen=999)
#**************************************************************************************regression
##subset
dfm <- subset(df, select = c(dp_bias, gaze_bias, rrs_brooding,
             n_dp_valid, n_gaze_valid, cesd_group, cesd_score, trialType, trialType_,
             mean_gaze_away, mean_gaze_toward, var_gaze_bias, final_gaze_bias, participant, nested,
             luminance, devicePixelRatio, os, windowSize,
             Stim_onset, Dotloc_onset))
#drop any NA values
dfm <- dfm[!is.na(dfm$cesd_group),]

#drop participants
#df_ <- df_[(!df_$participant==91),]

#convert variables as factor
##devicePixelRatio
dfm$devicePixelRatio <- factor(dfm$devicePixelRatio)
categories <- unique(dfm$devicePixelRatio)

##os #drop os=="Chrome OS"; samples too small
dfm <- dfm[(!dfm$os=='cos'),]
dfm$os <- factor(dfm$os)
categories <- unique(dfm$os)

##participant
dfm$participant <- factor(dfm$participant)
categories <- unique(dfm$participant)

##windowSize
dfm$windowSize <- factor(dfm$windowSize)
categories <- unique(dfm$windowSize)

#view variables
str(dfm)
summary(dfm)

#************************************************************linear regression 1
#filter for nested event
df_ <- dfm %>% 
  filter(nested == 'subject')

#-------------------------model
ln1 <- glm(cesd_group ~ gaze_bias*log(n_gaze_valid), data=df_)
#tidy
ln1_df = broom::tidy(ln1)
#-------------------------------------plots
#-----------check for normality
##probability plot (qq)
#plot 1
ggplot(ln1) +
  stat_qq(aes(sample = .resid)) +
  stat_qq_line(aes(sample = .resid))
#-----------residuals vs fitted
#This residuals plot is being used to measure heteroscedasticy. 
#If the plots are dispersed in a random-like pattern then a linear
#regression might be a good model for this data.
ggplot(fortify(ln1, df_), aes(.fitted, .resid)) +
  geom_point(aes(colour = factor(cesd_group))) +
  geom_hline(yintercept = 0) +
  geom_smooth(se = FALSE)
#-----------cooks distance
plot(ln1, which = 4, cook.levels=cutoff)
ggplot(fortify(ln1, df_), aes(seq_along(.cooksd), .cooksd)) +
  geom_bar(stat = "identity", position = "identity") +
  geom_text(aes(label=ifelse((.cooksd>.2),participant,"")),
            hjust=-0.1,vjust=-0.1,size=3) +
  geom_hline(yintercept=.2,linetype=4,colour="orange")

#************************************************************linear regression 2
#using nested == 'trialType', we will have two samples per subject
#filter for nested event
#measuring for gaussian distribution (continous y). Note: if measuring binomial, then use glmer.
df_ <- dfm %>% 
  filter(nested == 'trialType')
#-------------------------------------model
ln2 <- lmer(cesd_score ~ cesd_score * dp_bias + (1|participant), data=df_)
#tidy
ln2_df = broom::tidy(ln2)
#-------------------------------------plots
#-----------check for normality
##probability plot (qq)
qqnorm(resid(ln2))
qqline(resid(ln2),col = 2,lwd=2,lty=2)

#************************************************************mixed model regression
#filter for nested event
df_ <- dfm %>% 
  filter(nested == 'trialType')

#check if there are any na's that might interfere with model
sapply(X = df_, FUN = function(x) sum(is.na(x)))
#--------------------model
#options(scipen=999)
mixed <- glmer(factor(cesd_group) ~ dp_bias:n_dp_valid + gaze_bias:log(n_gaze_valid) + 
                 (1|participant), family=binomial(link="logit"), data=df_)
#tidy
mixed_df = broom::tidy(mixed)
#--------------------check for normality
##probability plot
qqnorm(resid(mixed))
qqline(resid(mixed),col = 2,lwd=2,lty=2)
#********************************************************************plot

#********************************************************************debugging
#how to extract data from return (inside a function)
# logit_output <- logit_(df_)
# logit_df = logit_output[[1]]
# logit_model = logit_output[[2]]







#********************************************************************test
#-----------load data
path <- "/Users/mdl-admin/Desktop/mdl-R33-analysis/output/analysis/html/model/logit/dp_bias/csv/"
df <- read.csv(file=file.path(path, 'logit.csv'), header=TRUE)

#----normalize trial to [0,1] (recommended by Jason)
df$TrialNum <- lapply(df$TrialNum, function(x){((x - 0)/(197 - 0))})

#----set type
# set as factor
df$os <- factor(df$os)
df$trialType <- factor(df$trialType)
df$participant <- factor(df$participant)
# set trial as numeric (recommended by Jason)
df$TrialNum <- as.numeric(df$TrialNum)

#-----------run logistic regression
model <- glmer(cesd_group ~ dp_bias + trialType + TrialNum + (1+TrialNum|participant), weights=n_dp_valid, 
               family=binomial(link="logit"), data=df, nAGQ=0)

#-----------getting x,y coordinates for qqplot
#create plot
gg <- ggplot(model) + 
  stat_qq(aes(sample = .resid, colour = factor(trialType))) + 
  geom_abline(linetype = "dotted") + 
  theme_bw()
#convert to dataframe
gg <- ggplot_build(gg)[["data"]][[1]] %>% 
  subset(select = c(sample, theoretical)) %>%
  as.data.frame.matrix()

#-----------creating robust dataframe from model
#(including raw data, residuals vs fitted)
robust <- broom::augment(model) %>% 
  subset(select = c(participant, trialType, .resid, .fitted)) %>%
  as.data.frame.matrix()

#-----------merge robust and qq dataframe
dt <- merge(robust, gg, by.x=".resid", by.y="sample", all.x = TRUE)

#-----------convert model to dataframe
table <- broom::tidy(model)
#plot
#devtools::install_github("strengejacke/ggeffects")
library(ggeffects)
plot(ggpredict(result, c("os", "trialType")))




