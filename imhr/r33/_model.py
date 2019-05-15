#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
| @purpose: Run statistical models for analysis.  
| @date: Created on Sat May 1 15:12:38 2019  
| @author: Semeon Risom  
| @email: semeon.risom@gmail.com  
| @url: https://semeon.io/d/R33-analysis  
"""

# available classes and functions
__all__ = ['Model']

# required external libraries
__required__ = ['rpy2','pandas']

# global
from pdb import set_trace as breakpoint
import os, re
import datetime

# rpy2
#set path
os.environ["R_HOME"] = "/Library/Frameworks/R.framework/Versions/Current/Resources/"

# local libraries
if __name__ == '__main__':
	from .. import plot
	from .. import settings

class Model():
	"""Run statistical models for analysis."""
	def __init__(self, isLibrary=False):
		"""
		Initiate the mdl.r33.Model module.

        Parameters
        ----------
        isLibrary : :obj:`bool`
            Check if required libraries are available. Default `False`.
        """
        #check libraries
		if isLibrary:
			settings.library(__required__)

		# constants
		self.console = settings.console
		self.debug = settings.debug
		self.stn = settings.stn
		self.popover = settings.popover
		self.link = settings.link

	@classmethod
	def anova(cls, config, y, f, df, csv, path, effects, is_html=True):
		"""Run analysis of variance model using rpy2, seaborn and pandas.

		Parameters
		----------
		y : :obj:`str`
			Response variable.
		f : :obj:`str`
			Formula to use for analysis.
		df : :class:`pandas.DataFrame`
			Pandas dataframe of raw data.
		f : :obj:`str`
			R-compatiable formula.
		csv : :obj:`str`
			Name of generated CSV file to run analysis in R.
		path : :obj:`str`
			The directory path to save the generated files.
		effects : :obj:`list`
			List of main effects.
		is_html : :obj:`bool`
			Whether html should be generated.

		Returns
		-------
		model :  `rpy2.robjects.methods.RS4 <https://rpy2.github.io/doc/latest/html/robjects_oop.html?#rpy2.robjects.methods.RS4>`_
			Python representation of an R instance of class 'S4'.
		df_anova : :class:`pandas.DataFrame`
			Pandas dataframe of model output.
		get_anova : :class:`str`
			R script to run model.
		html : :class:`str`
			HTML output.

		Notes
		-----
		**Resources**
			- https://rpsychologist.com/r-guide-longitudinal-lme-lmer
			- https://sites.ualberta.ca/~lkgray/uploads/7/3/6/2/7362679/slides_-anova_assumptions.pdf
			- https://rpubs.com/tmcurley/twowayanova
			- https://rstudio-pubs-static.s3.amazonaws.com/158708_78d414c091fc47bd99f6f75e3bd8f4cb.html
			- https://m-clark.github.io/docs/mixedModels/anovamixed.html
			- http://dwoll.de/rexrepos/posts/anovaMixed.html
			- https://stats.stackexchange.com/questions/247582/repeated-measures-anova-in-r-errorsubject-vs-errorsubject-day
			- https://cran.r-project.org/web/packages/afex/vignettes/afex_anova_example.html#post-hoc-contrasts-and-plotting
			- http://www.let.rug.nl/nerbonne/teach/rema-stats-meth-seminar/presentations/Wieling-MixedModels-2011.pdf

		**Definition**:
			A test that allows one to make comparisons between the means of multiple groups of data, where two independent variables are considered. 

		**Assumptions of ANOVA**
			#. Normal distribution (normality)
				- Short: Samples are drawn from a normally distributed population (Q-Q Plot, Shapiro-Wilks Test)
				- Detailed Definition: Residuals in data are normally distributed.
			#. Homogeneity of variance (homoscedasticity)
				- Short: Variances are equal (or similar).
				- Detailed: Varience for a DV is constant across the sample. (residual vs fitted plot, Scale-Location plot, Levene's test)
			#. Independent observations
				- Samples have been drawn independently of each other. No analysis needed.

		**Hypothesis Interpretation**
			- **Null**: The means of all levels of an IV groups are equal.
			- **Alternative**: The mean of at least level of an IV is different.
		"""
		from rpy2.robjects import pandas2ri, r
		pandas2ri.activate()

		#----for timestamp
		_t0 = datetime.datetime.now()
		_f = debug(message='t', source="timestamp")
		console('model.anova(%s)'%(y), 'green')

		#----metadata
		source = "anova"

		#---------check if paths exist
		for path_ in [path, path+"/csv/", path+"/img/"]:
			if not os.path.exists(path_):
				os.makedirs(path_)

		#---------save data for access by R
		df.to_csv(path + "/csv/" + csv, index=None)

		#---------get number of remaining subjects (datapoints) used
		subject_anova = df.drop_duplicates(subset="participant", keep="first").shape[0]

		#---------run r
		#code
		get_anova = '\n'.join([
			'#!/usr/bin/env Rscript3.5.1',
			'rm(list=ls());',
			'#----library',
			'# core',
			'library(tidyverse);',
			'library(broom);',
			'# analysis',
			'library(lme4); library(lmerTest);',
			'# plot',
			'library(ggplot2);',
			'# estimated marginal means',
			'library(emmeans); library(multcomp);',
			'\t' + '',
			"#----repeated measures anova model", 
			'anova_ <- function(){',
			'\t' + "#----load data",
			'\t' + 'path <- "%s"'%(path + "csv/"),
			'\t' + "df <- read.csv(file=file.path(path, '%s'), header=TRUE)"%(csv),
			'\t' + '',
			'\t' + '#----set type',
			'\t' + 'df$trialType <- factor(df$trialType)',
			'\t' + 'df$cesd_group <- factor(df$cesd_group)',
			'\t' + 'df$participant <- factor(df$participant)',
			'\t' + '',
			'\t' + '#----run model',
			'\t' + 'lmer_ <- lmerTest::lmer(%s, data=df)'%(f),
			'\t' + 'aov_ <- stats::anova(lmer_)',
			'\t' + '',
			'\t' + '#----Estimated Marginal Means (Least-Squares Means) of all factor levels',
			'\t' + 'pair_ <- emmeans::emmeans(lmer_, c(%s),'%(','.join("'{0}'".format(x) for x in effects['main'].keys())),
			'\t' + '                          type = "response", adjust = "tukey")',
			'\t' + '# Comparison of Differences Between Levels of Factor',
			'\t' + 'lsmeans_ <- summary(emmeans::as.glht(pairs(pair_)), test=adjusted("free")) %>% ',
			'\t' + '   broom::tidy()',
			'\t' + '',
			'\t' + '#----getting x,y coordinates for qqplot',
			'\t' + '# create plot',
			'\t' + 'gg <- ggplot(lmer_) + ',
			'\t' + '  ggplot2::stat_qq(aes(sample = .resid, colour = factor(trialType))) + ',
			'\t' + '  ggplot2::geom_abline(linetype = "dotted")',
			'\t' + '',
			'\t' + '# convert to tibble',
			'\t' + 'gg <- ggplot_build(gg)[["data"]][[1]] %>% ',
			'\t' + '  dplyr::select(sample, theoretical)',
			'\t' + '',
			'\t' + '#----creating residuals tibble from model',
			'\t' + '# including raw data, residuals vs fitted)',
			'\t' + '# .resid=residuals, .fitted=predicted values .estimate=estimate of fixed effect',
			'\t' + 'residuals <- broom::augment(lmer_) %>% ',
			'\t' + '   dplyr::select(%s, .resid, .fitted)'%('participant' + ', ' + y + ', ' + ', '.join(effects['main'].keys())),
			'\t' + '',
			'\t' + '#----merge residuals and qq tibble',
			'\t' + 'residuals <- as.data.frame(merge(x=residuals, y=gg, by.x=".resid", by.y="sample", all.x = TRUE))',
			'\t' + '',
			'\t' + '#----prepare data for export',
			'\t' + '# convert model output to tibble',
			'\t' + 'output <- broom::tidy(aov_)',
			'\t' + '# convert model summary to tibble',
			'\t' + 'summary <- broom::glance(lmer_)',
			'\t' + '',
			'\t' + '#----return model output, model, residuals, lsmeans, model summary',
			'\t' + 'return(list(output, lmer_, residuals, lsmeans_, summary))',
		'}'])
		# load r function
		anova_r = r(get_anova)
		# run
		df_r = anova_r()

		#----extract df and model from rpy2
		df_anova = df_r[0]
		model = df_r[1]
		residuals = df_r[2]
		lsmeans = df_r[3]
		summary = df_r[4]

		#----clean data
		#rename
		df_anova = df_anova.rename(columns={'sumsq':'SS','meansq':'MS','statistic':'f','p.value':'Pr(>|f|)','DenDF':'DF','NumDF':'N'})
		# round p-value
		df_anova['Pr(>|f|)'] = df_anova[['Pr(>|f|)']].apply(lambda x: x.dropna().round(4).astype(str))
		#rename columns
		df_anova = df_anova.rename_axis("index", axis="columns")

		#----format summary
		summary = summary.rename_axis("index", axis="columns")
		summary = summary.to_html(index=True, index_names=True).replace('<table border="1" class="dataframe">',
		'<table id="table1" class="table '+source+' table-striped table-bordered hover dt-responsive nowrap"\ cellspacing="0" width="100%">')

		#----prepare metadata
		short_ = config['metadata']['short']
		long_ = config['metadata']['long']
		def_ = config['metadata']['def']
		cite_ = config['metadata']['cite']
		url_ = config['metadata']['url']
		var_ = config['metadata']['var']
		img_ = config['metadata']['img']

		#---------title, footnote, results
		title = '<b>Table 1.</b> Repeated Measures ANOVA for %s (<i>N</i> = %s).'%(long_[y], subject_anova)
		#----description
		description = ''.join([
			"<p><b>Type III Analysis of Variance Table with Satterthwaite's method</b> \
			[%a]. "%(link(name='anova', url='https://www.rdocumentation.org/packages/stats/versions/3.5.3/topics/anova')),
			"<div class='paragraph'>",
				"<div>The assumptions for the model are:</div>",
				'<ul class="number-list">',
					'<li>%s (%s).</li>'
					%(popover(name=long_['nd'],title=long_['nd'],description=def_['nd']),
					link(name='Q-Q Plot', url='#qq')),
					'<li>%s (%s).</li>'
					%(popover(name=long_['hv'],title=long_['hv'],description=def_['hv']),
					link(name='Residual vs Fitted Plot', url='#rf')),
					'<li>%s</li>'
					%(popover(name=long_['io'],title=long_['io'],description=def_['io'])),
				'</ul>',
			'</div>'
			"<div class='paragraph'>",
				"<div>The following post-hoc analysis were run:</div>",
				'<ul class="number-list">',
					'<li>%s.</li>'
					%(link(name='Estimated Marginal Means', url='#lsmean')),
					'<li>%s.</li>'
					%(link(name='Pairwise Comparison Plot', url='#boxplot')),
					'<li>%s.</li>'
					%(link(name='Q-Q Plot', url='#qq')),
					"<li>%s.</li>"
					%(link(name='Residual vs Fitted Plot', url='#rf')),
				'</ul>',
			'</div>'
		])

		#----results
		results = [
			'<div class="subtitle">Statistical Analysis</div>',
			"<p>",
			def_['exclude'],
			'We employed a repeated measures ANOVA using the anova() function in the <i>stats</i> R package \
			(%s; %s).'%(\
			popover(name=long_['R'], title=long_['R'], description=cite_['R']),
			popover(name=long_['anova'], title=long_['anova'], description=cite_['anova']))
		]

		#list of main effects    
		#"The fixed effects was %s,"%(def_['cesd_group'])
		if effects['main'] != None:
			#create qualifier #check if single random effect or multiple random effects
			qualifier = 'was included' if len(effects['main']) == 1 else 'were included'
			#start of statement
			results.append("For our model, ")
			#for each effect
			for idx, effect in enumerate(effects['main']):
				#if single item
				if len(effects['main']) == 1:
					results.append(" %s."%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
				#multiple items
				else:
					#last item
					if idx + 1 == len(effects['main']):
						results.append("and %s."%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
					else:
						results.append("%s,"%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
			#end  
			results.append("%s as main effects."%(qualifier))

		#list of random effects
		#stimulus (within subjects; %s, %s),"%(def_['iaps'], def_['pofa']),
		if effects['random'] != None:
			#create qualifier #check if single random effect or multiple random effects
			qualifier = 'was included' if len(effects['random']) == 1 else 'were included'
			#start of statement
			results.append("Random effects for")
			#for each effect
			for idx, effect in enumerate(effects['random']):
				#if single item
				if len(effects['random']) == 1:
					results.append(" %s."%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
				#multiple items
				else:
					#last item
					if idx + 1 == len(effects['random']):
						results.append("and %s."%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
					else:
						results.append("%s,"%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
			#end
			results.append('%s in the model to account for their respective variation in their slopes and intercepts.'%(qualifier))

		#outcome variable
		results.append('%s was used as the outcome measure.</p><p>'%(popover(name=long_[y],title=long_[y],description=def_[y])))

		# results
		results.append('For our analysis of %s, our results revealed'%(short_[y]))
		for idx, effect in enumerate(effects['main']):
			#get row
			row = df_anova[df_anova['term'].str.contains(effect)]
			#get term, B, se, z, p # lmer
			name = effect
			N_ = int(row['N'].values[0])
			DF_ = int(row['DF'].values[0])
			f_ = stn(row['f'].values[0])
			p_ = stn(row['Pr(>|f|)'].values[0])
			#significance
			if float(p_) <= 0.05:
				results.append('a statistically significant effect of')
			else:
				results.append('no statistically significant effect of')
			#if single item
			if len(effects['main']) == 1:
				results.append('%s (<a><i>F</i> (%s, %s) = %s, <i>p</i> = %s</a>).'%(short_[name], N_, DF_, f_, p_))
			#multiple items
			else:
				#last item
				if idx + 1 == len(effects['main']):
					results.append('%s (<a><i>F</i> (%s, %s) = %s, <i>p</i> = %s</a>).'%(short_[name], N_, DF_, f_, p_))
				else:
					results.append('%s (<a><i>F</i> (%s, %s) = %s, <i>p</i> = %s</a>),'%(short_[name], N_, DF_, f_, p_))
		## build results            
		results = ' '.join(results)

		# combine
		footnote = summary + re.sub(r'\s+', ' ', description + results).strip()

		#----create script
		script = ['<div class="code-container" style="display: none">' + '\n',
					'<div class="button-bar">'+'\n',
						'<a href="#" class="btn code hidden" source="copy" role="button">Copy</a>',
						'<a href="#" class="btn code hidden" source="download" role="button">Download</a>',
					'</div>'+'\n',
					'<pre class="line-numbers">' + '\n',
						#'<code id="editor" class="lang-r">'+'\n', #tinymce
						'<code contenteditable="true" class="lang-r" name=%s>'%(var_[y]) +'\n', #prismjs
							'%s'%(get_anova) + '\n',
						'</code>' + '\n',
					'</pre>' + '\n',
				'</div>\n']
		script = ''.join(script)

		#----plots and tables
		#lsmeans table
		#https://cran.r-project.org/web/packages/afex/vignettes/afex_anova_example.html
		try:         
			lsmeans = lsmeans.drop(['rhs'], 1)
			lsmeans['p.value'] = lsmeans[['p.value']].apply(lambda x: x.dropna().round(4).astype(str))
			lsmeans = lsmeans.rename_axis("index", axis="columns")
			lsmeans = lsmeans.rename(columns={'lhs':'Contrasts','std.error':'SE','statistic':'t','p.value':'Pr(>|t|)'})
		except:
			pass
		#create
		html_plots = []
		title_ = '<b>Table 2.</b> Pairwise Comparisons of Estimated Marginal Means.'
		footnote_ = def_['emm']
		html_plots.append({"title":title_,"footnote":footnote_,"anchor":"lsmean",'type':'table','df':lsmeans})

		# for each main effect (if categorical)
		for idx, effect in enumerate(effects['main']):
			# if categorical variable and not trialType
			if (effects['main'][effect] == 'categorical') and (effect != 'trialType'):
				#boxplot
				file = "%s_%s_boxplot.png"%(y, effect)
				path_ = path + "/img/" + file
				title_="Pairwise Comparisons Plot."
				footnote_ = 'This boxplot provides a comparison of %s and across both %s and %s stimuli. \
				Both IAPS and POFA plots were nornalized to allow direct comparison.'\
				%(short_[effect],
				popover(name=short_['iaps'], title=long_['iaps'], description=cite_['iaps'], image=img_['iaps']),
				popover(name=short_['pofa'], title=long_['pofa'], description=cite_['pofa'], image=img_['iaps']))
				# append and draw
				html_plots.append({"title":title_,"file":"%s"%(file),"footnote":footnote_, "anchor":"boxplot", 'type':'plot'})
				plot.boxplot(config=config, df=residuals, path=path_, x=effect, y=y, cat='bias')

		#probability (QQ) plot
		file = "%s_qq.png"%(y)
		path_ = path + "/img/" + file
		title_="Q-Q Plot (<a class='cat iaps'>iaps</a>, <a class='cat pofa'>pofa</a>)."
		footnote_ = def_['qq']
		html_plots.append({"title":title_,"file":"%s"%(file),"footnote":footnote_, "anchor":"qq", 'type':'plot'})
		plot.qq_plot(config=config, y=y, residuals=residuals, path=path_)

		#residuals vs fitted plot
		file = "%s_residuals.png"%(y)
		path_ = path + "/img/" + file
		title_="Residuals vs Fitted Plot (<a class='cat iaps'>iaps</a>, <a class='cat pofa'>pofa</a>)."
		footnote_ = def_['rvf']
		html_plots.append({"title":title_,"file":"%s"%(file),"footnote":footnote_, "anchor":"rf", 'type':'plot'})
		plot.residual_plot(config=config, y=y, residuals=residuals, path=path_)

		#save model and plot
		##create html
		html = None
		if is_html:
			path_ = path + '%s.html'%(y)
			html = plot.html(config=config, df=df_anova, raw_data=df, path=path_, source=source, title=title, name=y, script=script, 
					plots=html_plots, footnote=footnote, var=var_[y], short=short_[y], long=long_[y])
		#----end
		console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
		return model, df_anova, get_anova, html

	@classmethod
	def lmer(cls, config, y, f, df, exclude, csv, path, effects, is_html=True):
		"""Run linear mixed regression model, using rpy2, seaborn and pandas.

		Parameters
		----------
		y : :obj:`str`
			Response variable.
		f : :obj:`list` of :obj:`str`
			Formula to use for analysis.
		df : :class:`pandas.DataFrame`
			Pandas dataframe of raw data.
		f : :obj:`str`
			R-compatiable formula.
		exclude : :obj:`list`
			List of participants to be excluded.
		csv : :obj:`str`
			Name of generated CSV file to run analysis in R.
		path : :obj:`str`
			The directory path to save the generated files.
		effects : :obj:`list`
			List of main effects.
		is_html : :obj:`bool`
			Whether html should be generated.

		Returns
		-------
		model :  `rpy2.robjects.methods.RS4 <https://rpy2.github.io/doc/latest/html/robjects_oop.html?#rpy2.robjects.methods.RS4>`_
			Python representation of an R instance of class 'S4'.
		df_lmer : :class:`pandas.DataFrame`
			Pandas dataframe of model output.
		get_lmer : :class:`str`
			R script to run model.
		html : :class:`str`
			HTML output.

		Notes
		-----
		**Resources**
			- https://rpsychologist.com/r-guide-longitudinal-lme-lmer
			- https://stackoverflow.com/questions/47686227/poisson-regression-in-statsmodels-and-r
			- https://tsmatz.wordpress.com/2017/08/30/glm-regression-logistic-poisson-gaussian-gamma-tutorial-with-r/
			- https://stats.stackexchange.com/questions/311556/help-interpreting-count-data-glmm-using-lme4-glmer-and-glmer-nb-negative-binom
		"""
		from rpy2.robjects import pandas2ri, r
		pandas2ri.activate()

		#----for timestamp
		_t0 = datetime.datetime.now()
		_f = debug(message='t', source="timestamp")
		console('model.lmer(%s)'%(y), 'green')

		#----metadata
		source = 'onset'

		#-----exclude participants
		df_ex = df[~df['participant'].isin(exclude)]

		#----check if paths exist
		for path_ in [path, path + "csv/", path+"/img/"]:
			if not os.path.exists(path_):
				os.makedirs(path_)

		#----save data for access by R
		df_ex.to_csv(path + "csv/" + csv, index=None)

		#----get number of remaining subjects (datapoints) used
		subject_poisson = df_ex.drop_duplicates(subset="participant", keep="first").shape[0]

		#----model
		model_ = 'lmerTest::lmer(%s, data=df)'%(f)

		#----run r
		#code
		get_lmer = '\n'.join([
			'#!/usr/bin/env Rscript3.5.1',
			'rm(list=ls());',
			'#----library',
			'# core',
			'library(tidyverse);',
			'library(broom); library(broom.mixed);',
			'# analysis',
			'library(lme4); library(lmerTest);',
			'# plot',
			'library(ggplot2);',
			'# estimated marginal means',
			'library(emmeans); library(multcomp);',
			'\t' + '',
			"#----linear mixed model", 
			'lmer_ <- function(){',
			'\t' + "#----load data",
			'\t' + 'path <- "%s"'%(path + "csv/"),
			'\t' + "df <- read.csv(file=file.path(path, '%s'), header=TRUE)"%(csv),
			'\t' + '',
			'\t' + '#----drop data',
			'\t' + '# os #samples too small',
			'\t' + 'df <- df[(!df$os=="cos"),]',
			'\t' + '',
			'\t' + '#----normalize trial to [0,1] (recommended by Jason)',
			'\t' + 'df$TrialNum <- lapply(df$TrialNum, function(x){((x - 0)/(197 - 0))})',
			'\t' + '',
			'\t' + '#----set type', 
			'\t' + '# set as factor',
			'\t' + "df$os <- factor(df$os)",
			'\t' + "df$trialType <- factor(df$trialType)",
			'\t' + 'df$participant <- factor(df$participant)',
			'\t' + '# set trial as numeric (recommended by Jason)',
			'\t' + 'df$TrialNum <- as.numeric(df$TrialNum)',
			'\t' + '',      
			'\t' + '#----run model',
			'\t' + 'model <- %s'%(model_),
			'\t' + '',
			'\t' + '#----getting x,y coordinates for qqplot',
			'\t' + '# create plot',
			'\t' + 'gg <- ggplot(model) + ',
			'\t' + '  ggplot2::stat_qq(aes(sample = .resid, colour = factor(trialType))) + ',
			'\t' + '  ggplot2::geom_abline(linetype = "dotted") + ',
			'\t' + '  theme_bw()',
			'\t' + '# convert to tibble',
			'\t' + 'gg <- ggplot_build(gg)[["data"]][[1]] %>% ',
			'\t' + '  dplyr::select(sample, theoretical)',
			'\t' + '',
			'\t' + '#----creating residuals tibbles from model',
			'\t' + '# including raw data, residuals vs fitted',
			'\t' + '# .resid=residuals, .fitted=predicted values .estimate=estimate of fixed effect',
			'\t' + 'residuals <- broom::augment(model) %>% ',
			'\t' + '   dplyr::select(%s, .resid, .fitted)'%('participant' + ', sqrt.' + y + '., ' + ', '.join(effects['fixed'].keys())),
			'\t' + '',
			'\t' + '#----merge residuals and qq tibbles',
			'\t' + 'residuals <- merge(x=residuals, y=gg, by.x=".resid", by.y="sample", all.x = TRUE)',
			'\t' + '',
			'\t' + '#----prepare data for export',
			'\t' + '# convert output to tibble',
			'\t' + 'output <- broom.mixed::tidy(model)',
			'\t' + '# convert summary to tibble',
			'\t' + 'summary <- broom.mixed::glance(model)',
			'\t' + '',
			'\t' + '#----return model output, model, residuals, model summary',
			'\t' + 'return(list(output, model, residuals, summary))',
		'}'])
		#load r function
		lmer_r = r(get_lmer)
		#run
		df_r = lmer_r()

		#----extract df, model, summary from rpy2
		df_lmer = df_r[0]
		model = df_r[1]
		residuals = df_r[2]
		summary = df_r[3]

		#----clean data
		# drop row if it contains intercepts
		drop = ['sd__(Intercept)','	sd__TrialNum','cor__(Intercept).TrialNum','sd__Observation','sd__TrialNum']
		df_lmer = df_lmer[~df_lmer['term'].isin(drop)]
		#rename
		df_lmer = df_lmer.rename(columns={'estimate':'B','std.error':'SE','statistic':'t','p.value':'Pr(>|t|)'})
		# round 
		## B
		df_lmer['B'] = df_lmer[['B']].apply(lambda x: x.dropna().round(4).astype(str))
		## SE
		df_lmer['SE'] = df_lmer[['SE']].apply(lambda x: x.dropna().round(4).astype(str))
		## t
		df_lmer['t'] = df_lmer[['t']].apply(lambda x: x.dropna().round(4).astype(str))
		## p-value
		df_lmer['Pr(>|t|)'] = df_lmer[['Pr(>|t|)']].apply(lambda x: x.dropna().round(4).astype(str))
		#rename columns
		df_lmer = df_lmer.rename_axis("index", axis="columns")
		# drop column
		df_lmer = df_lmer.drop(['group','effect'], 1)

		#----format summary
		summary = summary.rename_axis("index", axis="columns")
		summary = summary.to_html(index=True, index_names=True).replace('<table border="1" class="dataframe">',
		'<table id="table2" class="table '+source+' table-striped table-bordered hover dt-responsive nowrap"\ cellspacing="0" width="100%">')

		#---------title, footnote, results
		short_ = config['metadata']['short']
		long_ = config['metadata']['long']
		def_ = config['metadata']['def']
		cite_ = config['metadata']['cite']
		url_ = config['metadata']['url']
		var_ = config['metadata']['var']

		#----title, description, and results
		title = '<b>Table 1.</b> Linear Mixed Model Regression for %s (<i>N</i> = %s).'%(long_[y], subject_poisson)
		description = ''.join([
			"<p><b>Linear Mixed Model Fit by REML (Laplace Approximation)</b> \
			[%a]. "%(link(name='lmer', url='https://www.rdocumentation.org/packages/lme4/versions/1.1-21/topics/lmer')),
			"This table summarizes effects on onset error rate with trial number, operating system, and stimulus.</p>",
			"<div class='paragraph'>",
				"<div>The assumptions for the model are:</div>",
				'<ul class="number-list">',
					'<li>%s (%s).</li>'
					%(popover(name=long_['rnd'],title=long_['rnd'],description=def_['rnd']),
					link(name='Q-Q Plot', url='#qq')),
					'<li>%s (%s).</li>'
					%(popover(name=long_['hv'],title=long_['hv'],description=def_['hv']),
					link(name='Residual vs Fitted Plot', url='#rf')),
					'<li>%s</li>'
					%(popover(name=long_['io'],title=long_['io'],description=def_['io'])),
				'</ul>',
			'</div>'
			"<div class='paragraph'>",
				"<div>The following post-hoc analysis were run:</div>",
				'<ul class="number-list">',
					'<li>%s.</li>'
					%(link(name='Individual Trend Plot', url='#itl')),
					'<li>%s.</li>'
					%(link(name='Group Trend Plot', url='#gtl')),
					'<li>%s.</li>'
					%(link(name='Q-Q Plot', url='#qq')),
					"<li>%s.</li>"
					%(link(name='Residual vs Fitted Plot', url='#rf')),
				'</ul>',
			'</div>'
		])

		#----results
		'''For statistical analysis, models were conducted with R, version 3.3.2 ([R]), using the <i>lme4</i> package [lmer]. To \
		analyze [y] we fit linear mixed-effects models using the <i>lmer</i> function. For our model, Group (NHI vs. PWA), Ambiguity 
		(ambiguous vs. unambiguous) and Context (DO-bias vs. SC-bias) were entered as fixed effects. Random intercepts and slopes 
		by participants and items were included for all fixed effects, as it was expected that participants and items would be 
		differently affected by the experimental manipulation. '''
		results = [
			'<div class="subtitle">Statistical Analysis</div>',
			"<p>",
			def_['exclude'],
			'We employed linear mixed effects models with random intercepts and slopes using the lmer() function in the <i>lme4</i> R package \
			(%s; %s).'%(\
			popover(name=long_['R'], title=long_['R'], description=cite_['R']),
			popover(name=long_['lmer'], title=long_['lmer'], description=cite_['lmer']))
		]

		#list of fixed effects    
		#"The fixed effects was %s,"%(def_['cesd_group'])
		if effects['fixed'] != None:
			#create qualifier #check if single random effect or multiple random effects
			qualifier = 'was included' if len(effects['fixed']) == 1 else 'were included'
			#start of statement
			results.append("For our model, ")
			#for each effect
			for idx, effect in enumerate(effects['fixed']):
				#if single item
				if len(effects['fixed']) == 1:
					results.append(" %s."%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
				#multiple items
				else:
					#last item
					if idx + 1 == len(effects['fixed']):
						results.append("and %s."%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
					else:
						results.append("%s,"%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
			#end  
			results.append("%s as fixed effects."%(qualifier))

		#list of random effects
		#stimulus (within subjects; %s, %s),"%(def_['iaps'], def_['pofa']),
		if effects['random'] != None:
			#create qualifier #check if single random effect or multiple random effects
			qualifier = 'was included' if len(effects['random']) == 1 else 'were included'
			#start of statement
			results.append("Random effects for")
			#for each effect
			for idx, effect in enumerate(effects['random']):
				#if single item
				if len(effects['random']) == 1:
					results.append(" %s."%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
				#multiple items
				else:
					#last item
					if idx + 1 == len(effects['random']):
						results.append("and %s."%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
					else:
						results.append("%s,"%(popover(name=long_[effect],title=long_[effect],description=def_[effect])))
			#end
			results.append('%s in the model to account for their respective variation in their slopes and intercepts.'%(qualifier))

		#outcome variable
		results.append('%s was used as the outcome measure.</p><p>'%(popover(name=long_[y],title=long_[y],description=def_[y])))

		# results
		results.append('For our analysis of %s, our results revealed'%(short_[y]))
		for idx, effect in enumerate(effects['fixed']):
			#get row
			row = df_lmer[df_lmer['term'].str.contains(effect)]
			#get term, B, se, z, p # lmer
			name = effect
			B_ = row['B'].values[0]
			se_ = row['SE'].values[0]
			p_ = row['Pr(>|t|)'].values[0]
			#significance
			if float(p_) <= 0.05:
				results.append('a statistically significant effect of')
			else:
				results.append('no statistically significant effect of')
			#if single item
			if len(effects['fixed']) == 1:
				results.append('%s (<a><i>t</i> = %s, <i>SE</i> = %s, <i>p</i> = %s</a>).'%(short_[name], B_, se_, p_))
			#multiple items
			else:
				#last item
				if idx + 1 == len(effects['fixed']):
					results.append('%s (<a><i>t</i> = %s, <i>SE</i> = %s, <i>p</i> = %s</a>).'%(short_[name], B_, se_, p_))
				else:
					results.append('%s (<a><i>t</i> = %s, <i>SE</i> = %s, <i>p</i> = %s</a>),'%(short_[name], B_, se_, p_))

		## build results 
		results = ' '.join(results)

		# combine
		footnote = summary + re.sub(r'\s+', ' ', description + results).strip()

		#---------plots
		#build plots
		plots = {}

		#---individual trend line
		clip = 250 if y=='diff_dotloc' else 200
		plots['individual'] = {}
		plots['individual']['type'] = 'plot'
		plots['individual']['file'] = '%s_individual'%(y)
		plots['individual']['path'] = path + "/img/" + "%s.png"%(plots['individual']['file'])
		plots['individual']['title'] = "Individual Trend Plot of the Difference Between Expected and True Onset Time \
		for %s (nested by subject:trial, <i>window</i> = 5)."%(long_[y])
		# footnote
		_exc = len(config['metadata']['subjects']['exclude'])
		_pct = (round(len(config['metadata']['subjects']['exclude'])/len(config['metadata']['subjects']['eyetracking']), 4)*100)
		plots['individual']['footnote'] = "Each line represents a participants individual %s across all trials. Participants with \
		Dotloc or Stimulus Onset Error median above 3SD (<i>n</i> = %s, %.1f%%) are drawn with a semi-opaque line. \
		The graph has been clipped at <i>y</i> = %s for displaying purposes."%(short_[y], _exc, _pct, clip)
		#---group trend plot
		plots['group'] = {}
		#---binned
		plots['group']["binned"] = {"bins":33,"ptype":'diff'}
		#---unbinned
		plots['group']["unbinned"] = {"bins":None,"ptype":'diff'}
		#both
		plots['group']['type'] = 'plot'
		plots['group']['file'] = '%s_group'%(y)
		plots['group']['path'] = path + "/img/" + "%s.png"%(plots['group']['file'])
		plots['group']['title'] = "Trend Plot of the Difference Between Expected and True Onset Time \
		for %s (nested by subject:trial)."%(long_[y])
		plots['group']['footnote'] = "Data is either unbinned (c,d) or binned into %s discrete evenly-sized groups (a,b). \
		The model is still fit using the original data. No participants have been excluded for this analysis. \
		The binned graph has been clipped at <i>y</i> = 1000 for displaying purposes."%(plots['group']["binned"]['bins'])
		# run
		#rename
		df = df.rename(columns={'onset>500':'onset_greater'})
		html_plots = plot.onset_diff_plot(config=config, df=df, meta=plots, drop=exclude, y=y, clip=clip)

		#---probability (QQ) plot
		file = "%s_qq.png"%(y)
		path_ = path + "/img/" + file
		title_="Q-Q Plot (<a class='cat iaps'>iaps</a>, <a class='cat pofa'>pofa</a>)."
		footnote_ = def_['qq']
		html_plots.append({"title":title_,"file":"%s"%(file),"footnote":footnote_, "anchor":"qq", 'type':'plot'})
		plot.qq_plot(config=config, y=y, residuals=residuals, path=path_)

		#---residuals vs fitted plot
		file = "%s_residuals.png"%(y)
		path_ = path + "/img/" + file
		title_="Residuals vs Fitted Plot (<a class='cat iaps'>iaps</a>, <a class='cat pofa'>pofa</a>)."
		footnote_ = def_['rvf']
		html_plots.append({"title":title_,"file":"%s"%(file),"footnote":footnote_, "anchor":"rf", 'type':'plot'})
		plot.residual_plot(config=config, y=y, residuals=residuals, path=path_)

		#---create script
		script = ['<div class="code-container" style="display: none">'+'\n',
					'<div class="button-bar">'+'\n',    
						'<a href="#" class="btn code hidden" source="copy" role="button">Copy</a>',
						'<a href="#" class="btn code hidden" source="download" role="button">Download</a>',
					'</div>'+'\n',
					'<pre class="line-numbers">'+'\n',
						#'<code id="editor" class="lang-r">'+'\n', #tinymce
						'<code contenteditable="true" class="lang-r" name=%s>'%(var_[y]) +'\n', #prismjs
						'%s\n'%(get_lmer),
						'</code>'+'\n',
					'</pre>'+'\n',         
				'</div>'+'\n']
		script = ''.join(script)

		#----html
		html = None
		if is_html:
			html_name = '%s_error'%(y)
			path_ = path + "%s.html"%(html_name)
			html = plot.html(config=config, df=df_lmer, raw_data=df, path=path_, source=source, title=title, name=html_name,
					script=script, plots=html_plots, footnote=footnote, var=var_[y], short=short_[y], long=long_[y])
		#----end
		console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
		return model, df_lmer, get_lmer, html

	@classmethod
	def logistic(cls, config, y, f, df, me, exclude, csv, path, is_html=True):
		"""Run logistic regression model, using rpy2, seaborn and pandas.

		Parameters
		----------
		y : :obj:`str`
			Response variable.
		f : :obj:`str`
			Formula to use for analysis.
		df : :class:`pandas.DataFrame`
			Pandas dataframe of raw data.
		me : :obj:`list` of :obj:`str`
			List of main effects.
		exclude : :obj:`list`
			List of participants to be excluded.
		csv : :obj:`str`
			Name of generated CSV file to run analysis in R.
		path : :obj:`str`
			The directory path to save the generated files.
		is_html : :obj:`bool`
			Whether html should be generated.

		Returns
		-------
		model :  `rpy2.robjects.methods.RS4 <https://rpy2.github.io/doc/latest/html/robjects_oop.html?#rpy2.robjects.methods.RS4>`_
			Python representation of an R instance of class 'S4'.
		df_logit : :class:`pandas.DataFrame`
			Pandas dataframe of model output.
		get_logit : :class:`str`
			R script to run model.
		html : :class:`str`
			HTML output.

		Notes
		-----
		**Resources**
			- https://rpsychologist.com/r-guide-longitudinal-lme-lmer
			- https://stats.idre.ucla.edu/r/dae/mixed-effects-logistic-regression/
			- https://www.statisticssolutions.com/assumptions-of-logistic-regression/
		"""
		from rpy2.robjects import pandas2ri, r
		pandas2ri.activate()

		#----for timestamp
		_t0 = datetime.datetime.now()
		_f = debug(message='t', source="timestamp")
		console('model.logistic(%s)'%(y), 'green')

		#----metadata
		source = 'logit'
		#get fullname
		full = y.replace("_", " ").title().replace("Cesd", "CESD")

		#-----exclude participants
		df = df[~df['participant'].isin(exclude)]

		#---------check if paths exist
		for path_ in [path, path+"/csv/", path+"/img/"]:
			if not os.path.exists(path_):
				os.makedirs(path_)

		#---------save data for access by R
		df.to_csv(path + "/csv/" + csv, index=None)

		#-------get number of remaining subjects (datapoints) used
		subjects_logit = df.drop_duplicates(subset="participant", keep="first").shape[0]

		#-------model
		#f = 'factor(cesd_group) ~ dp_bias + gaze_bias + final_gaze_bias + (1|participant)'
		# f = 'glmer(%s, \n\
		#            family=binomial(link="logit"), data=df, nAGQ=0)'%(f)
		f = 'lmer(%s, data=df)'%(f)

		#-------logit and confidence intervals to R data.frame
		##note: confidence intervals are based on the profiled log-likelihood function
		get_logit = '\n'.join([
			'#!/usr/bin/env Rscript3.5.1',
			'rm(list=ls());',
			'#----library',
			'# core',
			'library(tidyverse);',
			'library(broom);',
			'# analysis',
			'library(lme4);',
			'# plot',
			'library(ggplot2);',
			'# estimated marginal means',
			'library(emmeans); library(multcomp);',
			'\t' + '',
			'#----generalized linear mixed model',
			'logit_ <- function(){',
			'\t' + "#----load data",
			'\t' + 'path <- "%s"'%(path + "csv/"),
			'\t' + "df <- read.csv(file=file.path(path, '%s'), header=TRUE)"%(csv),
			'\t' + '',
			'\t' + '#----normalize trial to [0,1] (recommended by Jason)',
			'\t' + 'df$TrialNum <- lapply(df$TrialNum, function(x){((x - 0)/(197 - 0))})',
			'\t' + '',
			'\t' + '#----set type', 
			'\t' + '# set as factor',
			'\t' + "df$os <- factor(df$os)",
			'\t' + "df$trialType <- factor(df$trialType)",
			'\t' + 'df$participant <- factor(df$participant)',
			'\t' + '# set trial as numeric (recommended by Jason)',
			'\t' + 'df$TrialNum <- as.numeric(df$TrialNum)',
			'\t' + '',
			'\t' + '#----run model',
			'\t' + 'model <- %s'%(f),
			'\t' + '',
			'\t' + '#----odds ratio and confidence interval',
			'\t' + 'or_ci <- exp(cbind(OR=fixef(model), confint(model, parm="beta_", method="Wald"))) %>%',
			'\t' + '  cbind(term = rownames(.), .)',
			'\t' + 'rownames(or_ci) <- 1:nrow(or_ci)',
			'\t' + '',
			'\t' + '#----getting x,y coordinates for qqplot',
			'\t' + '# create plot',
			'\t' + 'gg <- ggplot(model) + ',
			'\t' + '  ggplot2::stat_qq(aes(sample = .resid, colour = factor(trialType))) + ',
			'\t' + '  ggplot2::geom_abline(linetype = "dotted") + ',
			'\t' + '  theme_bw()',
			'\t' + '# convert to tibble',
			'\t' + 'gg <- ggplot_build(gg)[["data"]][[1]] %>% ',
			'\t' + '  dplyr::select(sample, theoretical)',
			'\t' + '',
			'\t' + '#----creating residuals tibbles from model',
			'\t' + '# including raw data, residuals vs fitted',
			'\t' + '# .resid=residuals, .fitted=predicted values .estimate=estimate of fixed effect',
			'\t' + 'residuals <- broom::augment(model) %>% ',
			'\t' + '   dplyr::select(participant, trialType, cesd_group, .resid, .fitted)',
			'\t' + '',
			'\t' + '#----merge residuals and qq tibbles',
			'\t' + 'residuals <- merge(x=residuals, y=gg, by.x=".resid", by.y="sample", all.x = TRUE)',
			'\t' + '',
			'\t' + '#----prepare data for export',
			'\t' + '# convert model to tibble',
			'\t' + 'output <- broom::tidy(model)',
			'\t' + '# convert summary to tibble',
			'\t' + 'summary <- broom::glance(model)',
			'\t' + '',
			'\t' + '#----merge output with odds ratio and confidence interval',
			'\t' + 'output <- merge(x=output, y=or_ci, by.x="term", by.y="term", all.x = TRUE, sort = FALSE)',
			'\t' + '',
			'\t' + '#----return model output, model, residuals, model summary',
			'\t' + 'return(list(output, model, residuals, summary))',
		'}'])
		#----run r code
		#load r function
		logit_r = r(get_logit)
		#run
		df_r = logit_r()

		#----extract model dataframe, model, and residuals dataframe from rpy2
		df_logit = df_r[0]
		model = df_r[1]
		residuals = df_r[2]
		summary = df_r[3]

		#----clean data
		#rename
		df_logit = df_logit.rename(columns={'estimate':'B','std.error':'SE','statistic':'z','p.value':'Pr(>|z|)','97.5 %':'97.5%','2.5 %':'2.5%'})
		# round p-value
		df_logit['Pr(>|z|)'] = df_logit[['Pr(>|z|)']].apply(lambda x: x.dropna().round(4).astype(str))
		#merge ci
		df_logit['95% CI'] = df_logit[['2.5%', '97.5%']].values.tolist()
		# drop column
		df_logit = df_logit.drop(['group','effect','2.5%', '97.5%'], 1)
		# drop row if it contains intercepts
		# drop = ['sd_(Intercept).participant','sd_TrialNum.participant','cor_(Intercept).TrialNum.participant',
		#         'sd__(Intercept)','sd__TrialNum','cor__(Intercept).TrialNum']
		# df_logit = df_logit[~df_logit['term'].isin(drop)]

		#rename columns
		df_logit = df_logit.rename_axis("index", axis="columns")

		#----format summary
		summary = summary.rename_axis("index", axis="columns")
		summary = summary.to_html(index=True, index_names=True).replace('<table border="1" class="dataframe">',
		'<table id="table2" class="table '+source+' table-striped table-bordered hover dt-responsive nowrap"\ cellspacing="0" width="100%">')

		#---------title, footnote, results
		short_ = config['metadata']['short']
		long_ = config['metadata']['long']
		ref_ = config['metadata']['ref']
		def_ = config['metadata']['def']

		#-------title, footnote, and results
		title = '<b>Table 1.</b> Generalized Linear Mixed Model Regression for %s (N = %s).'%(full, subjects_logit)
		#description
		description = ''.join([
			"<p><b>Generalized Linear Mixed Model Fit by Maximum Likelihood (Adaptive Gauss-Hermite Quadrature)</b> \
			[<a class='anchor', href='https://www.rdocumentation.org/packages/lme4/versions/1.1-21/topics/glmer'>glmer</a>]. ",
			"This table summarizes effects on CESD score with trial number, bias score, and stimulus.</p>",
			"<div class='paragraph'>",
				"<div>The assumptions for the model are:</div>",
				'<ul class="number-list">',
					'<li>%s (<a href="#qq" class="anchor">Q-Q Plot</a>).</li>'%(def_['nd']),
					"<li>%s (<a href='#rf' class='anchor'>Residual vs Fitted Plot</a>).</li>"%(def_['hv']),
					'<li>%s </li>'%(def_['io']),
				'</ul>',
			'</div>'
			"<div class='paragraph'>",
				"<div>The following post-hoc analysis were run:</div>",
				'<ul class="number-list">',
					'<li><a href="#qq" class="anchor">Q-Q Plot</a>.</li>',
					"<li><a href='#rf' class='anchor'>Residual vs Fitted Plot</a>.</li>",
				'</ul>',
			'</div>'
		])
		#results
		terms = ['bias score','stimulus','trial number']
		results = [
			"The resulting data were analysed by fitting mixed effects logistic regression models in 'R', using the glmer \
			function (%s)."%(def_['lmer']),
			"The dependent variable was a binary measure of CESD score ('Low' (<16) and 'High' (≥16))."
			"The random effects were: trial and particpant.",
			"The fixed effects were: %s score (within subjects),"%(me[0].replace("_", " ")),
			"trial (within subjects; 0-197),",
			"and stimulus (within subjects; %s, %s)."%(def_['iaps'], def_['pofa']),
			"Weights were applied to the model to correct for the validity of bias score per trial."
		]
		## main effects
		for idx, effect in enumerate(me):
			#get row
			row = df_logit[df_logit['term'].str.contains(effect)]
			#get term, B, se, z, p
			term = terms[idx]
			or_ = stn(row['OR'].values[0])
			ci_ = '%s, %s'%(stn(row['95% CI'].values[0][0]),stn(row['95% CI'].values[0][1]))
			p_ = stn(row['Pr(>|z|)'].values[0])
			#append
			#if first item
			results.append('From our results, task %s did not predict the magnitude of CESD score &beta;=%s, 95%% CI[%s], p=%s.'%(term,or_,ci_,p_))

		results = '<p>' + ' '.join(results) + '</p>'

		#combine all
		footnote = re.sub(r'\s+', ' ', summary + description + results).strip()

		#----prepare script for html
		script = ['<div class="code-container" style="display: none">'+'\n',
					'<pre class="line-numbers">'+'\n',
						'<code class="lang-r">'+'\n',
						'%s\n'%(get_logit),
						'</code>'+'\n',
					'</pre>'+'\n',
				'</div>'+'\n']
		script = ''.join(script)

		#----allows seaborn to be run if matplotlib has already been loaded
		os.environ['KMP_DUPLICATE_LIB_OK']='True'

		#----plots
		html_plots = []
		#probability (QQ) plot
		file = "%s_qq.png"%(y)
		path_ = path + "/img/" + file
		title_="Q-Q Plot for CESD Group (<a class='cat iaps'>iaps</a>, <a class='cat pofa'>pofa</a>)."
		footnote_ = def_['qq']
		html_plots.append({"title":title_,"file":"%s"%(file),"footnote":footnote_, "anchor":"qq"})
		plot.qq_plot(config=config, y=y, residuals=residuals, path=path_)

		#residuals vs fitted plot
		file = "%s_residuals.png"%(y)
		path_ = path + "/img/" + file
		title_="Residuals vs Fitted for CESD Group (<a class='cat iaps'>iaps</a>, <a class='cat pofa'>pofa</a>)."
		footnote_ = def_['rvf']
		html_plots.append({"title":title_,"file":"%s"%(file),"footnote":footnote_, "anchor":"rf"})
		plot.residual_plot(config=config, y=y, residuals=residuals, path=path_)

		#----save model and plot
		#save model and plot
		##create html
		html = None
		if is_html:
			path_ = path + '/%s.html'%(y)
			html = plot.html(config=config, df=df_logit, raw_data=df, path=path_, source=source, plots=html_plots, name=y, 
					title=title, footnote=footnote, script=script)        
		#----end
		console('%s finished in %s msec'%(_f,((datetime.datetime.now()-_t0).total_seconds()*1000)), 'blue')
		return model, df_logit, get_logit, html
