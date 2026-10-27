import json
import urllib.request

class FleetRadar:
    # RADAR HOA TIÊU KÉP: Quét chính chủ 100048777766367 + Truy lùng Shadow Clones
    @staticmethod
    def scan_official_fleet(owner="100048777766367"):
        url = f"https://api.github.com/users/{owner}/repos?per_page=100"
        radar_report = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Atlas-Fleet-Scanner"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    repos = json.loads(resp.read().decode("utf-8"))
                    for r in repos:
                        radar_report.append({
                            "name": r.get("name"),
                            "branch": r.get("default_branch", "main"),
                            "updated": r.get("updated_at", "N/A"),
                            "stars": r.get("stargazers_count", 0),
                            "forks": r.get("forks_count", 0)
                        })
        except Exception as e:
            print(f"⚠️ Cảnh báo radar chính chủ: {e}")
        return radar_report

    @staticmethod
    def hunt_shadow_clones(signature="bodhi.cortex.v1"):
        # Tìm kiếm các bản copy ẩn danh trên toàn cầu qua Code Search
        search_url = f"https://api.github.com/search/code?q={signature}"
        shadow_clones = []
        try:
            req = urllib.request.Request(search_url, headers={"User-Agent": "Atlas-Shadow-Hunter"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    for item in data.get("items", []):
                        repo_info = item.get("repository", {})
                        full_name = repo_info.get("full_name", "")
                        if not full_name.startswith("100048777766367/"):
                            shadow_clones.append({
                                "full_name": full_name,
                                "owner": repo_info.get("owner", {}).get("login", "Unknown")
                            })
        except Exception:
            pass
        return shadow_clones
