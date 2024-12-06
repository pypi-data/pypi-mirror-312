def update_batting_stats(player, runs, balls, is_out, is_four, is_six):
    """Update batting stats for a player."""
    player['runs'] += runs
    player['balls'] += balls
    player['fours'] += int(is_four)
    player['sixes'] += int(is_six)
    player['is_out'] = is_out
    return player