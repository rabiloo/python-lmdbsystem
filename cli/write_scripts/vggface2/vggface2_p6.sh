#!/bin/bash

set -eux

# Write Image
python cli/write_image.py --lmdb-file "/tmp/facedata/lmdb/vggface2_p6_image.lmdb" \
    --folder "/home/ubuntu/Downloads/RIB/VGGFACE2_Cleandata_p6" \
    --suffix .jpg \
    --fn-md5-mode w \
    --fn-md5-path "/tmp/facedata/lmdb/vggface2_p6_fn_md5.json"

# # Write Label From Dataset
python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/vggface2_p6_age_origin.lmdb" \
    --files "/tmp/facedata/labels/VGGFACE2_Cleandata_p6/label_origin.txt" \
    --delimiter "\t" \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/vggface2_p6_fn_md5.json"

# Write Label From Visage Tool
# python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/vggface2_p6_gender_visage.lmdb" \
#     --folder "/tmp/facedata/labels/VGGFACE2_Cleandata_p6/label_visage" \
#     --suffix .txt \
#     --delimiter "\n" \
#     --values-index 0 \
#     --fn-md5-mode r \
#     --fn-md5-path "/tmp/facedata/lmdb/vggface2_p6_fn_md5.json" \
#     --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
# python cli/write_text.py --lmdb-file "/tmp/facedata/lmdb/vggface2_p6_age_visage.lmdb" \
#     --folder "/tmp/facedata/labels/VGGFACE2_Cleandata_p6/label_visage" \
#     --suffix .txt \
#     --delimiter "\n" \
#     --values-index 1 \
#     --fn-md5-mode r \
#     --fn-md5-path "/tmp/facedata/lmdb/vggface2_p6_fn_md5.json"

# Write Label From Face++ Tool
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/vggface2_p6_gender_facepp.lmdb" \
    --folder "/tmp/facedata/labels/VGGFACE2_Cleandata_p6/label_facepp" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/vggface2_p6_fn_md5.json" \
    --keys-extracted "gender,value" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_json_facepp.py --lmdb-file "/tmp/facedata/lmdb/vggface2_p6_age_facepp.lmdb" \
    --folder "/tmp/facedata/labels/VGGFACE2_Cleandata_p6/label_facepp" \
    --suffix .json \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/facedata/lmdb/vggface2_p6_fn_md5.json" \
    --keys-extracted "age,value"
