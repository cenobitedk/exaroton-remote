import requests

BASE = "https://api.exaroton.com/v1"

STATUS_LABELS = {
    0: "Offline",
    1: "Online",
    2: "Starting",
    3: "Stopping",
    4: "Restarting",
    5: "Saving",
    6: "Loading",
    7: "Crashed",
    8: "Pending",
    9: "Transferring",
    10: "Preparing",
}


class ExarotonAPI:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {token}"

    def _get(self, path: str):
        r = self.session.get(f"{BASE}{path}", timeout=10)
        r.raise_for_status()
        data = r.json()
        if not data.get("success"):
            raise RuntimeError(data.get("error", "Unknown API error"))
        return data["data"]

    def account(self):
        return self._get("/account/")

    def servers(self):
        return self._get("/servers/")

    def server(self, server_id: str):
        return self._get(f"/servers/{server_id}/")

    def start(self, server_id: str):
        return self._get(f"/servers/{server_id}/start/")

    def stop(self, server_id: str):
        return self._get(f"/servers/{server_id}/stop/")

    def status_label(self, status_code: int) -> str:
        return STATUS_LABELS.get(status_code, f"Unknown ({status_code})")
