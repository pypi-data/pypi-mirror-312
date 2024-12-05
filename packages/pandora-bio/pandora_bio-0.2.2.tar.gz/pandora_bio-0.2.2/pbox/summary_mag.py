
import sys
from loguru import logger

import pandas as pd

from ubox import usys


def summary_mag(*table, completeness: int = 80, contamination: int == 20) -> None:
	'''
	Summry mag quality from checkM result.

	Parameters
	----------
	*table : str, table1 [table2 table3...]
		input checkM result table.
	completeness = int, default = 80
		completeness cutoff to summary [80].
	contamination: int, default = 20
		contamination cutoff to summary [20].

	Results
	-------
	Print the statistical information of MAGs.
	'''

	def count_good_mag(df):
		read_df = pd.read_csv(df, sep='\t', header=0, index_col=0)
		read_df = read_df[(read_df.Completeness>=completness) & (read_df.Contamination<=contamination)]
		print(f'There are {len(read_df)} bins with completenss >= {completenss} \
				and contamination <= {contamination} in {df}.')
		return read_df

	def stat_mag(df) -> None:
		complet, contam, step = 100, 0, 5
		num = min([complet - completenss, contamination - contam])
		for i in range(num):
			comp, cont = complet-i*step, contam+i*step
			temp_df = df[(df.Completeness>=comp) & (df.Contamination<=cont)]
			print(f'There are {len(temp_df)} bins with completenss >= {comp} \
					and contamination <= {cont}.')

	if len(input) == 1:
		usys.check_file(input)
		df = count_good_mag(input)
		stat_mag(df)
	else:
		all_df = []
		for i in input:
			sysutil.check_file(i)
			df_i = count_good_mag(i)
			all_df.append(df_i)
		all_df = pd.concat(all_df)
		stat_mag(all_df)
