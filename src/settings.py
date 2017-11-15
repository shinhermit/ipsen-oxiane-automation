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
    "action": {
        "add_rum": "addCompositeMonitor",
        "get_auth_token": "authToken"
    },
    "default_tag": '["Default"]',
    "version": "2",
    "custom_action": {
        "base_url": "http://api.monitis.com/customMonitorApi"
    },
    "credentials": {
        # apy key from the monitis account, in the Tools > API menu.
        "api_key": "24DRL1UFK3FU4LECK8C3JCGLFA",
        "secret_key": "5N5BMKERKKK1S7FER2GLEBF7M4",
        "auth_method": "token"
    },
    "monitor": {
        "monitor_params": ("ignoreQueryParams:IgnoreQueryParams:true:1:"
                           "false:false;domain:Domain:ipsen-oxiane.blogspot.fr:1:"
                           "false:false;aggType:AggType:median:1:false:false;"),
        "result_params": "position:Position:N/A:2;difference:Difference:N/A:3;",
        "monitor_type": "RUM"
    }
}
