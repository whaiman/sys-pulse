# SysPulse

SysPulse is a console-based system monitoring application built with Python and the Textual library. It provides a user-friendly interface to track processes, CPU usage, memory, and other system metrics in real time.

## Features

- **Real-Time Process Monitoring**: Displays a list of processes with PID, name, CPU usage, and memory consumption.
- **System Information**: Detailed insights into the operating system, kernel, architecture, uptime, CPU, and memory.
- **Dynamic Updates**: Refreshes data every second, including an ASCII-art styled clock.
- **Customizable Interface**: Styled TUI (Textual User Interface) with a dark theme and highlighted active processes.
- **CPU Usage Smoothing**: Uses exponential smoothing for stable CPU usage display.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/whaiman/sys-pulse.git
   cd sys-pulse
   ```

2. **Install Python**:
   Ensure Python 3.8 or higher is installed on your system.

3. **Install Dependencies**:
   Run the following command to install required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   python index.py
   ```

## Usage

Upon launching, the application displays two main sections:

- **Left Column**: Shows the current time in ASCII-art style and system information (OS, kernel, architecture, uptime, CPU, memory).
- **Right Column**: A process table with columns for PID, Process, CPU %, and RAM, updated in real time.

**Controls**:

- Use arrow keys to navigate the process table.
- Press `Ctrl+C` to exit the application.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch with your username as a prefix (e.g., `git checkout -b yourusername/your-feature`).
3. Make changes and commit (`git commit -m "Added new feature"`).
4. Push to your fork (`git push origin yourusername/your-feature`).
5. Create a Pull Request to the main repository.

Please adhere to PEP 8 coding standards and include tests for new features.

## Dependencies

- **Python 3.8+**
- **textual**: For the textual user interface.
- **psutil**: For retrieving system metrics and process information.
- **pyfiglet**: For rendering the ASCII-art clock.

Install dependencies using:

```bash
pip install textual psutil pyfiglet
```

## Notes

- **Limitations**: Some metrics (e.g., CPU frequency or temperatures) may not be available on certain systems via `psutil`.
- **Performance**: The application displays only the top 20 processes by CPU usage for systems with many processes.
- **Compatibility**: Tested on Linux, Windows, and macOS. Some features (e.g., process data access) may be restricted due to permissions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
