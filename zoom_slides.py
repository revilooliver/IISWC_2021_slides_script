# Project: IISWC 2021 Script
# Filename: zoom_slides.py
# Date: August 20, 2021
# Author: Ji Liu
# Title: PC Meeting - Zoom Slides Generator
# Description:
## This script will generate zoom breakout room powerpoint for each paper based on PC conflict

#%% Import some libraries that are needed
import pandas as pd
import tqdm
from pathlib import Path
import math
import logging
import os
import sys
import os

from Utils.utils import chmkdir, chdir

# Input CSV filename
paper_data_filename           = 'sample-data/input/iiswc21-paperdata-tag.csv'
paper_pc_conflict_filename    = 'sample-data/input/iiswc21-pcconflicts.csv'

# Output tex filename
paper_discussion_slides_folder = 'sample-data/output/slides'

# Template path
template_path = 'sample-data/output/template'

# Load the Paper Data
paper_data_df = pd.read_csv(paper_data_filename)

# Load the Paper PC Conflict
paper_pc_conflict_df = pd.read_csv(paper_pc_conflict_filename)

# %% Make Folder
if not os.path.exists(paper_discussion_slides_folder):
    os.makedirs(paper_discussion_slides_folder)

def slides():
    # Generate template
    gen_beamer_template(template_path, paper_discussion_slides_folder)
    # Iterate through each paper
    for index,paper in tqdm.tqdm(paper_data_df.iterrows(), total=paper_data_df.shape[0]):
            paper_title = paper['Title']
            paper_ID = paper['ID']
            gen_discussion_slides_single(index, paper_title, paper_ID, paper_discussion_slides_folder)




def gen_discussion_slides_single(index, paper_title, paper_ID, output_path):
    #find all pc conflicts from pc conflict name, generate a list of names
    frame_title = "Discussion" #f"Discussion No.{index + 1}"
    conflict_df = paper_pc_conflict_df.loc[paper_pc_conflict_df['title'] == paper_title]

    tpc_conflicts = []
    for index, conflicts in conflict_df.iterrows():
        pc_name = conflicts['first'] + " " + conflicts['last']
        tpc_conflicts.append(pc_name)
    tpc_conflicts.sort()

    num_tpc_per_line = 3
    with chdir(output_path):
        with chmkdir("frames"):
            with open(f"{paper_ID}.tex", "w") as f:
                f.write("\\begin{frame}{" + frame_title + "}\n")
                f.write("  \\begin{center}\n")
                f.write("    {\\LARGE\\bfseries Paper \\#" + str(paper_ID) +"}\n")
                f.write("    \n")
                f.write("    \\bigskip\n")
                f.write("    \n")
                if len(tpc_conflicts) == 0:
                    f.write("    No pc member is in conflict")
                else:
                    f.write(
                        "    The following pc members are in conflict (sorted by first name)\n"
                    )
                    f.write("    \n")
                    f.write("    \\bigskip\n")
                    f.write("    \n")
                    f.write("    \\begin{footnotesize}\n")
                    num_column = num_tpc_per_line
                    f.write(
                            "      \\begin{tabularx}{\\linewidth}{|"
                            + num_column * ("X|")
                            + "} \\hline \n"
                        )
                    table_size = int(math.ceil(len(tpc_conflicts)/num_tpc_per_line)) * num_tpc_per_line
                    for i in range(table_size):
                        if i % num_tpc_per_line == 0:
                            f.write("        ")
                        if i < len(tpc_conflicts):
                            f.write(tpc_conflicts[i])
                        if i % num_tpc_per_line == num_tpc_per_line - 1:
                            f.write(" \\\\ \\hline \n")
                        else:
                            f.write(" & ")
                    f.write("      \\end{tabularx}\n")
                    f.write("    \\end{footnotesize}\n")
                f.write("  \\end{center}\n")
                f.write("\\end{frame}\n")
        with open("content.tex", "a") as f:
            f.write("\\input{frames/" + str(paper_ID) + ".tex}\n")

def gen_beamer_template(template_path, output_path):

    tp = Path(template_path).resolve()
    op = Path(output_path).resolve()

    with chmkdir(op):
        with open("slides.tex", "w") as f:
            f.write("\\documentclass{beamer}\n")
            f.write("\\usepackage{tabularx}\n")
            f.write("\\usetheme{focus}\n")
            f.write("\\title{IISWC2021}\n")
            f.write("\\subtitle{PC Meeting}\n")
            f.write("\\date{xx xx 2021}\n")
            f.write("\\begin{document}\n")
            f.write("  \\begin{frame}\n")
            f.write("    \maketitle\n")
            f.write("  \\end{frame}\n")
            f.write("\\input{content.tex}\n")
            f.write("\\end{document}\n")

        with open("content.tex", "w") as f:
            f.write("\n")

    for f in tp.iterdir():
        if f.suffix == ".sty":
            src_file = f.resolve()
            dst_file = op / f.name
            shutil.copy(src_file, dst_file)

if __name__ == "__main__":
    slides()