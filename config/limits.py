# config/limits.py

# Pacing between individual emails (seconds)
DELAY_MIN = 30
DELAY_MAX = 90

# Resilience
MAX_RETRIES = 3

# Daily Quota
DAILY_LIMIT = 50  # 

# Session Management
MAX_PER_SESSION = 50
SESSION_PAUSE_MIN = 60
SESSION_PAUSE_MAX = 180