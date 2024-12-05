#coding:utf-8

import sys
from loguru import logger

from ubox import usys, useq


def fxlength(
				seq_in: str = None,
				plot: bool = False,
				avg_only: bool=False
	) -> None:
	'''
	Stdout length of each sequence,
	plot a histgram if plot=True was set.

	Parameter
	---------
	seq_in := file
		input sequence file, fastq or fasta.
	plot := bool, default = False
		set to plot histgram of sequences' length [False].
	avg_only := bool, default = False
		set to print average length only [False].
	'''

	usys.check_file(seq_in)

	#length = {}
	#length['length'] = {}
	length = []
	if not avg_only: print('seqid\tlength')
	handle = usys.open_file(seq_in)
	logger.info('Reading the sequence length...')
	for name, seq, qual in useq.readseq(handle):
		if not avg_only: print(f'{name}\t{len(seq)}')
		#length['length'][name] = len(seq)
		length.append(len(seq))
	logger.info('Reading sequence length finished.')

	#if avg_only or plot:
	#	try:
	#		import pandas as pd
	#	except ModuleNotFoundError:
	#		logger.error(f'<pandas> required, try <pip install pandas>.')
	#		sys.exit()
			# dict to DataFrame
		#length = pd.DataFrame.from_dict(length)

	if avg_only or plot:
		try:
			import numpy as np
		except ModuleNotFoundError:
			logger.error('<numpy> required, try <pip3 install numpy.>')
			sys.exit()

	if avg_only: print(f'The mean length is {np.mean(length)}.\n')

	if plot:

		try:
			import matplotlib
		except ModuleNotFoundError:
			logger.error('<matplotlib> required, try <pip3 install matplotlib>.')
			sys.exit()

		matplotlib.use('Agg')
		import matplotlib.pyplot as plt
		logger.info('Plotting histogram...')
		ax = plt.subplot()
		ax.hist(length, density=False)
		xlim, ylim = ax.get_xlim(), ax.get_ylim()
		text_posi = 0.05*(xlim[1]-xlim[0])+xlim[0], 0.9*(ylim[1]-ylim[0])+ylim[0]
		ax.text(0.05*(text_posi[0], text_posi[1], 'mean length: %.2f' % np.mean(length))
		ax.set_xlabel('sequence length')
		ax.set_ylabel('frequency')
		plt.savefig(f'{seq_in}.len.pdf', dpi=600)
		logger.info(f'The histogram stored at **{seq_in}.len.pdf**')
