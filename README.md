# How to use this prediction API sample scripts in Python

This script set refer google api client sample in Python, you can see original codes here [ google-api-python-client/samples/prediction ]( https://github.com/google/google-api-python-client/tree/master/samples/prediction ).
`prediction.py` is a sample code using OAuth credentials (JSON) link to your personal information on your Google Developer Console. `prediction_service.py` is also same, but it uses Service Account Credentials instead of personal OAuth2 credentials. 2nd one is to avoid OAuth2 browser authentication such as `Two Legged OAuth`.

## System Requirement

- Python 2.7
- Virtualenv

## Prepare your python environment using virtualevn

```
$ virtualenv venv
$ source venv/bin/activate
(venv)$ mkdir lib
(venv)$ pip install -t lib -r requirements.txt
```

## Working with Google Developer Console

- Create a project from Developer Console
- Enable 2 API which are Prediction API and Cloud Storage API.
- Create a OAuth2 credentials and populates it with name `client_secrets.json`.
- Create a ServiceAccount.
- Download credentials as. `<your-project-name>-xxxx.json` to place same level on your `client_secrets.json`
- Upload language_id.txt to your Cloud Storage

## Run prediction.py

```
$ python prediction.py "bucket/object" "model_id" "project_id"
```

## Run prediction_service.py

```
$ python prediction_service.py "bucket/object" "model_id" "project_id" "my-xxxxx.json"
```
