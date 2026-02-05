from pathlib import Path
from blazing.wheel_builder import build_wheel


def main():
    package_path = Path('.')
    wheel_info = build_wheel(str(package_path))
    print({'wheel': wheel_info.filename})


if __name__ == '__main__':
    main()
