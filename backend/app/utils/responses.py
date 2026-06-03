from flask import jsonify


def api_response(data=None, message: str = "", error: str | None = None, status: int = 200):
    body = {"success": status < 400, "message": message}
    if data is not None:
        body["data"] = data
    if error:
        body["error"] = error
    return jsonify(body), status
