"""
Build Wheel

Demonstrates building a Python wheel from the current package directory using
Blazing's built-in wheel_builder utility.  The resulting wheel can be uploaded
to the control plane for distribution to executor workers.

Patterns shown:
  1. build_wheel(str(package_path)) to compile a distributable Python wheel
  2. wheel_info.filename to inspect the generated wheel artifact name
  3. Synchronous (non-async) entry point suitable for CI/CD packaging scripts
"""
from pathlib import Path
from blazing.wheel_builder import build_wheel


def main():
    package_path = Path('.')
    wheel_info = build_wheel(str(package_path))
    print({'wheel': wheel_info.filename})


if __name__ == '__main__':
    main()
