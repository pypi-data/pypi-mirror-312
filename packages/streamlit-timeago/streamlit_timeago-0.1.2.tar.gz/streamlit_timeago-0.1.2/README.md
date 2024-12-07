# Streamlit Time Ago

Streamlit wrapper of `timeago-react`: https://www.npmjs.com/package/timeago-react

Examples:

```
just now
12 seconds ago
2 hours ago
3 days ago
3 weeks ago
2 years ago

in 12 seconds
in 3 minutes
in 24 days
in 6 months
```

## Installation instructions

```sh
pip install streamlit-timeago
```

## Usage instructions

```python
from streamlit_timeago import time_ago
from datetime import datetime

time_ago(datetime.now())
```
