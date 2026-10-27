class PipelineSimulator:
    # Mô phỏng nhịp đập chuỗi cung ứng khép kín
    @staticmethod
    def inspect_pipeline_integrity(fleet_names):
        core_links = ["contract", "nexus-08", "vault", "forge", "distill", "golem", "oracle", "cortex"]
        status_map = {}
        for link in core_links:
            status_map[link] = "🟢 ONLINE" if any(link in name for name in fleet_names) else "⚪ STANDBY"
        return status_map
