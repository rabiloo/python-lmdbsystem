#!/bin/bash

set -eux

# Write Image
python cli/write_image.py --lmdb-file "/tmp/facedata/lmdb/utkface_image.lmdb" \
    --folder "/tmp/facedata/original/UTKFace" \
    --suffix .jpg \
    --fn-md5-mode w \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json"

# Write Label From Dataset
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/utkface_gender_origin.lmdb" \
    --folder "/tmp/facedata/original/UTKFace" \
    --suffix .jpg \
    --delimiter "_" \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json" \
    --from-filename
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/utkface_age_origin.lmdb" \
    --folder "/tmp/facedata/original/UTKFace" \
    --suffix .jpg \
    --delimiter "_" \
    --values-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json" \
    --from-filename

# Write Label From Visage Tool
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/utkface_gender_visage.lmdb" \
    --folder "/tmp/facedata/labels/UTKFace/label_visage" \
    --suffix .txt \
    --delimiter "\n" \
    --values-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/utkface_age_visage.lmdb" \
    --folder "/tmp/facedata/labels/UTKFace/label_visage" \
    --suffix .txt \
    --delimiter "\n" \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json"

# Write Label From Face++ Tool
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/utkface_gender_facepp.lmdb" \
    --folder "/tmp/facedata/labels/UTKFace/label_facepp" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json" \
    --keys-extracted "gender,value" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/utkface_age_facepp.lmdb" \
    --folder "/tmp/facedata/labels/UTKFace/label_facepp" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json" \
    --keys-extracted "age,value"

# Write Label From Mivolo Tool
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/utkface_age_mivolo.lmdb" \
    --files "/tmp/facedata/labels/UTKFace/label_mivolo.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json"

# Write Label From MWR Tool
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/utkface_age_mwr.lmdb" \
    --files "/tmp/facedata/labels/UTKFace/label_mwr.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json"

# Write Cleaned Image
python cli/write_image.py --lmdb-file "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/utkface_image.lmdb" \
    --folder "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/UTKFace" \
    --suffix .jpg \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json"
