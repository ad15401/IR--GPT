import re
from collections import Counter

def summarize_logs(log_text: str) -> str:
    """Simplify raw log text into a short incident summary."""
    ips = re.findall(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', log_text)
    users = re.findall(r'user[=:]\s*([A-Za-z0-9_.-]+)', log_text, re.I)
    events = re.findall(r'(failed|success|error|denied|approved|created|deleted)', log_text, re.I)
    times = re.findall(r'\b\d{2}:\d{2}:\d{2}\b', log_text)

    ip_counts = Counter(ips)
    user_counts = Counter(users)
    event_counts = Counter([e.lower() for e in events])

    summary = []
    if ip_counts:
        top_ip, count = ip_counts.most_common(1)[0]
        summary.append(f"{count} events from IP {top_ip}")
    if user_counts:
        top_user, count = user_counts.most_common(1)[0]
        summary.append(f"user {top_user} appears {count} times")
    if event_counts:
        top_event, count = event_counts.most_common(1)[0]
        summary.append(f"{count} '{top_event}' events detected")
    if times:
        summary.append(f"latest timestamp {max(times)}")

    if not summary:
        return "No clear pattern — review raw logs manually."

    return "; ".join(summary) + "."

