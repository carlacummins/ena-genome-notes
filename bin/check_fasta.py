#!/usr/bin/env python

import sys, argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description="Check fasta file for duplicates")
parser.add_argument('--fa', help="input fasta")
parser.add_argument('--out', help="output fasta")
opts = parser.parse_args(sys.argv[1:])

seen = {}
order = []
total_seqs, dup_seqs = 0, 0
for seq_record in SeqIO.parse(opts.fa, "fasta"):
    seq_r_id = seq_record.id
    seq_r_len = len(seq_record)

    try:
        if seq_r_len != seen[seq_r_id]['len']:
            sys.stderr.write(f"Duplicate ID ({seq_r_id}) found with different sequence lengths:",
                             f"{seq_r_len}, {seen[seq_r_id]['len']}",
                             "\n")
            sys.exit(1)
        dup += 1
        total += 1
    except KeyError:
        seen[seq_r_id] = {'seq': seq_record.seq, 'len':seq_r_len, 'desc': seq_record.description}
        order.append(seq_r_id)
        total += 1

with open(opts.out, 'w') as outfile:
    for k in order:
        outfile.write(f">{seen[k]['desc']}\n{seen[k]['seq']}\n")

print(f"Removed {dup} duplicate sequences from a total of {total}")