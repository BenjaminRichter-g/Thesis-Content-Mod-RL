from mastodon import Mastodon
import json

mastodon = Mastodon(api_base_url='https://mastodon.social')

# Get 100 most recent public posts
toots = mastodon.timeline_public(limit=100)

with open("public_timeline.jsonl", "w") as f:
    for toot in toots:
        f.write(json.dumps(toot) + "\n")
