#!/bin/bash
# 
# Prepare GCP project environment by creating the required bucket and dataset.

#############################################################################
# Run the first command, return if succeed. Otherwise run the second command.
# Arguments:
#   $1: first command
#   $2: second command
# Returns:
#   None
#############################################################################
check_and_run() {
  echo "Executing: "$1
  unset IFS
  $1
  if [[ $? -ne 0 ]]; then
    echo "Executing: "$2
    $2
    if [[ $? -ne 0 ]]; then
      echo "Fail to set up the GCP environment."
      exit 1
    fi
  fi
  echo "Success."
}

echo "Preparing GCP environment..."
commands_to_run=(
  "gsutil ls gs://airflow-gcp-smoke, gsutil mb gs://airflow-gcp-smoke"
  "bq ls airflow, bq mk airflow"
  "bq ls airflow_temp, bq mk airflow_temp" )
for command in "${commands_to_run[@]}"
do
  IFS=","
  set $command
  check_and_run $1 $2
done
echo "GCP environment is ready." 
