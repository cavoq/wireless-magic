import subprocess

class NetworkManager:
    
    @staticmethod
    def set_state(state: int) -> bool:
        cmd = "sudo systemctl start NetworkManager"
        if state not in [0, 1]:
            return False
        if state == 0:
            cmd = "sudo systemctl stop NetworkManager"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            return False
        return True

    @staticmethod
    def get_state() -> int:
        cmd = "sudo systemctl status NetworkManager"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if "active (running)" in result.stdout:
            return 1
        return 0
