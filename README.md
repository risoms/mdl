# Pupil dilation ROI
Semeon (08-01-2018)

### This directory includes ROI data related to stimuli set used in Pupil dilation. There are three types of files in the directory:
- metadata file (metadata.csv)
- image roi coordinates (e.g. 1601.csv)
- image sample (e.g. 1601_all.png)

### 1601_all.png
This provides an example of the stimulus used to extract roi images. The images were imbedded within a chart for convenience.

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |


### 1601.csv
CSV files (named after corresponding image) are a list of each ROI xy-coordinate. Columns are id (unique id for each roi), x, y coordinates. 
Note: y-axis uses reversed cartesian coordinates (origin starts at top left corner).
| id | x | y |
| ------ | ------ | ------ |
| 16011 | 332 | 479 |
| 16011 | 332 | 480 |
| 16011 | 332 | 481 |
| 16012 | 271 | 261 |
| s | s | s |

### metadata.csv
The metadata.csv file is a list of each ROI's relevant metadata (valence, resolution)
| id | file | ROI | resolution | valence | … | … |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 16011 | 1601 | 1 | (575, 767) | positive | … | … |
| 16012 | 1601 | 2 | (575, 767) | positive | … | … |
| 19101 | 1910 | 1 | (1024, 768) | positive | … | … |
| 20301 | 2030 | 1 | (1024, 768) | positive | … | … |
| … | … | … | … | … | … | … |


