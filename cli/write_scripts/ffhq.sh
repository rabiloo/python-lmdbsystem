#!/bin/bash

set -eux

# Write Image
python cli/write_image.py --lmdb-file "/tmp/facedata/lmdb/ffhq_image.lmdb" \
    --folder "/tmp/facedata/original/ffhq_1024x1024" \
    --suffix .png \
    --lmdb-map-size 214748364800 \
    --fn-md5-mode w \
    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json"

#python cli/write_image.py --lmdb-file "/media/ubuntu/My Passport/ffhq_image.lmdb" \
#    --folder "/media/ubuntu/My Passport/ffhq_1024x1024" \
#    --suffix .png \
#    --lmdb-map-size 214748364800 \
#    --fn-md5-mode w \
#    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json"

# Write Label From Human
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/ffhq_age_human.lmdb" \
    --files "/tmp/facedata/labels/FFHQ/label_human.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json"

# Write Label From Visage Tool
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/ffhq_gender_visage.lmdb" \
    --folder "/tmp/facedata/labels/FFHQ/label_visage" \
    --suffix .txt \
    --delimiter "\n" \
    --values-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_txt.py --lmdb-file "/tmp/facedata/lmdb/ffhq_age_visage.lmdb" \
    --folder "/tmp/facedata/labels/FFHQ/label_visage" \
    --suffix .txt \
    --delimiter "\n" \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json"

# Write Label From Face++ Tool
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/ffhq_gender_facepp.lmdb" \
    --folder "/tmp/facedata/labels/FFHQ/label_facepp" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json" \
    --keys-extracted "gender,value" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/ffhq_age_facepp.lmdb" \
    --folder "/tmp/facedata/labels/FFHQ/label_facepp" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json" \
    --keys-extracted "age,value"

# Write Cleaned Image
python cli/write_image.py --lmdb-file "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/ffhq_image.lmdb" \
    --folder "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/FFHQ" \
    --suffix .png \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json"
