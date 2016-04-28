#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -pe smp 1
#$ -l virtual_free=0.9G
#$ -l h=blacklace02.blacklace|blacklace03.blacklace|blacklace04.blacklace|blacklace05.blacklace|blacklace06.blacklace|blacklace07.blacklace|blacklace08.blacklace|blacklace09.blacklace|blacklace10.blacklace


# script to run blast homology pipe
USAGE="run_blast2csv.sh <query.fa> <dna, protein (query_format)> <genome_sequence.fa> <output_directory>"


#-------------------------------------------------------
# 		Step 0.		Initialise values
#-------------------------------------------------------

IN_QUERY=$1
QUERY_FORMAT=$2
IN_GENOME=$3
ORGANISM=$(echo $IN_GENOME | rev | cut -d "/" -f4 | rev)
STRAIN=$(echo $IN_GENOME | rev | cut -d "/" -f3 | rev)
QUERY=$(echo $IN_QUERY | rev | cut -d "/" -f1 | rev)
GENOME=$(echo $IN_GENOME | rev | cut -d "/" -f1 | rev)
CUR_PATH=$PWD
if [ "$4" ]; then OutDir=$CUR_PATH/$4 else OutDir=$CUR_PATH/analysis/blast_homology/$ORGANISM/$STRAIN; fi
WORK_DIR=$TMPDIR/blast_"$STRAIN"
mkdir $WORK_DIR
cd $WORK_DIR
cp $CUR_PATH/$IN_GENOME $GENOME
cp $CUR_PATH/$IN_QUERY $QUERY
OUTNAME="$STRAIN"_"$QUERY"

echo "Running blast_pipe.sh"
echo "Usage = $USAGE"
echo "Organism is: $ORGANISM"
echo "Strain is: $STRAIN"
echo "Query is: $QUERY"
echo "This is $QUERY_FORMAT data"
echo "Genome is: $GENOME"
echo "You are running scripts from:"
echo "$SCRIPT_DIR"

if test "$QUERY_FORMAT" = 'protein'; then
	SELF_BLAST_TYPE='blastp'
	BLAST_CSV_TYPE='tblastn'
elif test "$QUERY_FORMAT" = 'dna'; then
	SELF_BLAST_TYPE='blastn'
	BLAST_CSV_TYPE='tblastx'
else exit
fi


#-------------------------------------------------------
# 		Step 1.		blast queries against genome
#-------------------------------------------------------

SCRIPT_DIR=$HOME/git_repos/emr_repos/tools/pathogen/blast
$SCRIPT_DIR/blast2csv.pl $QUERY $BLAST_CSV_TYPE $GENOME 5 > "$OUTNAME"_hits.csv


#-------------------------------------------------------
# 		Step 2.		Cleanup
#-------------------------------------------------------

mkdir -p $CUR_PATH/analysis/blast_homology/$ORGANISM/$STRAIN/

cp -r $WORK_DIR/"$OUTNAME"_hits.csv $CUR_PATH/analysis/blast_homology/$ORGANISM/$STRAIN/.

rm -r $WORK_DIR/