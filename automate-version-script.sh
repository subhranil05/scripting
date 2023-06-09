#! /bin/bash
#########################################
# Developed By: Subhranil Ghosh 
# Description: This script will help to push git tag with incremeneted version
#########################################
# set -x

FILE_NAME=release.txt
VERSION=$(cat $FILE_NAME| grep "VERSION" | awk -F= '{print $2}')
REMOVED_PREFIX=$(echo "$VERSION" | sed 's/-d[0-9][0-9]*//')
RELEASE=$(cat $FILE_NAME | grep "RELEASE" | awk -F= '{print $2}')

## Checking if any chnage in CHART VERSION

if [ $REMOVED_PREFIX == $RELEASE ]
then
    VERSION_NUMBER=$(echo "$VERSION" | awk -F'-' '{print $NF}' | sed 's/d//')

    INCREMENTED_VERSION_NUMBER=$(($VERSION_NUMBER + 1))
    echo "@@@@ INCREMENTED THE VERSION SUFFIX @@@@"

    NEW_VERSION="$REMOVED_PREFIX-d$INCREMENTED_VERSION_NUMBER"

    echo "@@@@ UPDATING VERSION in $FILE_NAME @@@@"
    sed -i "s/VERSION=.*/VERSION=$NEW_VERSION/" $FILE_NAME
else
    echo "@@@@ NOTICED NEW CHART VERSION is HERE @@@@"
    NEW_VERSION="$REMOVED_PREFIX-d1"

    echo "@@@@ UPDATING RELEASE in $FILE_NAME @@@@"
    sed -i "s/RELEASE=.*/RELEASE=$REMOVED_PREFIX/" $FILE_NAME
fi

echo "The TAG to be pushed to git is: $NEW_VERSION"

#GIT COMMANDS To PUSH TAGS
git tag $NEW_VERSION

echo "LOCAL TAG CREATED"

git push origin $NEW_VERSION
echo "NEW TAG: $NEW_VERSION is PUSHED to GITHUB"

## COMMIT CHANGES to GIHUB REPO
echo "COMMITING CHANGES to GITHUB"
git add $FILE_NAME

git commit -m "Updated Release Verison with $NEW_VERSION"

git push
echo "COMMITED CHANGES to GITHUB"