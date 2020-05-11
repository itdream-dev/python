#!/bin/bash -e

# get last commit hash prepended with @ (i.e. @8a323d0)
function parse_git_hash() {
    git rev-parse HEAD 2> /dev/null | sed "s/\(.*\)/\1/"
}

function deploy() {
    if [ $1 = "staging" ]; then
        DEPLOYENV="ivysaur-staging"
    fi
    if [ $1 = "production" ]; then
        DEPLOYENV="ivysaur-production"
    fi

    if [ ! -d ".elasticbeanstalk" ]; then
        mkdir -p ".elasticbeanstalk"
    fi
    cp config_template.yml .elasticbeanstalk/config.yml

    cp ebignore .ebignore
    echo "starting deployment for $1: $DEPLOYENV"
    echo "removing old .ebextensions"
    rm -rf .ebextensions
    sleep 2
    echo "copying new .ebextensions"
    cp -r aws_extensions/$1/beans .ebextensions
    sleep 2
    echo "init env"
    eb init ivysaur --profile=ivysaur
    eb use $DEPLOYENV
    sleep 2
    echo "starting deploy"
    eb deploy
}

if [ $1 = "staging" ] || [ $1 = "production" ] || [ $1 = "both" ] ; then
    GIT_HASH=$(parse_git_hash)
    echo ${GIT_HASH} > version.txt
    echo "git hash: ${GIT_HASH}"

    if [ $1 = "staging" ]; then
        deploy "staging"
    fi
    if [ $1 = "production" ]; then
        deploy  "production"
    fi
    if [ $1 = "both" ]; then
        deploy "staging"
        sleep 2
        deploy "production"
    fi
else
    echo $"Usage: $0 {staging | production | both}"
    exit 1
fi
