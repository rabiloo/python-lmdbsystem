#!/bin/bash

set -eux

# Write Label From Baidu Tool
root_data_path="/tmp/facedata/mount"
datasets=(
    #        "aaf"
    #        "afad"
    #        "afd"
    "deepglint"
    #        "fairface"
    "ffhq"
    #        "rfw"
    #        "utkface"
)
for dataset in "${datasets[@]}"; do
    echo "Handling with dataset: $dataset ..."
    echo "Building Gender LMDB File ..."
    ## Gender
    python cli/write_json_baidu.py \
        --lmdb-file "${root_data_path}/${dataset}/${dataset}_gender_baidu.lmdb" \
        --folder "${root_data_path}/${dataset}/label_baidu" \
        --suffix .json \
        --fn-md5-path "${root_data_path}/${dataset}/${dataset}_fn_md5.json" \
        --keys-extracted "gender,type" \
        --key-probability 0.9 \
        --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"

    echo "Building Age LMDB File  ..."
    ## Age
    python cli/write_json_baidu.py \
        --lmdb-file "${root_data_path}/${dataset}/${dataset}_age_baidu.lmdb" \
        --folder "${root_data_path}/${dataset}/label_baidu" \
        --suffix .json \
        --fn-md5-path "${root_data_path}/${dataset}/${dataset}_fn_md5.json" \
        --keys-extracted "age"

done
