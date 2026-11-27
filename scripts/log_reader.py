"""Physical LF-delimited lines, including empty lines and an unterminated final line."""
import json
from collections import Counter

def count_lines(stream):
    total = 0
    last = b""
    while block := stream.read(1 << 20):
        total += block.count(b"\n")
        last = block[-1:]
    return total + int(last not in (b"", b"\n"))

def log_path(label_path):
    if not label_path.startswith("labels/"):
        raise ValueError(label_path)
    return "gather/" + label_path[len("labels/"):]

def check_labels(stream, nlines):
    counts = Counter()
    types = Counter()
    seen = set()
    for raw in stream:
        counts["annotation_rows"] += 1
        try:
            row = json.loads(raw)
            n, labels = row["line"], row["labels"]
            if type(n) is not int or not isinstance(labels,list) or not labels or not all(isinstance(s,str) and s for s in labels):
                raise ValueError("invalid annotation")
        except (ValueError, KeyError, TypeError, UnicodeError):
            counts["malformed"] += 1
            continue
        if nlines is None:
            counts["unresolved_file"] += 1
        elif not 1 <= n <= nlines:
            counts["out_of_bounds"] += 1
        else:
            counts["matched"] += 1
            counts["repeated_ref"] += int(n in seen)
            counts["multilabel_rows"] += int(len(set(labels)) > 1)
            seen.add(n)
            types.update(labels)
    counts["unique_lines"] = len(seen)
    counts["assignments"] = sum(types.values())
    return counts, types
