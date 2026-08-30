from datetime import datetime


def relative_time(timestamp: str) -> str:
    try:
        created = datetime.strptime(
            timestamp,
            "%Y-%m-%d %H:%M:%S"
        )

        now = datetime.now()

        seconds = int(
            (now - created).total_seconds()
        )

        if seconds < 0:
            return "Just now"

        if seconds < 60:
            return "Just now"

        minutes = seconds // 60

        if minutes < 60:
            return (
                f"{minutes} minute ago"
                if minutes == 1
                else f"{minutes} minutes ago"
            )

        hours = minutes // 60

        if hours < 24:
            return (
                f"{hours} hour ago"
                if hours == 1
                else f"{hours} hours ago"
            )

        days = hours // 24

        if days == 1:
            return "Yesterday"

        if days < 7:
            return (
                f"{days} day ago"
                if days == 1
                else f"{days} days ago"
            )

        return created.strftime("%b %d")

    except (ValueError, TypeError):
        return timestamp