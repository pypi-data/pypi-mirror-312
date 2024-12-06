import requests

def calculate_overall_load(data):
    try:
        cpu = data.get("cpu_usage_percent", 0)
        memory = data.get("memory_usage_percent", 0)
        disk = data.get("disk_usage_percent", 0)
        return round((cpu + memory + disk) / 3, 2)
    except Exception:
        return None

def get_server_load(server_url):
    try:
        response = requests.get(f"{server_url}/status")
        if response.status_code == 200:
            data = response.json()
            overall_load = calculate_overall_load(data)
            return overall_load
        else:
            print(f"Failed to get load from {server_url}, status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting server load from {server_url}: {e}")
        return None

def is_spam(message, model_name='spamNS_v6', user_token=None): 
    """
    Проверяет, является ли сообщение спамом, и отправляет запрос на менее загруженный сервер.
    
    :param message: Строка сообщения для анализа.
    :param model_name: Имя модели для использования (по умолчанию: 'spamNS_v6').
    :param user_token: Токен API для аутентификации.
    
    :return: Словарь с результатами анализа (включая is_spam, confidence, model_used, tokens_used, cost, api_key).
    """
    if not user_token:
        print("API token is required for authentication.")
        return {
            "is_spam": False,
            "confidence": 0.0,
            "model_used": None,
            "tokens_used": 0,
            "cost": 0.0,
            "api_key": None,
        }
    
    api_urls = [
        "https://neurospacex-ruspamtwo.hf.space/api/check_spam",
        "https://neurospacex-ruspam.hf.space/api/check_spam"
    ]
    
    server_loads = {url: get_server_load(url.replace("/api/check_spam", "/api/")) for url in api_urls}
    
    available_servers = {url: load for url, load in server_loads.items() if load is not None}
    
    selected_server = min(available_servers, key=available_servers.get, default=None)
    
    if not selected_server:
        print("No available servers found.")
        return {
            "is_spam": False,
            "confidence": 0.0,
            "model_used": model_name,
            "tokens_used": 0,
            "cost": 0.0,
            "api_key": user_token,
        }
    
    headers = {
        "api-key": user_token
    }
    data = {
        "message": message,
        "model_name": model_name
    }
    
    try:
        response = requests.post(selected_server, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"Response received from server: {selected_server}")

            return {
                "is_spam": result.get('is_spam', 0) == 1,
                "confidence": result.get('confidence', 0.0),
                "model_used": result.get('model_used', model_name),
                "tokens_used": result.get('tokens_used', 0),
                "cost": result.get('cost', 0.0),
                "api_key": result.get('api_key', user_token),
            }
        else:
            print(f"Server at {selected_server} failed with status code {response.status_code}.")
            if response.status_code == 400:
                result = response.json()
                if 'error' in result:
                    print(f"Error: {result['error']}")
    except requests.exceptions.RequestException as e:
        print(f"Network error while connecting to {selected_server}: {e}")
    
    print("Failed to process the request.")
    return {
        "is_spam": False,
        "confidence": 0.0,
        "model_used": model_name,
        "tokens_used": 0,
        "cost": 0.0,
        "api_key": user_token,
    }
