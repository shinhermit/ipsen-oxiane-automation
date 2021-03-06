

googleapi = {
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
    },
    "tag_manager": {
        "api_name": "tagmanager",
        "api_version": "v2",
        "scopes": ['https://www.googleapis.com/auth/tagmanager.edit.containers',
                   'https://www.googleapis.com/auth/tagmanager.readonly']
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
        "auth_method": "token"
    },
    "monitor": {
        "monitor_default_type": "RUM",
        "default_tag": '["test"]',
        "monitor_params": ("ignoreQueryParams:IgnoreQueryParams:true:1:"
                           "false:false;aggType:AggType:median:1:false:false;"),
        "result_params": "position:Position:N/A:2;difference:Difference:N/A:3;"
    }
}