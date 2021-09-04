# IISWC_2021_slides
Python script for generating pc meeting slides for IISWC2021
## Prerequisite
Python script needs Pandas and tqdm package. The .tex file compilation requires beamer package.
## Description
Running the following command to generate the slides:
```
python zoom_slides.py
```
## Input
- iiswc21-paperdata-tag.csv: Paper data from HotCRP "any submitted paper" "Download > CSV"
- iiswc21-pcconflicts.csv: Paper conflicts data from HotCRP "any submitted paper" "Download > PC Conflicts"
The script will generate the slides based on paper infomation in paperdata.csv and the pc conflict infomation in pcconflicts.csv
## Output
The slides.tex file will be generated in 'sample-data/output/slides' folder. 
Then the user can use overleaf or texlive to compile the .tex file and generate corresponding pdf file. Overleaf is recommended since it is an online editor and does not require installation.

The generated example slides are shown in meeting_slides.pdf
## Acknowledge
Many thanks to https://github.com/TheNetAdmin/MightyPC
