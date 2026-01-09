#!/usr/bin/env python3
from datetime import datetime
from zoneinfo import ZoneInfo

now = datetime.now(ZoneInfo("America/Los_Angeles"))
print(now.strftime("%m/%d/%Y %I:%M %p %Z"))
