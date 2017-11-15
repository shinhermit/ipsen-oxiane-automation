

googleapi = {
    "credentials": {
        "client_secret_path": "./etc/credentials/client_secret.json",
        "credentials_base_path": "./etc/credentials/"
    },
    "analytics": {
        "api_name": "analytics",
        "api_version": "v3",
        "scopes": ["https://www.googleapis.com/auth/analytics.edit",
                   "https://www.googleapis.com/auth/analytics.readonly"]
    },
    "search_console": {
        "api_name": "webmasters",
        "api_version": "v3",
        "scopes": ['https://www.googleapis.com/auth/webmasters',
                   'https://www.googleapis.com/auth/webmasters.readonly']
    }
}

monitisapi = {
    "api_url": "http://dashboard.monitis.com/customMonitorApi",
    "version": "2",
    "actions": {
        "add_rum": "addCompositeMonitor",
        "get_auth_token": "authToken"
    },
    "credentials": {  # Most values are from Monitis's Tools menu.
        "api_key": "24DRL1UFK3FU4LECK8C3JCGLFA",
        "secret_key": "5N5BMKERKKK1S7FER2GLEBF7M4",
        "agent_key": "4HJLF3JQJPGOCBE8EP5IE8BT0G",
        "auth_method": "token"
    },
    "monitor": {
        "monitor_type": "RUM",
        "monitor_test_type": "http",
        "default_tag": '["test"]',
        "monitor_params": ("ignoreQueryParams:IgnoreQueryParams:true:1:"
                           "false:false;aggType:AggType:median:1:false:false;"),
        "result_params": "position:Position:N/A:2;difference:Difference:N/A:3;",
    }
}
