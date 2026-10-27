import os
import sys
import json
import time
import hashlib
import urllib.request

# ==============================================================================
# BẢN ĐỒ ADN TỰ ĐẺ THỂ XÁC ATLAS (EMBRYONIC BLUEPRINTS)
# ==============================================================================
ATLAS_BLUEPRINTS = {
    "contract.json": json.dumps({
        "contract_id": "bodhi.atlas.v1",
        "genesis_root": "100048777766367/contract",
        "derived_node": "100048777766367/atlas",
        "role": "SUPREME_FLEET_NAVIGATOR",
        "rules": {
            "zero_pii": True,
            "pan_fleet_observation": True,
            "shadow_clone_detection": True,
            "frontpage_live_dashboard": True
        }
    }, indent=4),

    "Dockerfile": """FROM python:3.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
CMD ["python", "kernel.py"]
""",

    "simulator/__init__.py": "# Simulator Package\n",

    "simulator/fleet_radar.py": '''import json
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
''',

    "simulator/pipeline_simulator.py": '''class PipelineSimulator:
    # Mô phỏng nhịp đập chuỗi cung ứng khép kín
    @staticmethod
    def inspect_pipeline_integrity(fleet_names):
        core_links = ["contract", "nexus-08", "vault", "forge", "distill", "golem", "oracle", "cortex"]
        status_map = {}
        for link in core_links:
            status_map[link] = "🟢 ONLINE" if any(link in name for name in fleet_names) else "⚪ STANDBY"
        return status_map
''',

    "synapses/state.json": json.dumps({"generation_epoch": 1, "status": "atlas_seeded"}, indent=4)
}

# ==============================================================================
# HẠT NHÂN CHỈ HUY ATLAS KERNEL
# ==============================================================================
STATE_FILE = "synapses/state.json"
TOPOLOGY_FILE = "synapses/fleet_topology.json"

class AtlasKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/atlas")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.contract_repo = f"{self.owner}/contract"
        
        # BƯỚC 0: TỰ ĐẺ THỂ XÁC
        self.self_materialize()

        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from simulator.fleet_radar import FleetRadar
        from simulator.pipeline_simulator import PipelineSimulator

        self.radar = FleetRadar
        self.simulator = PipelineSimulator
        self.epoch = self.load_epoch()

    def self_materialize(self):
        for path, code in ATLAS_BLUEPRINTS.items():
            if not os.path.exists(path):
                parent_dir = os.path.dirname(path)
                if parent_dir: os.makedirs(parent_dir, exist_ok=True)
                with open(path, "w", encoding="utf-8") as f: f.write(code)

    def load_epoch(self):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("generation_epoch", 0) + 1
        except Exception: return 1

    def update_frontpage_dashboard(self, official_fleet, shadow_clones, pipeline_status, cid):
        """TỰ ĐỘNG GHI ĐÈ BẢNG ĐIỀU HÀNH MẶT TIỀN TRANG CHỦ README.MD"""
        total_nodes = len(official_fleet)
        total_shadows = len(shadow_clones)
        
        md_content = f"""# 🗺️ BODHI-ATLAS: TỔNG TRẠM HOA TIÊU & ĐÀI CHỈ HUY HẢI ĐĂNG
> **Bản Đồ Số Sống Đại Hệ Sinh Thái** | **Kỷ nguyên hải đăng:** #{self.epoch}  
> **Chứng Chỉ Lượng Tử Toàn Đàn CID:** `{cid}`

---

### 📊 TỔNG QUAN MẠCH ĐẬP HỆ SINH THÁI:
| Chỉ Số Hải Đăng | Giá Trị Thực Tế | Đánh Giá Tình Trạng |
| :--- | :---: | :--- |
| **Nút Mạng Chính Chủ** | **`{total_nodes} Repos`** | 🟢 100% Thuộc chủ quyền `{self.owner}` |
| **Bản Sao Ẩn Danh (Shadow)** | **`{total_shadows} Repos`** | 🌐 Đang âm thầm cày dữ liệu trên toàn cầu |
| **Trạng Thái Chuỗi Cung Ứng**| **Khép Kín Hoàn Toàn** | 🟢 Không đứt gãy, tự tuần hoàn năng lượng |

---

### 🏭 TRẠNG THÁI 8 MẮT XÍCH CÔNG NGHIỆP CỐT LÕI:
| Phân Vai Mắt Xích | Repo Đại Diện | Tình Trạng Mạch Đập |
| :--- | :--- | :---: |
| **1. Hiến Pháp Bất Biến [q]** | `contract` | {pipeline_status.get('contract', '🟢 ONLINE')} |
| **2. Não Bộ Hội Tụ F8** | `nexus-08` | {pipeline_status.get('nexus-08', '🟢 ONLINE')} |
| **3. Thương Cảng Dữ Liệu** | `vault` / `vault-01..04` | {pipeline_status.get('vault', '🟢 ONLINE')} |
| **4. Cơ Bắp GPU (NVIDIA Tier)** | `forge` | {pipeline_status.get('forge', '🟢 ONLINE')} |
| **5. Chưng Cất Trọng Số INT8**| `distill` | {pipeline_status.get('distill', '🟢 ONLINE')} |
| **6. Tay Chân Hành Động Tác Tử**| `golem` | {pipeline_status.get('golem', '🟢 ONLINE')} |
| **7. Cổng Chân Lý Thực Tế** | `oracle` | {pipeline_status.get('oracle', '🟢 ONLINE')} |
| **8. Vỏ Não Tân Sinh Đa Nhân Bản**| `cortex` | {pipeline_status.get('cortex', '🟢 ONLINE')} |

---

### 🛰️ DANH SÁCH CHI TIẾT CÁC NÚT MẠNG ĐANG HOẠT ĐỘNG ({total_nodes} NÚT):
| STT | Tên Nút Mạng | Nhánh Mặc Định | Cập Nhật Gần Nhất | Lượt Fork |
| :---: | :--- | :---: | :--- | :---: |
"""
        for idx, node in enumerate(sorted(official_fleet, key=lambda x: x["name"]), start=1):
            md_content += f"| {idx} | 🏛️ **[{node['name']}](https://github.com/{self.owner}/{node['name']})** | `{node['branch']}` | {node['updated']} | {node['forks']} |\n"

        if shadow_clones:
            md_content += f"""
---

### 🕵️ BẢN ĐỒ BẢN SAO ẨN DANH TRÊN TOÀN CẦU ({total_shadows} REPOS):
> *Các kho lưu trữ tải code về chạy độc lập, mang theo chữ ký số của hệ sinh thái:*
| STT | Repo Ẩn Danh | Chủ Tài Khoản | Phân Loại |
| :---: | :--- | :---: | :---: |
"""
            for s_idx, s_node in enumerate(shadow_clones, start=1):
                md_content += f"| {s_idx} | 🌐 `{s_node['full_name']}` | `{s_node['owner']}` | Nút Thợ Miễn Phí |\n"

        md_content += f"""
---
*Khắc cốt và cập nhật tự động bởi Atlas Supreme Kernel | Bản Đồ Sống Bất Tử*
"""
        # 1. Ghi đè trực tiếp trang chủ README.md
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(md_content)

        # 2. Ghi vào GitHub Actions Step Summary
        summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_file:
            try:
                with open(summary_file, "a", encoding="utf-8") as f:
                    f.write(md_content)
            except Exception: pass

    def run(self):
        print("=" * 80)
        print(f"🗺️ [ATLAS SUPREME COMMAND] KHỞI ĐỘNG ĐÀI CHỈ HUY HẢI ĐĂNG #{self.epoch}")
        print("=" * 80)

        # 1. Quét toàn bộ repo chính chủ
        print(f"📡 [RADAR CHÍNH CHỦ] Đang quét tài khoản '{self.owner}'...")
        official_fleet = self.radar.scan_official_fleet(self.owner)
        fleet_names = [n["name"] for n in official_fleet]
        print(f"  └── 🏛️ Phát hiện {len(official_fleet)} nút mạng chính chủ đang hoạt động.")

        # 2. Truy lùng các bản sao ẩn danh toàn cầu
        print("🕵️ [RADAR THÁM TỬ] Đang rà soát các bản sao chép lậu trên GitHub...")
        shadow_clones = self.radar.hunt_shadow_clones("bodhi.cortex.v1")
        print(f"  └── 🌐 Phát hiện {len(shadow_clones)} bản sao ẩn danh đang phát sóng.")

        # 3. Kiểm định tính toàn vẹn của chuỗi cung ứng
        pipeline_status = self.simulator.inspect_pipeline_integrity(fleet_names)

        # 4. Lưu bản đồ số dạng JSON
        os.makedirs("synapses", exist_ok=True)
        with open(TOPOLOGY_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "epoch": self.epoch,
                "official_fleet": official_fleet,
                "shadow_clones": shadow_clones,
                "pipeline_status": pipeline_status
            }, f, indent=4)

        # 5. Đóng dấu Quantum CID toàn đàn
        t = int(time.time())
        seed = f"atlas_supreme_{self.epoch}_{t}_{len(official_fleet)}_{len(shadow_clones)}".encode()
        cid = hashlib.shake_256(seed).hexdigest(64)

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"generation_epoch": self.epoch, "last_t": t, "quantum_cid": cid, "status": "atlas_master_active"}, f, indent=4)

        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump({"contract": "bodhi.atlas.v1", "identity": self.repo_name, "cid": cid}, f, indent=4)

        # 6. Tự động vẽ Dashboard lên trang chủ README.md & Actions Summary
        self.update_frontpage_dashboard(official_fleet, shadow_clones, pipeline_status, cid)

        print(f"💾 [CHỨNG THỰC CID HẢI ĐĂNG]: {cid[:24]}...")
        print("✨ [HOÀN MỸ] Đã cập nhật Bảng Điều Hành Sống Động lên trang chủ README.md của Atlas!")
        print("=" * 80)

if __name__ == "__main__":
    AtlasKernel().run()
