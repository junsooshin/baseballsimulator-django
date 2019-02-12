# Combines the team play-by-play text files into one text file for the season.
#
# I ran this program beforehand to have the play-by-play file ready for the
# 'pickle_baserunning.py' program.

import glob

read_files = glob.glob('*.txt')

with open('2017plays.txt', 'wb') as outfile:
  for f in read_files:
    with open(f, 'rb') as infile:
      outfile.write(infile.read())