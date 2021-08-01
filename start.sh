#!/bin/bash

SCRIPT_PATH=${0%/*}
PROGRAMM_DIR=tb_weather
PROGRAMM_NAME=tbweather.py
CLEAN_NAME=__pycache__
REQUIRETMENTS_NAME=requiretments.txt
PY=python
PIP=pip
ACTION=$1

run ()
{
cd $SCRIPT_PATH/$PROGRAMM_DIR/
$PY $PROGRAMM_NAME
}
clean ()
{
rm -rf $PROGRAMM_PATH/$CLEAN_NAME
}
requiretments ()
{
$PIP install -r $SCRIPT_PATH/$REQUIRETMENTS_NAME
}
help ()
{
echo "    ~/start.sh <parameters>"
echo "-r |--run           - Runing telegram weather bot."
echo "-c |--clean         - Remove byte-compiled files by python."
echo "-rq|--requiretments - Install packages for telegram weather bot."
echo "-i |--install       - Install and run telegram weather bot."
echo "-rb|--re-build      - Re-building telegram weather bot."
echo "-h |--help          - Output help message."
}

case $ACTION in
-r|--run)
run
;;
-c|--clean)
clean
;;
-rq|--requiretments)
requiretments
;;
-i|--install)
requiretments
run
;;
-rb|--re-build)
clean
run
;;
-h|--help)
help
;;
*)
echo "Enter incorrect action"
help
;;
esac

exit 0
