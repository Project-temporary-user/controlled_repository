#!/bin/bash


if [ $# -eq 0 ]; then
 echo "Provide token, username, repository and number of commits"
 exit 1
fi

token=$1
username=$2
controlled_repository=$3
commit_number=$4

current_dir=$(dirname "$0")
echo $current_dir
initial_dir=`pwd`
cd $initial_dir/$current_dir

git remote set-url origin "https://${username}:${token}@github.com/${username}/${controlled_repository}.git"

sleep 1
for i in `seq $commit_number`; do
    echo `date '+%Y%m%d%H%M%S'` > README.md
    git add README.md
    git commit -m "new code change"
    git push origin master
    sleep 5
done


