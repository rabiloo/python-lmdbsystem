#!/bin/bash

set -eux

# Write Image
python cli/write_image.py --lmdb-file "/tmp/facedata/lmdb/aaf_image.lmdb" \
    --folder "/tmp/facedata/original/All-Age-Faces Dataset/original images" \
    --suffix .jpg \
    --fn-md5-mode w \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json"

# Write Label From Dataset
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/aaf_gender_origin.lmdb" \
    --files "/tmp/facedata/original/All-Age-Faces Dataset/image sets/train.txt,/tmp/facedata/original/All-Age-Faces Dataset/image sets/val.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json"
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/aaf_age_origin.lmdb" \
    --files "/tmp/facedata/original/All-Age-Faces Dataset/image sets/train.txt,/tmp/facedata/original/All-Age-Faces Dataset/image sets/val.txt" \
    --delimiter " " \
    --key-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json" \
    --pattern-value-in-key "\d{5}A(\d{2})" \
    --type-value-in-key int

# Write Label From Visage Tool
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/aaf_gender_visage.lmdb" \
    --folder "/tmp/facedata/labels/AAF/label_visage" \
    --suffix .txt \
    --delimiter "\n" \
    --values-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/aaf_age_visage.lmdb" \
    --folder "/tmp/facedata/labels/AAF/label_visage" \
    --suffix .txt \
    --delimiter "\n" \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json"

# Write Label From Face++ Tool
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/aaf_gender_facepp.lmdb" \
    --folder "/tmp/facedata/labels/AAF/label_facepp" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json" \
    --keys-extracted "gender,value" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/aaf_age_facepp.lmdb" \
    --folder "/tmp/facedata/labels/AAF/label_facepp" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json" \
    --keys-extracted "age,value"

# Write Label From Mivolo Tool
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/aaf_age_mivolo.lmdb" \
    --files "/tmp/facedata/labels/AAF/label_mivolo.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json"

# Write Label From MWR Tool
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/aaf_age_mwr.lmdb" \
    --files "/tmp/facedata/labels/AAF/label_mwr.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json"

## Write Label From Baidu Tool
#python cli/write_json_baidu.py --lmdb-file "/tmp/facedata/lmdb/aaf_gender_baidu.lmdb" \
#    --folder "/tmp/facedata/labels/AAF/label_baidu" \
#    --suffix .json \
#    --fn-md5-mode r \
#    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json" \
#    --keys-extracted "gender,type" \
#    --key-probability 0.9 \
#    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
#python cli/write_json_baidu.py --lmdb-file "/tmp/facedata/lmdb/aaf_age_baidu.lmdb" \
#    --folder "/tmp/facedata/labels/AAF/label_baidu" \
#    --suffix .json \
#    --fn-md5-mode r \
#    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json" \
#    --keys-extracted "age"


# Write Cleaned Image
python cli/write_image.py --lmdb-file "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/aaf_image.lmdb" \
    --folder "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/AAF" \
    --suffix .jpg \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json"
