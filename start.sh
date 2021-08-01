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

case $1 in
-r|--run)
cd $PROGRAMM_PATH
$PY $PROGRAMM_NAME
;;
-c|--clean)
rm -rf $PROGRAMM_PATH/$CLEAN_NAME
;;
-rq|--requiretments)
$PIP install -r $REQUIRETMENTS_PATH
;;
esac

exit 0
