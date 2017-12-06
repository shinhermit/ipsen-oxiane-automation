# ipsen-oxiane-automation

## Description

Various automation scripts to synchronize:

- Google Analytics
- Google Search Console
- Google Tag Manager
- AWS Route 53
- Monitis RUM monitors

## Setup

### Python executable

Create a Python 3.5 or higher venv and its binary to run the scripts. We made our tests using
a venv in the directory **_etc/bin/venv_** inside the project

### API Credentials

#### Google API credentials

The location of the client_secret.json is defined in the settings.py file and defaults to:

```
./etc/credentials/googleapi/client_secret.json
```