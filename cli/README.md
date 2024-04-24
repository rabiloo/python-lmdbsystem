


## Write LMDB with All-Age-Faces Dataset
### Structure Dataset
```
├── aglined faces
│   ├── 00000A02.jpg
│   ├── 00001A02.jpg
│   ├── ...
├── example
├── image sets
│   ├── train.txt
│   ├── val.txt
├── key points
├── original images
│   ├── 00000A02.jpg
│   ├── 00001A02.jpg
│   ├── ...
```
### CMD
```shell
bash cli/aaf.sh
```

## Write LMDB with AFAD
### Structure Dataset
```
├── 15
│   ├── 111
│   |   ├── 292943-1.jpg
│   |   ├── 292943-2.jpg
│   ├── 112
│   |   ├── 671487-0.jpg
│   |   ├── 660728-0.jpg
├── ...
├── 75
├── README.md
├── AFAD-Full.txt
```
### CMD
```shell
bash cli/afad.sh
```
