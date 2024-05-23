#!/bin/bash

set -eux

# Write Image
root_data_path="/tmp/facedata/mount"
datasets=(
    "aaf;AAF/All-Age-Faces Dataset/original images;jpg"
    "afad;AFAD;jpg"
    "afd;generated_yellow-stylegan2;png"
    "deepglint;DeepGlint_7000;jpg"
    "fairface;fairface-img-margin125-trainval;jpg"
    "rfw;test/data;jpg"
    "utkface;UTKFace;jpg"
    #    "vggface2_cleandata_p1;VGGFACE2_Cleandata_p1;jpg"
    #    "vggface2_cleandata_p2;VGGFACE2_Cleandata_p2;jpg"
    #    "vggface2_cleandata_p3;VGGFACE2_Cleandata_p3;jpg"
    #    "vggface2_cleandata_p4;VGGFACE2_Cleandata_p4;jpg"
    #    "vggface2_cleandata_p5;VGGFACE2_Cleandata_p5;jpg"
    #    "vggface2_cleandata_p6;VGGFACE2_Cleandata_p6;jpg"
    #    "vggface2_cleandata_p7;VGGFACE2_Cleandata_p7;jpg"
    #    "vggface2_cleandata_p8;VGGFACE2_Cleandata_p8;jpg"
    #    "vggface2_cleandata_p9;VGGFACE2_Cleandata_p9;jpg"
    #    "vggface2_cleandata_p10;VGGFACE2_Cleandata_p10;jpg"
)
for dataset in "${datasets[@]}"; do
    IFS=$';'
    dataset_item=($dataset)
    unset IFS
    echo "Handling with dataset: ${dataset_item[0]} ..."

    python cli/write_image.py \
        --lmdb-file "${root_data_path}/${dataset_item[0]}/${dataset_item[0]}_image.lmdb" \
        --folder "${root_data_path}/${dataset_item[0]}/${dataset_item[1]}" \
        --suffix ".${dataset_item[2]}" \
        --fn-md5-mode w \
        --fn-md5-path "${root_data_path}/${dataset_item[0]}/${dataset_item[0]}_fn_md5.json"

done

# Special case for too large dataset
## FFHQ
python cli/write_image.py \
    --lmdb-file "/media/ubuntu/My Passport/ffhq_image.lmdb" \
    --folder "/media/ubuntu/My Passport/ffhq_1024x1024" \
    --suffix .png \
    --lmdb-map-size 214748364800 \
    --fn-md5-mode w \
    --fn-md5-path "${root_data_path}/ffhq/ffhq_fn_md5.json"

## Write Cleaned Image
#python cli/write_image.py --lmdb-file "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/aaf_image.lmdb" \
#    --folder "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/AAF" \
#    --suffix .jpg \
#    --fn-md5-mode r \
#    --fn-md5-path "/tmp/facedata/lmdb/aaf_fn_md5.json"

## Write Cleaned Image
#python cli/write_image.py --lmdb-file "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/fairface_image.lmdb" \
#    --folder "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/FairFace" \
#    --suffix .jpg \
#    --fn-md5-mode r \
#    --fn-md5-path "/tmp/facedata/lmdb/fairface_fn_md5.json"

## Write Cleaned Image
#python cli/write_image.py --lmdb-file "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/ffhq_image.lmdb" \
#    --folder "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/FFHQ" \
#    --suffix .png \
#    --fn-md5-mode r \
#    --fn-md5-path "/tmp/facedata/lmdb/ffhq_fn_md5.json"

## Write Cleaned Image
#python cli/write_image.py --lmdb-file "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/rfw_image.lmdb" \
#    --folder "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/RFW" \
#    --suffix .jpg \
#    --fn-md5-mode r \
#    --fn-md5-path "/tmp/facedata/lmdb/rfw_fn_md5.json"

## Write Cleaned Image
#python cli/write_image.py --lmdb-file "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/utkface_image.lmdb" \
#    --folder "/tmp/facedata/SCRFD_500M_KPS_ALIGN_224x224/UTKFace" \
#    --suffix .jpg \
#    --fn-md5-mode r \
#    --fn-md5-path "/tmp/facedata/lmdb/utkface_fn_md5.json"
