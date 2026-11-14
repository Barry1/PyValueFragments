def print_time_result(wall: float, user: float, system: float) -> None:
    """Print Time Result."""
    load_percent = 0.0 if wall == 0 else 100 * (user + system) / wall
    print(
        f"{wall:8.3f} [s]",
        f"(User: {user:8.3f} [s]",
        f"System: {system:8.3f} [s])",
        f"{load_percent:6.2f}% Load" if wall != 0 else "   N/A Load",
        sep="\t",
    )
