#!/bin/sh
#! /bin/bash
# set -x
# Assign the provided arguments to variables
POSTGRES_HOST="$1"
POSTGRES_PORT="$2"
DB="$3"
BACKUP_DB="$4"
POSTGRES_USER="$5"
POSTGRES_PASSWORD="$6"
migration_job() {
    export PGPASSWORD=$6
    psql -v ON_ERROR_STOP=1 -h $POSTGRES_HOST -p $POSTGRES_PORT -d $DB -U "postgres" <<-EOSQL
    
        SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity 
        WHERE pg_stat_activity.datname = '$DB' AND pid <> pg_backend_pid();
        CREATE DATABASE $BACKUP_DB WITH TEMPLATE $DB OWNER $POSTGRES_USER;
EOSQL
    if [ $? -ne 0 ]; then
        echo "Error: SQL command failed"
        exit 1
    fi
    printf "\n==== Migration Completed from $DB to $BACKUP_DB ====\n"
}
    
migration_job