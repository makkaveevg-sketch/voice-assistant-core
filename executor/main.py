import json
from executor import actions

def process_command(json_input):
    try:
        data = json.loads(json_input)
        action = data.get("action")
        params = data.get("parameters", {})
        
        if action == "open_app":
            return actions.open_app(params.get("app_name"))
            
        elif action == "close_app":
            return actions.close_app(params.get("app_name"))
            
        elif action == "open_url":
            return actions.open_url(params.get("url"))
            
        elif action == "shutdown_pc":
            return actions.shutdown_pc()
            
        elif action == "restart_pc":
            return actions.restart_pc()
            
        else:
            return "Ошибка: Неизвестное действие (action)"
            
    except Exception as e:
        return f"Ошибка парсинга JSON: {e}"

if __name__ == "__main__":

    test_json_open = '{"action": "open_app", "parameters": {"app_name": "discord"}}'
    print(process_command(test_json_open))