#!/bin/bash

set -eux

# Write Image
python cli/write_image.py --lmdb-file "/tmp/AFAD/afad_image.lmdb" \
    --folder "/tmp/AFAD" \
    --suffix .jpg \
    --fn-md5-mode w \
    --fn-md5-path "/tmp/AFAD/afad_fn_md5.json"

# Write Label From Dataset
python cli/write_txt.py --lmdb-file "/tmp/AFAD/afad_gender_origin.lmdb" \
    --files "/tmp/AFAD/AFAD-Full.txt" \
    --delimiter " " \
    --key-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/AFAD/afad_fn_md5.json" \
    --pattern-value-in-key "/(\d{3})/" \
    --type-value-in-key int \
    --values-map "Female:0,Male:1,female:0,male:1,111:1,112:0"
python cli/write_txt.py --lmdb-file "/tmp/AFAD/afad_age_origin.lmdb" \
    --files "/tmp/AFAD/AFAD-Full.txt" \
    --delimiter " " \
    --key-index 0 \
    --fn-md5-mode r \
    --fn-md5-path "/tmp/AFAD/afad_fn_md5.json" \
    --pattern-value-in-key "/(\d{2})/" \
    --type-value-in-key int
