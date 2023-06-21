#!/bin/sh
#! /bin/bash
#########################################
# Developed By: Subhranil Ghosh 
# Description: This script take some postgres db releted arguments and will isntall a extension in db if not present.
#########################################
# set -x

# Function to initialize the job
init_job() {

  # initialize user password
  export PGPASSWORD=${POSTGRES_PASSWORD}
  # Connect to PostgreSQL and check if the pgcrypto user exists
  OUTPUT=$(psql -v ON_ERROR_STOP=1 -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$DB" -U "$POSTGRES_USER" -c "SELECT extname from pg_extension WHERE extname = 'pgcrypto';")

  # Check the exit status of the previous command
  if echo "$OUTPUT" | grep "(0 rows)"; then
    # The pgcrypto user does not exist, so create the extension
    psql -v ON_ERROR_STOP=1 -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$DB" -U "$POSTGRES_USER" -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
    echo "The pgcrypto extension is installed."
    exit 0
  else
    # The pgcrypto extension already exists, so exit the script
    echo "The pgcrypto extension is already installed."
    exit 0  
  fi
}

# Assign the provided arguments to variables
POSTGRES_HOST="$1"
POSTGRES_PORT="$2"
DB="$3"
POSTGRES_USER="$4"

# Call the init_job function
init_job