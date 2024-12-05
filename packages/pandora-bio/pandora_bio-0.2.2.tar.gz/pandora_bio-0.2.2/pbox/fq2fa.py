#coding:utf-8

import os
import sys
from loguru import logger

from ubox import usys, useq


def fq2fa(fq: str = None) -> None:
	'''
	Convert fastq to fasta.

	Parameter
	---------
	fq := str
		input fastq file (.gz).
	'''

	usys.check_file(fq)
	handle = usys.open_file(fq)
	for name, seq, qual in useq.readseq(handle):
		print(f'>{name}\n{seq}')
	handle.close()
