include $(top_srcdir)/config/spats.mk

AM_CPPFLAGS = -I$(top_srcdir)/src 

nobindir = $(bindir)

EXTRA_DIST = $(top_srcdir)/AUTHORS $(top_srcdir)/make_bin.sh \
matlab/barcodes_statistics.m \
matlab/bootstrap_error_bars.m \
matlab/Compute_WF.m \
matlab/correction_factors_examples.m \
matlab/entropy.m \
matlab/H_fun.m \
matlab/log_likelihood_fun.m \
matlab/MLE.m \
matlab/MLE_one_molecule.m \
matlab/randp.m \
matlab/WF_fun.m \
matlab/Readme.txt

AM_CXXFLAGS =

bin_PROGRAMS = \
	relabel_reads \
    match_read_pairs \
    compute_profiles

dist_bin_SCRIPTS = \
	spats.py \
	adapter_trimmer.py

dist_nobin_SCRIPTS = \
	targets_analyzer.py \
	analyze_spats_targets.py \
	fastq_revcomp.py

noinst_HEADERS = \
	assert_helpers.h \
	qual.h \
	tokenize.h \
	common.h \
	reads.h \
	common.h \
    bundles.h \
    hits.h

noinst_LIBRARIES = libspats.a

libspats_a_SOURCES = \
	common.cpp \
	qual.cpp \
	reads.cpp \
	tokenize.cpp \
    bundles.cpp \
    hits.cpp 

relabel_reads_SOURCES = relabel_reads.cpp  
relabel_reads_LDADD = libspats.a $(BOOST_THREAD_LIB)
relabel_reads_LDFLAGS =  $(BOOST_LDFLAGS)

match_read_pairs_SOURCES = match_read_pairs.cpp  
match_read_pairs_LDADD = libspats.a $(BOOST_THREAD_LIB)
match_read_pairs_LDFLAGS =  $(BOOST_LDFLAGS)

compute_profiles_SOURCES = compute_profiles.cpp  
compute_profiles_LDADD = libspats.a $(BOOST_THREAD_LIB)
compute_profiles_LDFLAGS =  $(BOOST_LDFLAGS)
