#!/bin/bash
echo $1
echo $2
echo $3

# declare a name for this job (replace <jobname> with something more descriptive)
#$ -N femsim_mds

# request the queue for this job
# replace <queue_name> with queue_name e.g all.q
#$ -q all.q

# request computational resources for this job as follows
# OpenMPI is current parallel environment for nodes without IB. Do not change unless you use a different MPI
# <num> specifies how many processors in total to request. It's suggested use 12*integer processors here. 
#$ -pe orte 1

# request 48 hours of wall time, if you need longer time please contact system admin
#$ -l h_rt=48:00:00

# run the job from the directory of submission. Uncomment only if you don't want the defaults.
#$ -cwd
# combine SGE standard output and error files
#$ -o $JOB_NAME.o$JOB_ID
#$ -e $JOB_NAME.e$JOB_ID
# transfer all your environment variables. Uncomment only if you don't want the defults
#$ -V

# The following is for reporting only. It is not really needed to run the job
# It will show how many processors you get in your output file
echo "Got $NSLOTS processors."

# Use full pathname to make sure we are using the right mpi
#If you are not using the general purpose mpiexec, make sure your mpi environment is properly set up such
#that the correct mpirun is found (you should use the mpirun provided with the compiler
#used to compile the program you are running).
#MPI_HOME is probably the same as the already-set MPIHOME.
MPI_HOME=/share/apps/openmpi_intel_20130712/bin

$MPI_HOME/mpiexec -n $NSLOTS $1
