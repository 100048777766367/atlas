class SmartFleetRadar:
    # 1. DANH SÁCH DÒNG HỌ ĐƯỢC PHÉP QUÉT (WHITE-LIST PREFIXES)
    ECOSYSTEM_CLANS = [
        "contract", "atlas", "nexus", "cortex", "neuron",
        "vault", "refinery", "forge", "distill", "golem", "oracle",
        "retina", "cochlea", "tactile", "olfactory", "motor", "seed", "monad", "shunya"
    ]

    @classmethod
    def is_ecosystem_repo(cls, repo_name):
        """LỌC BỎ RÁC: Chỉ quét nếu tên repo thuộc dòng họ Bodhi-Mesh"""
        clean_name = repo_name.lower().replace("-", "_")
        for clan in cls.ECOSYSTEM_CLANS:
            if clean_name.startswith(clan) or clan in clean_name:
                return True
        return False

    @classmethod
    def scan_targeted_fleet(cls, owner="100048777766367"):
        """CHỈ QUÉT NHỮNG GÌ CẦN THIẾT - BỎ QUA MỌI REPO KHÔNG LIÊN QUAN"""
        url = f"https://api.github.com/users/{owner}/repos?per_page=100"
        fleet = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Atlas-Smart-Radar"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                repos = json.loads(resp.read().decode('utf-8'))
                for r in repos:
                    # BƯỚC CHẶN 1: Bỏ qua repo archived hoặc không thuộc hệ sinh thái
                    if r.get("archived", False) or not cls.is_ecosystem_repo(r["name"]):
                        continue  # BỎ QUA NGAY LẬP TỨC!
                    
                    fleet.append({
                        "name": r["name"],
                        "branch": r.get("default_branch", "main"),
                        "updated": r.get("updated_at", "N/A"),
                        "forks": r.get("forks_count", 0)
                    })
        except Exception: pass
        return fleet
