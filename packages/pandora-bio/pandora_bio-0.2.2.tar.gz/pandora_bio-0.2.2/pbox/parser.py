import sys

import argparse as ap

from . import version

def parse_args(args):
    parent_parser = ap.ArgumentParser(add_help=False)
    parent_parser.add_argument(
                                '-v', '--version',
                                action='version',
                                version=version.__version__,
                                help='print version information'
    )

    fq_parser = ap.ArgumentParser(add_help=False)
    fq_parser.add_argument(
                            '-fq',
                            '--fastq',
                            required=True,
                            help='input fastq (.gz) file.'
    )

    plot_parser = ap.ArgumentParser(add_help=False)
    plot_parser.add_argument(
                                '-p',
                                '--plot',
                                action='store_true',
                                help='set to plot a figure, default=False'
    )

    seq_parser = ap.ArgumentParser(add_help=False)
    seq_parser.add_argument(
                            '-s',
                            '--sequence',
                            required=True,
                            help='input sequence file.'
    )



    p = ap.ArgumentParser(parents=[parent_parser], add_help=False)
    # create subparsers
    subp = p.add_subparsers(dest='subparser_name')
    # create parser for 'fq2fa' command
    p_fq2fa = subp.add_parser(
                                'fq2fa',
                                help='convert fastq to fasta.',
                                parents=[
                                            fq_parser,
                                            parent_parser
                                ]
    )

    # create parser for 'fxlength' command
    p_fxlength = subp.add_parser(
                                    'fxlength',
                                    parents=[
                                                seq_parser,
                                                plot_parser,
                                                parent_parser
                                    ],
                                    help='count sequence length.'
    )

    # create parser for 'avglength' command
    p_avglength = subp.add_parser(
                                    'avglength',
                                    parents=[
                                                seq_parser,
                                                plot_parser,
                                                parent_parser
                                    ],
                                    help='average length of input sequences.'
    )

    # create parser for check_phred command
    p_phred = subp.add_parser(
                                'check_phred',
                                help='check fastq Phred vaule.',
                                parents=[
                                            fq_parser,
                                            parent_parser
                                ]
    )
    p_phred.add_argument(
                            '-n',
                            '--num',
                            type=int,
                            default=1000,
                            help='number of sequences for Phred check (1000).'
    )

	# create parser for extract_seq command
    p_extract = subp.add_parser(
                                'extract_seq',
                                parents=[
                                            seq_parser,
                                            parent_parser
                                ],
                                help='extract sequences using id.'
    )
    p_extract_id = p_extract.add_mutually_exclusive_group()
    p_extract_id.add_argument(
                                '-i',
                                '--seqid',
                                nargs = '+',
                                help='sequence id to extract, seperate by " ".'
    )
    p_extract_id.add_argument(
                                '-l',
                                '--seqidlist',
                                help='id list in file to extract.'
    )
    p_extract.add_argument(
                            '-fq',
                            '--fastq',
                            action='store_true',
                            help='set if input is fastq.'
    )
    p_extract.add_argument(
                            '-u',
                            '--unmatch',
                            action='store_true',
                            help='set to extract unmatch sequences.'
    )

    # create parser for summary_mag command
    p_summary_mag = subp.add_parser(
                                    'summary_mag',
                                    parents=[parent_parser],
                                    help='summary high quality mag.'
    )
    p_summary_mag.add_argument(
                                '-t',
                                '--table',
                                nargs='+',
                                required=True,
                                help='input stat table(s) from CheckM, seperate by " ".'
    )
    p_summary_mag.add_argument(
                                '-cp',
                                '--completeness',
                                type=int,
                                default=80,
                                help='stat genomes with completeness above this value (80).'
    )
    p_summary_mag.add_argument(
                                '-ct',
                                '--contamination',
                                type=int,
                                default=20,
                                help='stat genomes with contamination below this value (20).'
    )


    # create parser for abs2rel command
    p_abs2rel = subp.add_parser(
                                'abs2rel',
                                parents=[parent_parser],
                                help='insert relative abundance for each sample.'
    )
    p_abs2rel.add_argument(
                            '-t',
                            '--table',
                            required=True,
                            help='input table, column represents sample, \
							row represents OTU, species, MAG etc.'
    )
    p_abs2rel.add_argument(
                            '-o',
                            '--out_table',
                            help='otput table, print if not set.'
    )

    if len(args) == 1 or args[1] == '-h' or args[1] == '--help':
        sys.exit(p.print_help())


    return p.parse_args()
