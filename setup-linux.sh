#!/bin/sh
#
# (c) 2020 Yoichi Tanibayashi
#
MYNAME=`basename $0`

SRC_DIR=`pwd`
DST_DIR=${HOME}/.config/inkscape/extensions

if [ ! -d ${DST_DIR} ]; then
    mkdir -pvf ${DST_DIR}
fi

cd ${DST_DIR}
pwd
ln -sfv ${SRC_DIR}/*.inx ${SRC_DIR}/*.py .
