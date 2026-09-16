from pathlib import Path

API_BASE = "https://2ch.su"
DEFAULT_TIMEOUT = 30.0
USER_AGENT = "api2ch/2.0.0 (+https://github.com/uburuntu/api2ch)"

# Compatibility conveniences. Validation no longer relies on frozen board or
# mirror lists.
api_mirrors = ("https://2ch.su", "https://2ch.hk", "https://beta.2ch.hk")
hostname_mirrors = tuple(origin.removeprefix("https://") for origin in api_mirrors)
downloads_dir = Path("downloads_2ch")
