#!/bin/bash
# Run by a restarting systemd unit: a kill resumes the build, a compile error stops it.
log="$HOME/Projects/.lightfox-full.log"
count_file="$HOME/Projects/.lightfox-build-attempts"
attempts=$(($(cat "$count_file" 2>/dev/null || echo 0) + 1))
echo "$attempts" > "$count_file"
echo "ATTEMPT $attempts $(date)" >> "$log"
if [ "$attempts" -gt 7 ]; then
  echo "FULL_BUILD_EXIT gave-up" >> "$log"
  exit 0
fi
./mach build >> "$log" 2>&1
echo "FULL_BUILD_EXIT $?" >> "$log"
exit 0
