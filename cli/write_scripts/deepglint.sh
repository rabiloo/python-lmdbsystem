#!/bin/bash

set -eux

# Write Image
python cli/write_image.py --lmdb-file "/tmp/facedata/lmdb/deepglint_image.lmdb" \
   --folder "/tmp/facedata/original/DeepGlint_7000" \
   --suffix .jpg \
   --fn-md5-mode w \
   --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json"

# Write Label From Visage Tool
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/aaf_gender_visage.lmdb" \
   --folder "/tmp/facedata/labels/AAF/label_visage" \
   --suffix .txt \
   --delimiter "\n" \
   --values-index 0 \
   --fn-md5-mode r \
   --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json" \
   --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/aaf_age_visage.lmdb" \
   --folder "/tmp/facedata/labels/AAF/label_visage" \
   --suffix .txt \
   --delimiter "\n" \
   --values-index 1 \
   --fn-md5-mode r \
   --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json"

# Write Label From Face++ Tool
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/deepglint_gender_facepp.lmdb" \
   --folder "/tmp/facedata/labels/DeepGlint/label_facepp" \
   --suffix .json \
   --fn-md5-mode r \
   --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json" \
   --keys-extracted "gender,value" \
   --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/deepglint_age_facepp.lmdb" \
   --folder "/tmp/facedata/labels/DeepGlint/label_facepp" \
   --suffix .json \
   --fn-md5-mode r \
   --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json" \
   --keys-extracted "age,value"

# Write Label From Mivolo Tool
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/deepglint_age_mivolo.lmdb" \
   --files "/tmp/facedata/labels/DeepGlint/label_mivolo.txt" \
   --delimiter " " \
   --key-index 0 \
   --values-index 1 \
   --fn-md5-mode r \
   --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json"

# Write Label From MWR Tool
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/deepglint_age_mwr.lmdb" \
   --files "/tmp/facedata/labels/DeepGlint/label_mwr.txt" \
   --delimiter " " \
   --key-index 0 \
   --values-index 1 \
   --fn-md5-mode r \
   --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json"

# Write Label From Baidu Tool
python cli/write_json_baidu.py --lmdb-file "/tmp/facedata/lmdb/deepglint_gender_baidu.lmdb" \
    --folder "/tmp/facedata/labels/DeepGlint/label_baidu" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json" \
    --keys-extracted "gender,type" \
    --key-probability 0.9 \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_json_baidu.py --lmdb-file "/tmp/facedata/lmdb/deepglint_age_baidu.lmdb" \
    --folder "/tmp/facedata/labels/DeepGlint/label_baidu" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/deepglint_fn_md5.json" \
    --keys-extracted "age"
