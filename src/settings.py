googleapi = {
    "credentials": {
        "client_secret_path": "etc/credentials/client_secret.json"
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
        "base_url": "http://api.monitis.com/api",
    },
    "custom_action": {
        "base_url": "http://api.monitis.com/customMonitorApi"
    }
}