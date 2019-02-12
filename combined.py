import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

# bam_to_tbi.py
# parser.add_argument('--riboseq-bam', required=True)
# parser.add_argument('--rnaseq-bam')
#
# # construct_synthetic_footprints.py
# parser.add_argument('--reference-fasta')
# parser.add_argument('--transcriptome-gtf')
# parser.add_argument('--footprint-length')
# parser.add_argument('--output-fastq-prefix')
#
# # compute_mappability.py
# parser.add_argument('--synthetic-bam')
# parser.add_argument('--mappability-output-prefix')  # As tabix
# # Above two steps could be downloaded
#
# # learn_model.py
# parser.add_argument('--reference-fasta', required=True)
# parser.add_argument('--transcriptome-gtf', required=True)
# parser.add_argument('--riboseq-tabix', required=True)
# parser.add_argument('--mappability-tabix')  # Could be downloaded
# parser.add_argument('--rnaseq-tabix')
# parser.add_argument('--log')
# parser.add_argument('--model-output')  # Could be held internally for inference step
# parser.add_argument('--batch')
# parser.add_argument('--scale-beta')
# parser.add_argument('--min-tolerence')
# parser.add_argument('--restarts')
#
# # infer_CDS.py
# parser.add_argument('--model-file')  # Generated by last step
# parser.add_argument('--reference-fasta')
# parser.add_argument('--transcriptome-gtf')
# parser.add_argument('--riboseq-tabix')
# parser.add_argument('--mappability-tabix')  # Could be downloaded
# parser.add_argument('--rnaseq-tabix')
# parser.add_argument('--inference-output')


# combined.py
parser.add_argument('--reference-fasta', required=True,
                    help='Path to a reference genome in fasta format')
parser.add_argument('--transcriptome-gtf', required=True,
                    help='Path to a transcriptome in gtf format')
parser.add_argument('--riboseq-bam',
                    help='Path to a BAM with riboseq mappings')
parser.add_argument('--rnaseq-bam', help='Path to a BAM with RNAseq mappings')
parser.add_argument('--kozak-model', default='kozak_model.npz',
                    help='Path to kozak model')
parser.add_argument('--output-prefix', required=True,
                    help='Path prefix for all output: generated tabix files, learned '
                         'model parameters, and final inference output')
parser.add_argument('--purge-all', action='store_true',
                    help='Do not keep any intermediate files; the final inference output will still '
                         'be generated')
parser.add_argument('--purge-learned-model', action='store_true',
                    help='Do not keep the learned model parameters')
parser.add_argument('--purge-tabix', action='store_true',
                    help='Do not keep the generated tabix files')

parser.add_argument('--inference-input-prefix', help='If given, will skip model learning and use these parameters '
                                                     'and tabix files')
parser.add_argument('--only-learn-model', action='store_true',
                    help='If given, will stop after learning model parameters')

model_group = parser.add_argument_group('Learning Model Parameters',
                                        'Parameters to the learn the inference model parameters')
model_group.add_argument('--log', help='Path to file to store statistics of the EM algorithm; not output '
                                       'if no path is given')
model_group.add_argument('--batch', type=int, default=1000,
                         help='Number of transcripts used for learning model parameters (default: 1000)')
model_group.add_argument('--scale-beta', type=float, default=1e4,
                         help='Scaling factor for initial precision values (default: 1e4)')
model_group.add_argument('--min-tolerence', type=float, default=1e-4,
                         help='Convergence criterion for change in per-base marginal likelihood (default: 1e-4)')
model_group.add_argument('--restarts', type=int, default=1,
                         help='Number of re-runs of the algorithm (default: 1)')

mappability_group = parser.add_argument_group('Mappability Tabix')
mappability_group.add_argument('--mappability-tabix-custom',
                               help='If provided, will use this instead of a download')
mappability_group.add_argument('--mappability-tabix-download',
                               help='If given, the mappability tabix will attempt to download. '
                                    'Choices are as follows:\n'
                                    '1) GRCh37 with GENCODE19 transcriptome\n'
                                    '2) GRCh38 with GENCODE38 transcriptome')

parser.print_help()


# Convert bams to tabix

