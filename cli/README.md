# Face Dataset
## Sample Label of 3rd Tools
<details>
<summary>Facepp</summary>

```yaml
{
  "request_id": "1699959145,1bb349e4-c83f-4a39-ad4e-8dcdc0cd34fb",
  "time_used": 0,
  "faces": [
    {
      "face_token": "974b332135a90dd90ac8c685fa983a69",
      "face_rectangle": {
        "top": 158,
        "left": 66,
        "width": 191,
        "height": 191
      },
      "attributes": {
        "gender": {
          "value": "Female"
        },
        "age": {
          "value": 3
        },
        "headpose": {
          "pitch_angle": 6.6730194,
          "roll_angle": -2.4714718,
          "yaw_angle": 3.7413023
        },
        "eyestatus": {
          "left_eye_status": {
            "no_glass_eye_open": 99.357,
            "no_glass_eye_close": 0,
            "normal_glass_eye_open": 0.635,
            "normal_glass_eye_close": 0.001,
            "dark_glasses": 0,
            "occlusion": 0.007
          },
          "right_eye_status": {
            "no_glass_eye_open": 99.763,
            "no_glass_eye_close": 0.011,
            "normal_glass_eye_open": 0.054,
            "normal_glass_eye_close": 0.005,
            "dark_glasses": 0.01,
            "occlusion": 0.158
          }
        },
        "emotion": {
          "anger": 22.269,
          "disgust": 1.227,
          "fear": 0.41,
          "happiness": 9.247,
          "neutral": 12.255,
          "sadness": 54.181,
          "surprise": 0.41
        },
        "facequality": {
          "value": 90.754,
          "threshold": 70.1
        },
        "ethnicity": {
          "value": ""
        },
        "beauty": {
          "male_score": 52.808,
          "female_score": 47.62
        },
        "mouthstatus": {
          "surgical_mask_or_respirator": 0,
          "other_occlusion": 0.004,
          "close": 0.245,
          "open": 99.751
        },
        "glass": {
          "value": "None"
        }
      }
    }
  ],
  "image_id": "zGJ7eeUqKzu0NJBxIodt7w==",
  "face_num": 1
}
```

</details>

<details>
<summary>Baidu</summary>

```yaml
{
  "face_list": [
    {
      "face_token": "2df98fc10747d685e4dd4794f91a9c26",
      "location": {
        "left": 18.03,
        "top": 41.28,
        "width": 88,
        "height": 74,
        "rotation": -2
      },
      "face_probability": 1,
      "angle": {
        "yaw": 5.83,
        "pitch": 2.12,
        "roll": -3.13
      },
      "age": 33,
      "expression": {
        "type": "none",
        "probability": 1
      },
      "face_shape": {
        "type": "square",
        "probability": 0.73
      },
      "gender": {
        "type": "male",
        "probability": 0.99
      },
      "glasses": {
        "type": "none",
        "probability": 1
      },
      "landmark150": {},
      "quality": {
        "occlusion": {
          "left_eye": 0,
          "right_eye": 0,
          "nose": 0,
          "mouth": 0,
          "left_cheek": 0.42,
          "right_cheek": 0.52,
          "chin_contour": 0.8
        },
        "blur": 0,
        "illumination": 129,
        "completeness": 1
      },
      "emotion": {
        "type": "neutral",
        "probability": 0.83
      },
      "mask": {
        "type": 0,
        "probability": 0.96
      }
    }
  ],
  "face_num": 1
}
```

</details>

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
Origin label of dataset get from "image sets/train.txt" and "image sets/val.txt"
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
Origin label of dataset get from "AFAD-Full.txt"
### CMD
```shell
bash cli/afad.sh
```
