#!/bin/sh

WDIR="[本ツール（data_setup）が置かれているディレクトリ]"
TDIR="data_setup"
SDIR="script"
IDIR="input_data"
ODIR="gen_data"
MDIR="covid19"

SPATH=${WDIR}/${TDIR}/${SDIR}
IPATH=${WDIR}/${TDIR}/${IDIR}
OPATH=${WDIR}/${TDIR}/${ODIR}
MPATH=${WDIR}/${MDIR}

# exec

echo "${SPATH}/get_data.py"
      ${SPATH}/get_data.py

echo "${SPATH}/gen_json.py"
      ${SPATH}/gen_json.py

echo "${SPATH}/merge_json.py"
      ${SPATH}/merge_json.py

echo "sed 's/\\\\/\\/g' ${OPATH}/data_new.json > ${OPATH}/data.json"
      sed 's/\\\\/\\/g' ${OPATH}/data_new.json > ${OPATH}/data.json

# to master

echo "cp ${OPATH}/data.json ${MPATH}/data/data.json"
      cp ${OPATH}/data.json ${MPATH}/data/data.json

echo "cd ${MPATH}"
      cd ${MPATH}

echo "yarn build"
      yarn build

echo "systemctl restart fukuoka-city"
      systemctl restart fukuoka-city
