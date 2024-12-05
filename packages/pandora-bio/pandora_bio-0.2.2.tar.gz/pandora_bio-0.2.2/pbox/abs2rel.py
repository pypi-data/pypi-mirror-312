#coding:utf-8

import sys
from loguru import logger

import pandas as pd

from ubox import usys


def abs2rel(table: str = None, out_table: str = None) -> None:
	'''
	Calculate relative abundance for each sample in the table
	and insert it to the table.

	Parameter
	---------
	table := str
		input table, column indicates sample, row indicates species, mags, OTU and so on.
	out_table := str, default = None
		name of output table.
		Print table if not set [None].
	'''
	usys.check_file(table, check_empty=True)
	in_table = pd.read_csv(table, sep='\t', header=0, index_col=0)

	head = []
	for i in in_table.columns:
		head.extend([i, f'{i}(%)'])
		in_table[f'{i}(%)'] = in_table[i]/in_table[i].sum()*100
	in_table.to_csv(out_table, sep='\t') if out_table else print(in_table)
