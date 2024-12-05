#coding:utf-8

import sys
from loguru import logger

import pandas as pd

from ubox import usys, useq


def extract_seq(
				seqid: str = None,
				idlist: str = None,
				seqin: str = None,
				fastq: bool = False,
				unmatch: bool = False
	) -> None:
	'''
	Extract sequences from fasta or fastq file.

	Parameter
	---------
	seqid := str, None
		sequence id to extract.
	idlist := str, None
		sequence id list to extract.
	seqin := str, None
		input fasta or fastq sequence file.
	fastq := bool, default = False
		set if input is fastq [False].
	unmatch := bool, default = False
		set to extract unmatch sequences [False].
	'''

	usys.check_file(seqin)
	if idlist: usys.check_file(idlist)
	handle = usys.open_file(seqin)
	allid = seqid and seqid or pd.read_csv(idlist, squeeze=False, header=None, index_col=0, sep='\t').index
	if not fastq:
		logger.info('Extracting sequences from fasta file...')
		if not unmatch:
			for name, seq, _ in useq.readseq(handle):
				if name in allid:
					print(f'>{name}\n{seq}\n')
		else:
			for name, seq, _ in useq.readseq(handle):
				if name not in allid:
					print(f'>{name}\n{seq}\n')
		logger.success('Finished extracting sequences from fasta file.')
	else:
		logger.info('Extracting sequences from fastq file...')
		if not unmatch:
			for name, seq, qual in sequtil.readseq(handle):
				if name in allid:
					print(f'@{name}\n{seq}\n+\n{qual}\n')
		else:
			for name, seq, qual in useq.readseq(handle):
				if name not in allid:
					print(f'@{name}\n{seq}\n+\n{qual}\n')
		logger.success('Finished extracting sequences from fastq file.')
	handle.close()
