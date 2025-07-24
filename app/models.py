import threading
import time

# In-memory storage for short code -> data
url_store = {}
# Structure: {
#   short_code: {
#       'url': original_url,
#       'clicks': int,
#       'created_at': timestamp
#   },
#   ...
# }

# Lock for thread safety
store_lock = threading.Lock()