import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
import subprocess
import shutil
import datetime

# ===================== METADATA =====================
APP_NAME = "WinForge EXE Compilation Suite"
APP_TAGLINE = "Controlled Windows Binary Generation Environment"
APP_VERSION = "1.4 - Dependency Aware Stable"

AUTHORIZED_NOTICE = "AUTHORIZED USE ONLY – INTERNAL COMPILATION ENVIRONMENT"

PYINSTALLER = "wine python -m PyInstaller"

BASE = Path.cwd()
WORKSPACE = BASE / "workspace"
INPUT = WORKSPACE / "input"
OUTPUT = WORKSPACE / "output"
LOGS = WORKSPACE / "logs"

for d in (INPUT, OUTPUT, LOGS):
    d.mkdir(parents=True, exist_ok=True)

# ===================== COMMON PROBLEMATIC LIBS =====================
COMMON_HIDDEN_IMPORTS = {
    "requests",
    "psutil",
    "cryptography",
    "PIL",
    "numpy",
    "pandas",
    "scapy",
}

# ===================== IMPORT DETECTION =====================
def detect_hidden_imports(py_file):
    detected = set()
    try:
        with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("import "):
                    detected.add(line.split()[1].split(".")[0])
                elif line.startswith("from "):
                    detected.add(line.split()[1].split(".")[0])
    except Exception:
        pass
    return detected

# ===================== APP =====================
class WinForgeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} | {APP_VERSION}")
        self.geometry("1080x720")
        self.resizable(False, False)

        self.source = None
        self.icon = None

        self.console = tk.BooleanVar(value=True)
        self.profile = tk.StringVar(value="Standard")
        self.exe_name = tk.StringVar()

        self._style()
        self._layout()

    # ===================== STYLE =====================
    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")

        s.configure(".", background="#0f172a", foreground="#e5e7eb", font=("Segoe UI", 10))
        s.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#38bdf8")
        s.configure("Sub.TLabel", foreground="#9ca3af")
        s.configure("Warn.TLabel", foreground="#fbbf24", font=("Segoe UI", 9, "bold"))
        s.configure("TLabelframe", background="#111827", foreground="#e5e7eb")
        s.configure("TLabelframe.Label",
                    background="#111827",
                    foreground="#38bdf8",
                    font=("Segoe UI", 10, "bold"))

    # ===================== UI =====================
    def _layout(self):
        root = ttk.Frame(self, padding=20)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root)
        header.pack(fill="x", pady=(0, 15))
        ttk.Label(header, text=APP_NAME, style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text=APP_TAGLINE, style="Sub.TLabel").pack(anchor="w")
        ttk.Label(header, text=AUTHORIZED_NOTICE, style="Warn.TLabel").pack(anchor="e")

        # SOURCE
        src = ttk.LabelFrame(root, text="Source Tool Ingestion", padding=15)
        src.pack(fill="x", pady=8)
        ttk.Button(src, text="Load Python Source (.py)", command=self.load_source).pack(side="left")
        self.src_label = ttk.Label(src, text="No source loaded")
        self.src_label.pack(side="left", padx=15)

        # BUILD CONFIG
        cfg = ttk.LabelFrame(root, text="Build Configuration", padding=15)
        cfg.pack(fill="x", pady=8)

        ttk.Label(cfg, text="Executable Name:").grid(row=0, column=0, sticky="w")
        ttk.Entry(cfg, textvariable=self.exe_name, width=30).grid(row=0, column=1, padx=10)

        ttk.Button(cfg, text="Select Icon (.ico)", command=self.load_icon).grid(row=0, column=2, padx=10)
        self.icon_label = ttk.Label(cfg, text="No icon")
        self.icon_label.grid(row=0, column=3, sticky="w")

        ttk.Label(cfg, text="Profile:").grid(row=1, column=0, sticky="w", pady=8)
        ttk.Combobox(
            cfg,
            textvariable=self.profile,
            values=["Standard", "Audit", "Hardened"],
            state="readonly",
            width=15
        ).grid(row=1, column=1, sticky="w")

        ttk.Checkbutton(cfg, text="Enable console output", variable=self.console)\
            .grid(row=1, column=2, sticky="w")

        # ACTIONS
        act = ttk.Frame(root)
        act.pack(fill="x", pady=12)
        ttk.Button(act, text="Execute Controlled Compilation", command=self.compile).pack(side="left")
        ttk.Button(act, text="Export Build Log", command=self.export_log).pack(side="left", padx=10)

        # LOGS
        log = ttk.LabelFrame(root, text="Compilation Audit Log", padding=15)
        log.pack(fill="both", expand=True)

        self.logbox = ScrolledText(
            log,
            bg="#020617",
            fg="#22c55e",
            insertbackground="white",
            font=("Consolas", 10)
        )
        self.logbox.pack(fill="both", expand=True)

    # ===================== LOG =====================
    def log(self, msg):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.logbox.insert("end", f"[{ts}] {msg}\n")
        self.logbox.see("end")

    # ===================== LOADERS =====================
    def load_source(self):
        f = filedialog.askopenfilename(filetypes=[("Python Source", "*.py")])
        if not f:
            return
        src = Path(f)
        dst = INPUT / src.name
        shutil.copy(src, dst)
        self.source = dst
        self.exe_name.set(src.stem)
        self.src_label.config(text=src.name)
        self.log(f"INGEST | Source accepted: {src.name}")

    def load_icon(self):
        f = filedialog.askopenfilename(filetypes=[("Icon", "*.ico")])
        if not f:
            return
        self.icon = Path(f)
        self.icon_label.config(text=self.icon.name)
        self.log(f"CONFIG | Icon selected: {self.icon.name}")

    # ===================== BUILD =====================
    def compile(self):
        if not self.source:
            messagebox.showerror("Policy Violation", "No source loaded")
            return

        name = self.exe_name.get().strip()
        if not name:
            messagebox.showerror("Invalid Configuration", "Executable name required")
            return

        self.log(f"PROCESS | Compilation started ({self.profile.get()})")

        # Cleanup
        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree("dist", ignore_errors=True)
        self.log("CLEANUP | Previous build artifacts removed")

        # Detect imports
        detected = detect_hidden_imports(self.source)
        hidden_flags = ""

        for mod in detected:
            if mod in COMMON_HIDDEN_IMPORTS:
                hidden_flags += f" --collect-all {mod}"
                self.log(f"AUTO-IMPORT | Collected dependency: {mod}")

        mode = "--console" if self.console.get() else "--windowed"
        icon_arg = f'--icon "{self.icon}"' if self.icon else ""
        version = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        cmd = (
            f'{PYINSTALLER} --onefile {mode} {icon_arg} '
            f'{hidden_flags} '
            f'--name "{name}" "{self.source}"'
        )

        self.log(f"COMMAND | {cmd}")

        try:
            subprocess.run(cmd, shell=True, check=True)
            exe = Path("dist") / f"{name}.exe"

            if exe.exists():
                final = OUTPUT / f"{name}_v{version}.exe"
                shutil.move(exe, final)
                self.log(f"SUCCESS | Binary generated: {final}")
                messagebox.showinfo("Build Complete", f"EXE ready:\n{final}")
            else:
                self.log("ERROR | EXE not found post-compilation")

        except subprocess.CalledProcessError as e:
            self.log(f"FAILURE | Compilation error: {e}")

    # ===================== EXPORT =====================
    def export_log(self):
        data = self.logbox.get("1.0", "end").strip()
        if not data:
            return
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file = LOGS / f"build_log_{ts}.txt"
        file.write_text(data)
        messagebox.showinfo("Log Exported", f"Log saved:\n{file}")

# ===================== RUN =====================
if __name__ == "__main__":
    WinForgeApp().mainloop()
