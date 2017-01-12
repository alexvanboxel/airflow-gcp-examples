#!/bin/bash
# 
# Prepare GCP project environment by creating the required bucket and dataset.

#######################################################
# Run command and check return status, exit if fails.
# Arguments:
#   $1: command to be run
# Returns:
#   None
#######################################################
exit_if_failed_on_command() {
  echo "executing "$1
  $1
  if [[ $? -eq 0 ]]; then
    echo "successful"
  else
    exit 1
  fi
}

echo "Preparing GCP environment..."
commands_to_run=( "gsutil mb gs://airflow-gcp-smoke" "bq mk airflow"
  "bq mk airflow_temp" )
for command in "${commands_to_run[@]}"
do
  exit_if_failed_on_command "$command"
done
echo "GCP environment is ready." 
