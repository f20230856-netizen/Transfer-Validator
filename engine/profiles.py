# engine/profiles.py

CLUB_STYLE = {
    "barcelona": {
        "required_role": "Winger",
        "key_metrics": ["Progressive Carries", "Successful Take-ons"],
        "min_percentile": 80
    },
    "real madrid": {
        "required_role": "Winger",
        "key_metrics": ["npxG", "Successful Take-ons"],
        "min_percentile": 85
    },
    "manchester city": {
        "required_role": "Midfielder",
        "key_metrics": ["Pass Completion", "Progressive Carries"],
        "min_percentile": 85
    },
    "arsenal": {
        "required_role": "Midfielder",
        "key_metrics": ["Passes into Penalty Area", "Pressures Att 3rd"],
        "min_percentile": 80
    },
    "liverpool": {
        "required_role": "Winger",
        "key_metrics": ["Pressures Att 3rd", "npxG"],
        "min_percentile": 80
    }
}