#!/bin/bash

set -eux

## Write Label From Dataset
root_data_path="/tmp/facedata/mount"
# AAF
## Gender
python cli/write_text_label_in_some_txt.py \
    --lmdb-file "${root_data_path}/aaf/aaf_gender_origin.lmdb" \
    --files "${root_data_path}/aaf/AAF/All-Age-Faces Dataset/image sets/train.txt,${root_data_path}/aaf/AAF/All-Age-Faces Dataset/image sets/val.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-path "${root_data_path}/aaf/aaf_fn_md5.json"
## Age
python cli/write_text_label_in_filename.py \
    --lmdb-file "${root_data_path}/aaf/aaf_age_origin.lmdb" \
    --folder "${root_data_path}/aaf/AAF/All-Age-Faces Dataset/original images" \
    --suffix .jpg \
    --delimiter "A" \
    --values-index 1 \
    --fn-md5-path "${root_data_path}/aaf/aaf_fn_md5.json" \
    --values-map "type:int"

# AFAD
## Gender
python cli/write_text_label_in_key_in_some_txt.py \
    --lmdb-file "${root_data_path}/afad/afad_gender_origin.lmdb" \
    --files "${root_data_path}/afad/AFAD/AFAD-Full.txt" \
    --delimiter " " \
    --key-index 0 \
    --fn-md5-path "${root_data_path}/afad/afad_fn_md5.json" \
    --pattern-value-in-key "/(\d{3})/" \
    --type-value-in-key int \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
## Age
python cli/write_text_label_in_key_in_some_txt.py \
    --lmdb-file "${root_data_path}/afad/afad_age_origin.lmdb" \
    --files "${root_data_path}/afad/AFAD/AFAD-Full.txt" \
    --delimiter " " \
    --key-index 0 \
    --fn-md5-path "${root_data_path}/afad/afad_fn_md5.json" \
    --pattern-value-in-key "/(\d{2})/" \
    --type-value-in-key int

# FairFace
## Gender
python cli/write_text_label_in_some_csv.py \
    --lmdb-file "${root_data_path}/fairface/fairface_gender_origin.lmdb" \
    --files "${root_data_path}/fairface/fairface_label_train.csv,${root_data_path}/facefair/fairface_label_val.csv" \
    --delimiter "," \
    --key-index 0 \
    --values-index 2 \
    --fn-md5-path "${root_data_path}/fairface/fairface_fn_md5.json" \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0" \
    --skip-header
## Age
python cli/write_text_label_in_some_csv.py \
    --lmdb-file "${root_data_path}/fairface/fairface_age_origin.lmdb" \
    --files "${root_data_path}/fairface/fairface_label_train.csv,${root_data_path}/facefair/fairface_label_val.csv" \
    --delimiter "," \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-path "${root_data_path}/fairface/fairface_fn_md5.json" \
    --skip-header

# FFHQ
## Age
python cli/write_text_label_in_some_txt.py \
    --lmdb-file "${root_data_path}/ffhq/ffhq_age_human.lmdb" \
    --files "${root_data_path}/ffhq/label_human.txt" \
    --delimiter " " \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-path "${root_data_path}/ffhq/ffhq_fn_md5.json"

# UTKFace
## Gender
python cli/write_text_label_in_filename.py \
    --lmdb-file "${root_data_path}/utkface/utkface_gender_origin.lmdb" \
    --folder "${root_data_path}/utkface/UTKFace" \
    --suffix .jpg \
    --delimiter "_" \
    --values-index 1 \
    --fn-md5-path "${root_data_path}/utkface/utkface_fn_md5.json" \
    --values-map "0:1,1:0"
## Age
python cli/write_text_label_in_filename.py \
    --lmdb-file "${root_data_path}/utkface/utkface_age_origin.lmdb" \
    --folder "${root_data_path}/utkface/UTKFace" \
    --suffix .jpg \
    --delimiter "_" \
    --values-index 0 \
    --fn-md5-path "${root_data_path}/utkface/utkface_fn_md5.json"

# VGGFACE2_Cleandata_p1
## Age
python cli/write_text_label_in_some_txt.py \
    --lmdb-file "${root_data_path}/vggface2_cleandata_p1/vggface2_cleandata_p1_age_origin.lmdb" \
    --files "${root_data_path}/vggface2_cleandata_p1/label_origin.txt" \
    --delimiter "\t" \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-path "${root_data_path}/vggface2_cleandata_p1/vggface2_cleandata_p1_fn_md5.json"

# VGGFACE2_Cleandata_p2
## Age
python cli/write_text_label_in_some_txt.py \
    --lmdb-file "${root_data_path}/vggface2_cleandata_p2/vggface2_cleandata_p2_age_origin.lmdb" \
    --files "${root_data_path}/vggface2_cleandata_p2/label_origin.txt" \
    --delimiter "\t" \
    --key-index 0 \
    --values-index 1 \
    --fn-md5-path "${root_data_path}/vggface2_cleandata_p2/vggface2_cleandata_p2_fn_md5.json"

# To p10
