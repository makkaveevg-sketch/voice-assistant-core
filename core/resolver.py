from core.app_map import APP_MAP


def resolve(command: dict):

    action = command.get("action")
    params = command.get("parameters", {})
    target = params.get("target")

    # 🔥 OPEN
    if action == "open":

        if not target:
            return {"status": "error", "message": "missing target"}

        target = target.lower().strip()

        if target not in APP_MAP:
            return {
                "status": "error",
                "message": f"unknown target: {target}"
            }

        app = APP_MAP[target]

        return {
            "status": "ok",
            "action": "open",
            "type": app["type"],
            "value": app["value"]
        }

    # 🔥 CLOSE (пока заготовка под Андрея)
    if action == "close":
        return {
            "status": "ok",
            "action": "close",
            "target": target
        }

    # 🔥 SYSTEM ACTIONS
    if action == "shutdown_pc":
        return {"status": "ok", "action": "shutdown_pc"}

    if action == "restart_pc":
        return {"status": "ok", "action": "restart_pc"}

    # 🔥 SCENARIO HOOK (будущее)
    if action == "scenario":
        return {
            "status": "ok",
            "action": "scenario",
            "name": params.get("name")
        }

    return {
        "status": "unknown",
        "raw": command
    }