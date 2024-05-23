#!/bin/bash

set -eux

# Write Label From Facepp Tool
root_data_path="/tmp/facedata/mount"
datasets=(
    "aaf"
    "afad"
    "afd"
    "deepglint"
    "fairface"
    "ffhq"
    "rfw"
    "utkface"
    #    "vggface2_cleandata_p1"
    #    "vggface2_cleandata_p2"
    #    "vggface2_cleandata_p3"
    #    "vggface2_cleandata_p4"
    #    "vggface2_cleandata_p5"
    #    "vggface2_cleandata_p6"
    #    "vggface2_cleandata_p7"
    #    "vggface2_cleandata_p8"
    #    "vggface2_cleandata_p9"
    #    "vggface2_cleandata_p10"
)
for dataset in "${datasets[@]}"; do
    echo "Handling with dataset: $dataset ..."
    echo "Building Gender LMDB File ..."
    ## Gender
    python cli/write_json_facepp.py \
        --lmdb-file "${root_data_path}/${dataset}/${dataset}_gender_facepp.lmdb" \
        --folder "${root_data_path}/${dataset}/label_facepp" \
        --suffix .json \
        --fn-md5-path "${root_data_path}/${dataset}/${dataset}_fn_md5.json" \
        --keys-extracted "gender,value" \
        --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"

    echo "Building Age LMDB File  ..."
    ## Age
    python cli/write_json_facepp.py \
        --lmdb-file "${root_data_path}/${dataset}/${dataset}_age_facepp.lmdb" \
        --folder "${root_data_path}/${dataset}/label_facepp" \
        --suffix .json \
        --fn-md5-path "${root_data_path}/${dataset}/${dataset}_fn_md5.json" \
        --keys-extracted "age,value"

done
