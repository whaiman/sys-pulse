import platform
import time
from datetime import datetime

import psutil
from pyfiglet import Figlet
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Static

f = Figlet(font="basic")


def get_size(bytes, suffix="B"):
    """Convert bytes to human-readable format."""
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= 1024


def get_system_info():
    """Retrieve system information."""
    try:
        uname = platform.uname()
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        svmem = psutil.virtual_memory()
        cpu_freq = psutil.cpu_freq()

        uptime = datetime.now() - boot_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"

        info = [
            f"OS: {uname.system} {uname.release}",
            f"Kernel: {uname.version}",
            f"Arch: {platform.machine()}",
            f"Host: {uname.node}",
            f"Uptime: {uptime_str}",
            f"CPU: {uname.processor} ({psutil.cpu_count(logical=False)}c/{psutil.cpu_count(logical=True)}t)",
        ]
        if cpu_freq:
            info.append(f"CPU Freq: {cpu_freq.current:.2f} MHz")
        info.append(f"RAM: {get_size(svmem.used)} / {get_size(svmem.total)}")
        info.append(f"Python: {platform.python_version()}")
        return "\n".join(info)
    except Exception as e:
        return f"Error retrieving system info: {e}"


class SystemMonitor(App):
    CSS_PATH = "design.tcss"

    def compose(self) -> ComposeResult:
        self.time_widget = Static(
            f.renderText(datetime.now().strftime("%H:%M:%S")), id="time"
        )
        self.info_widget = Static(get_system_info(), classes="info-panel")
        self.task_table = DataTable(id="task-table")
        self.task_table.add_columns("PID", "Process", "CPU %", "RAM")
        self.task_table.zebra_stripes = True
        self.task_table.cursor_type = "row"

        yield Horizontal(
            Vertical(
                self.time_widget,
                self.info_widget,
                classes="column left-column",
            ),
            Vertical(
                self.task_table,
                classes="column right-column",
            ),
            classes="container",
        )

    def on_mount(self) -> None:
        self._last_proc_cpu = {}
        self._last_ts = time.time()
        self._cpu_smoothing = {}
        self.set_interval(1.0, self.update)
        self.update_task_list()

    def update(self) -> None:
        self.time_widget.update(f.renderText(datetime.now().strftime("%H:%M:%S")))
        self.info_widget.update(get_system_info())
        self.update_task_list()

    def update_task_list(self) -> None:
        self.task_table.clear()
        try:
            now = time.time()
            dt = max(now - self._last_ts, 1e-6)
            self._last_ts = now
            cpu_count = psutil.cpu_count(logical=True) or 1

            rows = []
            new_proc_cpu = {}

            for proc in psutil.process_iter(
                ["pid", "name", "memory_info", "cpu_times"]
            ):
                try:
                    pid = proc.info["pid"]
                    if pid == 0:  # пропускаем System Idle
                        continue

                    t = proc.info["cpu_times"]
                    total = float(t.user + t.system)
                    new_proc_cpu[pid] = total

                    prev_total = self._last_proc_cpu.get(pid)
                    if prev_total is None:
                        cpu = 0.0  # новый процесс, CPU пока 0
                    else:
                        cpu = (total - prev_total) / dt * 100.0 / cpu_count
                        cpu = min(max(cpu, 0.0), 100.0)

                    # экспоненциальное сглаживание
                    self._cpu_smoothing[pid] = (
                        self._cpu_smoothing.get(pid, cpu) * 0.7 + cpu * 0.3
                    )
                    cpu = self._cpu_smoothing[pid]

                    name = (proc.info["name"] or "")[:12]
                    mem = proc.info.get("memory_info")
                    ram = get_size(mem.rss) if mem else "0B"

                    rows.append((pid, name, cpu, mem.rss if mem else 0, ram))

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    continue

            self._last_proc_cpu = new_proc_cpu

            # сортируем по CPU по убыванию
            rows.sort(key=lambda x: x[2], reverse=True)

            for pid, name, cpu, _, ram in rows[:20]:
                self.task_table.add_row(str(pid), name, f"{cpu:.2f}", ram)

        except Exception as e:
            self.task_table.add_row("-", "Error", f"{e}", "-")


if __name__ == "__main__":
    SystemMonitor().run()
