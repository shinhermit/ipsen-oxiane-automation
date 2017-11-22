

googleapi = {
    "credentials": {
        "client_secret_path": "./etc/credentials/googleapi/client_secret.json",
        "credentials_base_path": "./etc/credentials/googleapi/"
    },
    "analytics": {
        "api_name": "analytics",
        "api_version": "v3",
        "scopes": ["https://www.googleapis.com/auth/analytics.edit",
                   "https://www.googleapis.com/auth/analytics.readonly"],
        "dump_file": "./etc/dump/GA_property_list.csv"
    },
    "search_console": {
        "api_name": "webmasters",
        "api_version": "v3",
        "scopes": ['https://www.googleapis.com/auth/webmasters',
                   'https://www.googleapis.com/auth/webmasters.readonly']
    }
}

monitisapi = {
    "search_url": "http://dashboard.monitis.com/layout/{user_key}/searchitem",
    "api_url": "http://dashboard.monitis.com/customMonitorApi",
    "api_version": "2",
    "api_actions": {
        "add_rum": "addCompositeMonitor",
        "get_auth_token": "authToken"
    },
    "credentials": {
        # Most values are from Monitis's Tools menu.
        "client_secret_path": "./etc/credentials/monitisapi/secret_credentials.json",
        "auth_method": "token"
    },
    "monitor": {
        "monitor_default_type": "RUM",
        "default_tag": '["test"]',
        "monitor_params": ("ignoreQueryParams:IgnoreQueryParams:true:1:"
                           "false:false;aggType:AggType:median:1:false:false;"),
        "result_params": "position:Position:N/A:2;difference:Difference:N/A:3;",
        "dump_file": "./etc/dump/rum_monitors.csv"
    }
}


awsapi = {
    "route53": {
        "dump_file_path": "./etc/dump/AWS_backup_files/"
    }
}