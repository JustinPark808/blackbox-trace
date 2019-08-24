#!/bin/bash

# Check that an argument was given
if [ "$1" = "" ]; then
    echo "Number of insert statements was not given!"
    exit 1
fi

# Check that the right number of arguments was given
if [ $# -gt 1 ]; then
    echo "Too many arguments were given!"
    exit 1
fi

# Get the directory of this script and set the filename of the MySQL script to
# create 
DIR="$(cd $(dirname $BASH_SOURCE) && pwd)"
FILE="$DIR/insert_script.sql"

# Delete file if it already exists
rm $FILE >/dev/null 2>&1

# Append MySQL statements
echo \
"-- Setup database
DROP DATABASE IF EXISTS test_database;
CREATE DATABASE test_database;
USE test_database;

-- Setup table
DROP TABLE IF EXISTS test_table;
CREATE TABLE test_table(x INT);

-- Insert values
INSERT INTO test_table(x)
VALUES" \
    >> $FILE

# Append INSERT values
for (( i=1; i<=$1; i++ ))
do
    if [ $i -lt $1 ]; then
        echo "    (0)," >> $FILE
    else
        echo "    (0);" >> $FILE
    fi
done
