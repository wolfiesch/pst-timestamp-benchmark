#!/bin/bash
# Outputs current Pacific time in MM/DD/YYYY HH:MM AM/PM format
# Automatically handles PST/PDT transitions

TZ='America/Los_Angeles' date '+%m/%d/%Y %I:%M %p %Z'
