#!/bin/sh

#SBATCH --job-name=rmc                  # job name
#SBATCH --partition=univ                # default "univ" if not specified
#SBATCH --error=/home/maldonis/060911_rmc_eam_gr_vk_t4/job.%J.err
#SBATCH --output=/home/maldonis/060911_rmc_eam_gr_vk_t4/job.%J.out

#SBATCH --time=0-04:30:00               # run time in days-hh:mm:ss

#SBATCH --nodes=16                      # number of nodes requested (n)
#SBATCH --ntasks=16                     # required number of CPUs (n)
#SBATCH --ntasks-per-node=1             # default 16 (Set to 1 for OMP)
#SBATCH --cpus-per-task=16              # default 1 (Set to 16 for OMP)
##SBATCH --mem=16384                    # total RAM in MB, max 64GB  per node
##SBATCH --mem-per-cpu=4000              # RAM in MB (default 4GB, max 8GB)

##SBATCH --export=ALL

echo "JobID = $SLURM_JOB_ID"
echo "Using $SLURM_NNODES nodes"
echo "Using $SLURM_NODELIST nodes."
echo "Number of cores per node: $SLURM_TASKS_PER_NODE"
echo "Submit directory: $SLURM_SUBMIT_DIR"
echo ""

# Executable
mpirun rmc $SLURM_JOB_ID
