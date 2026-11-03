#!/usr/bin/env python3
"""Drop Glean metric and ping entries whose yaml file was deleted."""
import os
import re

path = "toolkit/components/glean/metrics_index.py"
out = []
for line in open(path):
    m = re.match(r'\s*"([\w./-]+\.yaml)",\s*$', line)
    if m and not os.path.exists(m.group(1)):
        print("dropped", m.group(1))
        continue
    out.append(line)
open(path, "w").writelines(out)
