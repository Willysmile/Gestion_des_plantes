#!/usr/bin/env python3
"""
LIVE UI TEST - Phase 4B Frontend Windows
Launches windows with timeout to detect startup errors
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path("/home/willysmile/Documents/Gestion_des_plantes")
VENV_PYTHON = PROJECT_ROOT / "backend/venv/bin/python"

print("\n" + "="*70)
print("  🎯 LIVE UI WINDOW TESTS - Phase 4B")
print("="*70 + "\n")

# Test 1: SettingsWindow startup
print("TEST 1: SettingsWindow Launch Detection")
print("-" * 70)

code1 = """
import sys
sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/frontend')
from app.windows.settings_window import SettingsWindow
print("OK - SettingsWindow created")
try:
    window = SettingsWindow()
    print("OK - SettingsWindow instance")
except Exception as e:
    print(f"ERROR - SettingsWindow: {e}")
    sys.exit(1)
"""

result = subprocess.run(
    [str(VENV_PYTHON), "-c", code1],
    capture_output=True,
    text=True,
    timeout=5
)

if result.returncode == 0:
    print("PASS - SettingsWindow")
    for line in result.stdout.split('\n'):
        if line.strip():
            print(f"  {line}")
else:
    print("FAIL - SettingsWindow")
    print(result.stderr)

# Test 2: DashboardWindow startup
print("\nTEST 2: DashboardWindow Launch Detection")
print("-" * 70)

code2 = """
import sys
sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/frontend')
from app.windows.dashboard_window import DashboardWindow
print("OK - DashboardWindow created")
try:
    window = DashboardWindow()
    print("OK - DashboardWindow instance")
except Exception as e:
    print(f"ERROR - DashboardWindow: {e}")
    sys.exit(1)
"""

result = subprocess.run(
    [str(VENV_PYTHON), "-c", code2],
    capture_output=True,
    text=True,
    timeout=5
)

if result.returncode == 0:
    print("PASS - DashboardWindow")
    for line in result.stdout.split('\n'):
        if line.strip():
            print(f"  {line}")
else:
    print("FAIL - DashboardWindow")
    print(result.stderr)

# Test 3: MainWindow startup
print("\nTEST 3: MainWindow Launch Detection")
print("-" * 70)

code3 = """
import sys
sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/frontend')
from app.main import MainWindow
print("OK - MainWindow created")
try:
    window = MainWindow()
    print("OK - MainWindow instance")
except Exception as e:
    print(f"ERROR - MainWindow: {e}")
    sys.exit(1)
"""

result = subprocess.run(
    [str(VENV_PYTHON), "-c", code3],
    capture_output=True,
    text=True,
    timeout=5
)

if result.returncode == 0:
    print("PASS - MainWindow")
    for line in result.stdout.split('\n'):
        if line.strip():
            print(f"  {line}")
else:
    print("FAIL - MainWindow")
    print(result.stderr)

print("\n" + "="*70)
print("  WINDOW STARTUP CHECK COMPLETE")
print("="*70 + "\n")
