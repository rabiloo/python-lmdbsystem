#!/bin/bash

set -eux

# Write Image
python cli/write_image.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_image.lmdb" \
    --folder "/tmp/All-Age-Faces Dataset/original images" \
    --suffix .jpg \
    --fn-md5-mode w \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json"

# Write Label From Dataset
python cli/write_txt.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_gender_origin.lmdb" \
    --files "/tmp/All-Age-Faces Dataset/image sets/train.txt,/tmp/All-Age-Faces Dataset/image sets/val.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json"
python cli/write_txt.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_age_origin.lmdb" \
    --files "/tmp/All-Age-Faces Dataset/image sets/train.txt,/tmp/All-Age-Faces Dataset/image sets/val.txt" \
    --delimiter " " \
    --key-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json" \
    --pattern-value-in-key "\d{5}A(\d{2})" \
    --type-value-in-key int

# Write Label From Visage Tool
python cli/write_txt.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_gender_visage.lmdb" \
    --folder "/tmp/AAF_visage/AAF" \
    --suffix .txt \
    --delimiter "\n" \
    --values-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_txt.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_age_visage.lmdb" \
    --folder "/tmp/AAF_visage/AAF" \
    --suffix .txt \
    --delimiter "\n" \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json"

# Write Label From Face++ Tool
python cli/write_json_facepp.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_gender_facepp.lmdb" \
    --folder "/tmp/AAF_visage/AAF" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json" \
    --keys-extracted "gender,value" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_json_facepp.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_age_facepp.lmdb" \
    --folder "/tmp/AAF_visage/AAF" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json" \
    --keys-extracted "age,value"

# Write Label From Baidu Tool
python cli/write_json_baidu.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_gender_baidu.lmdb" \
    --folder "/tmp/AFF_baidu" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json" \
    --keys-extracted "gender,type" \
    --key-probability 0.9 \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_json_baidu.py --lmdb-file "/tmp/All-Age-Faces Dataset/aaf_age_baidu.lmdb" \
    --folder "/tmp/AFF_baidu" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/All-Age-Faces Dataset/aaf_fn_md5.json" \
    --keys-extracted "age"
