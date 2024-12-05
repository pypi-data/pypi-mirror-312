#coding:utf-8

import sys
from loguru import logger

import numpy as np

from ubox import usys, useq


def check_phred(fq: str = None, num: int =  1000) -> None:

	'''
	Check phred value of input fastq.

	Parameter
	---------
	fq := str
		input fastq file.
	num := int, default = 1000
		number of sequence for phred check, [1000].
	'''

	usys.check_file(fq)
	logger.info(f'Checking Phred value using {num} sequences.')
	universal_quals, universal_mins, c = [], [], 0
	fh = usys.open_file(fq)
	for name, seq, qual in useq.readseq(fh):
		if c < num:
			qual = [ord(i) for i in qual]
			universal_quals.extend(qual)
			universal_mins.append(min(qual))
			c += 1
		else:
			break
	fh.close()
	print(f'Mean of all input ASCII: {np.mean(universal_quals)}\n')
	print(f'Mean of all minimum ASCII: {np.mean(universal_mins)}\n')
	print(f'SD of all minimum ASCII: {np.std(universal_mins)}\n')
