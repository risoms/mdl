### dotprobe-js
#### douments
* "Comparison of eye movement filters used in HCI"
* "Web technology and the Internet : the future of data acquisition in psychology?"
#### procedure
#### equipment
* VIEWPixx EEG (H:Horizontal, V:vertical)
	** viewable screen size (cm) - 52(H) x 29.5(V) (D=60cm)
	** screen resolution (px) - 1920 x 1080
	** refersh rate (Hz) - 120
	** colors - 32bit
	** OS - Windows 7
	** Distance from screen: 55-65cm
	** luminence: 100 cd/m2
	** screen width (cm): 52(H) x 29.5(V)
	** screen width (deg): 5.32(H) x 7.09(V)
	** screen width (px): 1920(H) x 1080(V)
	
* Dell U2414H (H:Horizontal, V:vertical)
	** viewable screen size (cm) - 53.5(H) x 30(V) (D=61.5cm)
	** screen resolution (px) - 1920 x 1080
	** aspect ratio: 1.78:1
	** refersh rate (Hz) - 60
	** colors - 32bit
	** OS - Windows 8.1
* Eyetrackers
	** Eyelink
		*** sampling rate - 500Hz
	** webgazer
		*** sampling rate - 20Hz
* Home
	** screensize (cm) - various
	** resolution (px) - various
	** refersh rate (Hz) - various
	** colors - various
	** OS - various

*stim
    ** screensize (cm) - 5.5(H) x 7.5(V)
	** resolution (px) - 206 x 272

#### redcap
* quids cutoff score
	** 13 or greater is eligible
	
#### stim
* IAPS - International Affective Picture System (Lang, Bradley, & Cuthbert, 2008) 
* POFA - Pictures of Facial Affect (Ekman & Friesen, 1976)

#### trial
* fixation: 0-1500ms (1500)
* facestim: 1500-4500ms (3000)
* dotloc: 4250-14250ms (10000)
* delay: 14250-14500ms (250)

#### task
* nine blocks of 198 trials
* two conditions (subject does same version each time): 
	* active training:
		-- probe [target] 80% neutral stim location
		-- probe [target] 20% dysphoric [sad] stim location
	* placebo:
		-- probe [target] 50% neutral stim location
		-- probe [target] 50% dysphoric [sad] stim location

#### structure
* 196-trials (total), 9-blocks, 22-trials [12 - pofa; 10*9 - iaps]
* minimal duration: 17 minutes + 4 minute break + 5 minute practice
	** (12 pofa_trials * 9 blocks * (4.5 second stim) +
	** (10 iaps_trials * 9 blocks * (6 second trial))
* maxinum duration: 50 minutes [include max response time]: 17 minutes + 4 minute break + 5 minute practice
	** (12 pofa_trials * 9 blocks * (4.5 second stim + 10 second response) + 
	** (10 iaps_trials * 9 blocks * (6 second trial + 10 second response))

```
dotprobe-js task
├── Practice
│	├── IAPS
│	│	├── Fixation: 1500msec
│	│	├── Stimulus: 4500msec
│	│	├── Probe: User defined 
│	├── POFA
│	│	├── Fixation: 1500msec
│	│	├── Stimulus: 3000msec
│	│	├── Probe: User defined
├── Task
│	├── Block 1: 20 trials
│	│	├── POFA: 12 trials
│	│	├── IAPS: 10 trials
│	├── Block 2
│	├── Block 3
│	├── Break: 2 minutes
│	├── Block 4 
│	├── Block 5
│	├── Block 6
│	├── Break: 2 minutes
│	├── Block 7
│	├── Block 8
│	├── Block 9
```

#### directory
```
task
├──dotprobe-js 
│	├── data - viewing participant data
│	│	├── a - view all participant data
│	│	├── u - user only
│	├── dist - required files
│	├── docs - notes related to task
│	├── src - program to run task
│	├── tools - files to edit task
│
Google
├──console developers - allow access to google calendar

Cron
├──https://mail.google.com/mail/u/0/#inbox/15debfaf3abec6b9
├──https://www.codeofaninja.com/2012/08/cron-job-example-with-putty.html
├── Fn + enter
├── crontab -e
├── 00 9 * * * /home/utw10625/public_html/app/dotprobe-js/data/notify/notify.php
├── press ESC.
├── type ":wq" and press enter.

```
### comments
* condition is permanent within subjects
* subjects must do the task only once per 24 hours

