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

We suggest creating a Python 3.5 or higher virtualenv and use its binary to run the scripts. We made our tests using
a venv in the directory **_etc/bin/venv_** inside the project.

Install the requirements in the virtualenv. From the root directory of the project:

```
etc/bin/venv/bin/pip install -r requirements.txt
```

### API Credentials

#### Google API credentials

Use the --credentials option to provide the path to the client_secret.json file
when executing any script the calls the google API. The client_secret.json can be downloaded from your
[Google Developer Console](https://console.developers.google.com/apis/dashboard "Developer Console").

For example (from the project root):

```
etc/bin/venv/bin/python google_analytics_dump_property_list.py \
            --credentials etc/credentials/googleapi/client_secret.json
            --output etc/dump/GA_property_list.csv
```

#### AWS API credentials

Configure your credentials using the AWS CLI:

```
$ aws configure

 > AWS Access Key ID [None]: Your Access Key
 > AWS Secret Access Key [None]: Your Secret Access Key
 > Default region name [None]: us-west-2
 > Default output format [None]: json
```

You can find the _Access Key_ and the _Secret Access Key_ in the AWS console.

[More info here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html "AWS CLI")

#### Monitis credentials

Create a credentials file for Monitis with the following content:

```
{
  "api_key": "your api key",
  "secret_key": "your secret key",
  "agent_key": "your agent key",
  "user_key": "your user key"
}
```

- The _API key_ and the _secret key_ can be obtained in the Monitis' _**Tools > API**_ menu.
- The _agent key_ can be found in Monitis' _**Tools > Agent_** menu

The secret key however can be found using the Network tool of a browser and request the listing of
monitors on the Monitis' website.

## Executing the scripts

### Google Analytics Properties Dump

Dum the list of all Google Analytics properties in a CSV file. Example:

```
etc/bin/venv/bin/python google_analytics_dump_property_list.py \
            --credentials etc/credentials/googleapi/client_secret.json
            --output etc/dump/GA_property_list.csv
```

### Google Search Console Add Sites From Analytics Properties

Add sites in Google Search Console from a list of properties previously dumped from
Google Analytics.

```
etc/bin/venv/bin/python google_search_console_add_from_analytics_property_list.py \
            --credentials etc/credentials/googleapi/client_secret.json
            --input etc/dump/GA_property_list.csv
```

### Google Tag Manager Add Tag From Analytics Properties

Add tags in Google Tag Manager from a list of properties previously dumped from
Google Analytics.

```
etc/bin/venv/bin/python google_tagmanager_add_from_analytics_property_list.py \
            --credentials etc/credentials/googleapi/client_secret.json
            --input etc/dump/GA_property_list.csv
```

### Monitis Add Monitors From Analytics Properties

Add monitors in Monitis from a list of properties previously dumped from
Google Analytics.

```
etc/bin/venv/bin/python monitis_add_monitor_from_GA_property_list.py \
            --credentials etc/credentials/monitisapi/secret_credentials.json
            --input etc/dump/GA_property_list.csv
```

### Monitis Dump Monitors list

Dum the list of all Monitis RUM monitors in a CSV file.

```
etc/bin/venv/bin/python monitis_dump_monitor_list.py \
            --credentials etc/credentials/monitisapi/secret_credentials.json
            --output etc/dump/monitis_rum_monitors.csv
```