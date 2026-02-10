"""BadUSB detection"""
import subprocess, os, json

class USBDetector:
    SUSPICIOUS_VID_PID = [
        ("05ac", "0256"),  # Counterfeit Apple
        ("2341", "8037"),  # Arduino (potential BadUSB)
    ]
    
    def list_usb_devices(self):
        devices = []
        try:
            result = subprocess.check_output(["lsusb"], text=True)
            for line in result.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 6:
                    vid_pid = parts[5].split(":")
                    devices.append({"bus": parts[1], "device": parts[3].rstrip(":"),
                                    "vid": vid_pid[0], "pid": vid_pid[1], "name": " ".join(parts[6:])})
        except: pass
        return devices
    
    def check_suspicious(self):
        devices = self.list_usb_devices()
        suspicious = []
        for d in devices:
            if (d["vid"], d["pid"]) in self.SUSPICIOUS_VID_PID:
                suspicious.append({**d, "reason": "Known BadUSB VID:PID"})
            if any(k in d.get("name","").lower() for k in ["hid", "keyboard", "rubber"]):
                if "mouse" not in d.get("name","").lower():
                    suspicious.append({**d, "reason": "HID device"})
        return suspicious
