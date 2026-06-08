import json
from executor import actions


def process_command(json_input):
    try:
        data = json.loads(json_input)
        action = data.get("action")
        params = data.get("parameters", {})
        
        if action == "open_app":
            app_name = params.get("app_name")
            is_admin = params.get("as_admin", False) # Проверяем, нужны ли права

            return actions.open_app(app_name, as_admin=is_admin)
            
        elif action == "close_app":
            return actions.close_app(params.get("app_name"))
            
        elif action == "open_url":
            return actions.open_url(params.get("url"))
            
        elif action == "shutdown_pc":
            return actions.shutdown_pc()
            
        elif action == "restart_pc":
            return action.restart_pc()
            
        else:
            return "Действие нераспознанно"
            
    except Exception as e:
        return f"Ошибка парсинга JSON: {e}"

if __name__ == "__main__":

    #test_open_app = '{"action": "open_app", "parameters": {"app_name": "discord"}}'
    #test_zapret = '{"action": "open_app", "parameters": {"app_name": "zapret", "as_admin": true}}'
    test_open_url = '{"action": "open_url", "parameters": {"url": "youtube"}}'
    #test_close_app = '{"action": "close_app", "parameters": {"app_name": "discord"}}'
    print(process_command(test_open_url))