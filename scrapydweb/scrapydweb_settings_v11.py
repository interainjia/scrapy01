import os

# Node(s) to monitor/manage. Format: 'ip:port' (one entry per scrapyd instance).
# For multiple nodes, add more entries here, e.g. ['scrapyd1:6800', 'scrapyd2:6800'].
SCRAPYD_SERVERS = [
    os.environ.get("SCRAPYD_SERVER", "scrapyd:6800"),
]

# Basic auth for the scrapydweb UI itself (recommended when exposed beyond localhost).
ENABLE_AUTH = os.environ.get("SCRAPYDWEB_ENABLE_AUTH", "false").lower() == "true"
USERNAME = os.environ.get("SCRAPYDWEB_USERNAME", "admin")
PASSWORD = os.environ.get("SCRAPYDWEB_PASSWORD", "admin")
