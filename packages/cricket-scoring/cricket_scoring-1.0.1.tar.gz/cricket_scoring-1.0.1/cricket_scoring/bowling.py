def update_bowling_stats(bowler, runs, balls, is_wicket):
    """Update bowling stats for a bowler."""
    bowler['runs_conceded'] += runs
    bowler['balls_bowled'] += balls
    bowler['wickets'] += int(is_wicket)
    bowler['overs'] = bowler['balls_bowled'] // 6 + (bowler['balls_bowled'] % 6) / 10
    return bowler
