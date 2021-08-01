#!/bin/bash

SCRIPT_PATH=${0%/*}
PROGRAMM_DIR=tb_weather
PROGRAMM_NAME=tbweather.py
PROGRAMM_PATH=$SCRIPT_PATH/$PROGRAMM_DIR/
CLEAN_NAME=__pycache__
REQUIRETMENTS_NAME=requiretments.txt
REQUIRETMENTS_PATH=$SCRIPT_PATH/$REQUIRETMENTS_NAME
PY=python
PIP=pip
ACTION=${1:---install}

run ()
{
cd $PROGRAMM_PATH
$PY $PROGRAMM_NAME
}
clean ()
{
rm -rf $PROGRAMM_PATH/$CLEAN_NAME
}
requiretments ()
{
$PIP install -r $REQUIRETMENTS_PATH
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
esac

exit 0
