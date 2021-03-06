#ifndef COMMON_H
#define COMMON_H
/*
 *  common.h
 *  Spats
 *
 *  Copyright 2008 Cole Trapnell. All rights reserved.
 *
 */
#include <stdint.h>
#include <cassert>
#include <cstring>
#include <cstdlib>
#include <string>
#include <cstdio>

extern int inner_dist_mean;
extern int inner_dist_std_dev;
extern int max_mate_inner_dist; 

extern int min_anchor_len;
extern int min_report_intron_length;
extern int max_report_intron_length;

extern int min_closure_intron_length;
extern int max_closure_intron_length;

extern int min_coverage_intron_length;
extern int max_coverage_intron_length;

extern int min_segment_intron_length;
extern int max_segment_intron_length;

extern uint32_t min_closure_exon_length;
extern int island_extension;

extern int segment_length; // the read segment length used by the pipeline
extern int segment_mismatches;

extern int max_splice_mismatches;

enum ReadFormat {FASTA, FASTQ};
extern ReadFormat reads_format;

extern bool verbose;
extern int max_multihits;
extern bool no_closure_search;
extern bool no_coverage_search;
extern bool no_microexon_search;
extern bool butterfly_search;

extern float min_isoform_fraction;

extern std::string output_dir;
extern std::string gff_file;
extern std::string gene_filter;

extern std::string ium_reads;

extern bool phred33_quals;
extern bool phred64_quals;

extern bool fastq_db;

extern bool compute_consensus_reactivities;
extern bool all_RT_starts;

int parseInt(int lower, const char *errmsg, void (*print_usage)());
int parse_options(int argc, char** argv, void (*print_usage)());


#endif
