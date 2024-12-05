# pandora-bio：A collection of some simple functions that are frequently used on a daily basis.

[[English](./README.md)] | [[中文](./README_CN.md)]

## 1. Introduction
 `pandora-bio` collected codes for many simple functions, which are convenient for users to call. After the installation, users can easily call the functions in the package, such as converting `fastq` to `fasta`, users just need to call the `fq2fa` command. Hope you find this tool useful.

`pandora` currently contains the following commands:

- `fq2fa`: convert `fastq` to `fasta`，`fasta` sequences are `stdout` on the fly。If you want `fasta` sequences in a file，use `>` to simply redirect `stdout` to the file.

- `check_phred`: check the average `Phred` value of input sequences。This module will read in a specifed number of sequences (`--num`), store all `ASCII` value of each sequences and minimal `ASCII` value as well, in the end, `stdout` the average of all stored `ASCII` value and average value of all minimal `ASCII` value and the standard deviation.

- `extract_seq`: extract matched/unmatched sequences with given `--seqid` or `--idlist`. `--seqid` can be multiple different ids seperated by " ", while `--idlist` should be provided a file contains `id` in a list/dataframe form, the first column represents the sequence id. When `--unmatch` is set, `stdout` will be all the sequences whose ids are not provided.

- `fxlength`: read in the sequence file and `stdout` the length of each sequence in the form of <sequence `id`><TAB><sequence length>.

- `avglength`: read in the sequence file and `stdout` the average length of all inputted sequences.

- `summary_mag`: read in the quality statistics file of one or more `CheckM/CheckM2` provided by `-i`, count the high-quality MAGs in each file with genome completeness higher than `--completeness` and contamination lower than `--contamination`, the information of these MAGs will retain for final summary. After integrating all the high-quality MAGs information, MAGs will be counted in steps of `5` as the completeness and contamination decreases from `100` and increases from `0`, respectively. For instance, when `--completeness 90 --contamination 10` is set，the function will count the number of MAGs with a completeness of `100` and a contamination of `0`, the number of MAGs with a completeness between `100` and `95` and a contamination between `0` and `5`, and the number of MAGs with a completeness between `95` and `90` and a contamination between `5` and `10`.

- `abs2rel`: calculate relative values for absolute values and insert the relative value column into the table. Columns represent samples.

## 2. Installation
`pandora` has been uploaded to `PyPI`, and can be installed using `pip`:
```
$ pip install pandora-bio
```

## 3. Usage
All subcommands in `pandora` can be called directly for different scenarios. View commands in `pandora`:
```
$ pandora -h
```
```
usage: pandora [-h] [-v] {fq2fa,fxlength,avglength,check_phred,extract_seq,summary_mag,abs2rel} ...

positional arguments:
  {fq2fa,fxlength,avglength,check_phred,extract_seq,summary_mag}
    fq2fa               convert fastq to fasta.
    fxlength            count sequence length.
    avglength           average length of input sequences.
    check_phred         check fastq Phred vaule.
    extract_seq         extract sequences using id.
    summary_mag         summary high quality mag.
    abs2rel             insert relative abundance for each sample.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print version information
```

### 3.1 `fq2fa`
Convert `fastq` to `fasta`. View details using `pandora fq2fa -h`.
```
$ pandora fq2fa -h
```
```
usage: pandora fq2fa [-h] [-v] -i FQ

optional arguments:
  -h, --help      show this help message and exit
  -v, --version   print version information
  -i FASTQ, --fastq FASTQ  input fastq file (.gz).
```

**`fq2fa` Example**
```
$ pandora fq2fa -i test.fastq.gz > test.fasta
$ pandora fq2fa -i test.fastq.gz | gzip > test.fasta.gz
```

### 3.2 `check_phred`
Check `Phred` value of input sequences. View details using `pandora check_phred -h`。
```
$ pandora check_phred -h
```
```
usage: pandora check_phred [-h] [-v] -i FASTQ [-n NUM]

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      print version information
  -i FASTQ, --fastq FASTQ     input fastq file.
  -n NUM, --num NUM  number of sequences for Phred check (1000).
```

**`check_phred` Example**
```
$ pandora check_phred -i test.fastq.gz -n 10000
```

### 3.3 `extract_seq`
Extract sequences based on the input sequence id. View details using `pandora extract_seq -h`.
```
$ pandora extract_seq -h
```
```
usage: pandora extract_seq [-h] [-v] [-i SEQID [SEQID ...] | -l SEQIDLIST] -s SEQUENCE [-fq] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print version information
  -i SEQID [SEQID ...], --seqid SEQID [SEQID ...]
                        sequence id to extract, seperate by " ".
  -l SEQIDLIST, --seqidlist SEQIDLIST
                        id list in file to extract.
  -s SEQUENCE, --sequence SEQUENCE
                        input sequence.
  -fq, --fastq          set if input is fastq.
  -u, --unmatch         set to extract unmatch sequences.
```

**`extract_seq` Example**
Extract sequences that match input `id`:
```
$ pandora extract_seq -i Filt9 -s test.fa > extracted_Filt9.fa
$ pandora extract_seq -l seq_list -s test.fa > extracted_all.fa
```

Extract sequences that don't match input `id`:
```
$ pandora extract_seq -i Filt9 -s test.fa -u
```


### 3.4 `fxlength`
Count the length of each sequence in the input file. View details using `pandora fxlength -h`.
```
$ pandora fxlength -h
```
```
usage: pandora fxlength [-h] [-v] -s SEQ [-p]

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      print version information
  -s SEQUENCE, --sequence SEQUENCE  input sequence file.
  -p, --plot         Set to plot a histogram for length.
```

**`fxlength` Example**
```
$ pandora fxlength -s test.fa --plot
$ pandora fxlength -s test_1.fa.gz --plot
```

### 3.5 `avglength`
Calculate the average length of input sequences. View details using `pandora avglength -h`.
```
$ pandora avglength -h
```
```
usage: pandora avglength [-h] [-v] -s SEQUENCE [-p]

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      print version information
  -s SEQUENCE, --sequence SEQUENCE  input sequence file.
  -p, --plot         set to plot a histogram for length
```

**`avglength` Example**
```
$ pandora avglength -s test.fa --plot
$ pandora avglength -s test_1.fq.gz --plot
```

### 3.6 `summary_mag`
Count high-quality MAGs based on the result of `CheckM/CheckM2`. View details using `pandora summary_mag -h`.
```
$ pandora summary_mag -h
```
```
usage: pandora summary_mag [-h] [-v] -i INPUT [INPUT ...] [-cp COMPLETENESS] [-ct COMTAMINATION]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print version information
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        input stats file from CheckM, seperate by " ".
  -cp COMPLETENESS, --completeness COMPLETENESS
                        stat genomes with completeness above this value (80).
  -ct COMTAMINATION, --comtamination COMTAMINATION
                        stat genomes with comtamination below this value (20).
```

**`summary_mag` Example**
```
$ pandora summary_mag -i checkm_result.txt -cp 80 -ct 20
```

### 3.7 `abs2rel`
Calculate the relative values based on the absolute values. View details using `pandora abs2rel -h`.
```
$ pandora abs2rel -h
```
```
usage: pandora abs2rel [-h] [-v] -i TABLE [-o OUT_TABLE]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print version information
  -i TABLE, --table TABLE
                        input table, column represents sample, row represents OTU, species, MAG etc.
  -o OUT_TABLE, --out_table OUT_TABLE
                        output table, print if not set.
```

**`abs2rel` Example**
```
$ pandora abs2rel -i abundance.table.xls -o abundance.table.relative.xls
```

## 4. Contribution
Feel free to contribute to this project. You can open an [issue](https://github.com/lijierr/pandora/issues) or submit a pull request.

## 5. Contact
Repository was developed by [Jie Li](https://github.com/lijier6).
