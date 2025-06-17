import re
from bs4 import BeautifulSoup
import emoji

class PreProcessor:
    def __init__(self):
        self.url_reg               = re.compile(r'https?://\s*[^\s<>"\'`]+')
        self.mention_reg           = re.compile(r'@\s*[\w\.-]+@[\w\.-]+')
        self.hashtag_reg           = re.compile(r'#\s*[\w-]+')
        # colon-based placeholders: e.g. :smile:
        self.emoji_placeholder_reg = re.compile(r':[^\s:]+:')

    def demojize_text(self, text):
        # turn all Unicode emojis into :short_name: placeholders
        return emoji.demojize(text, language='en')

    def preprocess(self, html_content):
        if not html_content:
            return {}

        # 1) HTML → text + links
        soup = BeautifulSoup(html_content, 'lxml')
        links_in_html = [a['href'] for a in soup.find_all('a', href=True)]
        raw_text = soup.get_text(separator=' ')

        # 2) In-place demojize
        demojized = self.demojize_text(raw_text)

        # 3) Extract entities
        mentions     = [m.strip() for m in self.mention_reg.findall(demojized)]
        hashtags     = [h.strip() for h in self.hashtag_reg.findall(demojized)]
        links        = list({*links_in_html, *self.url_reg.findall(demojized)})
        emojis       = self.emoji_placeholder_reg.findall(demojized)
        emoji_names  = [e.strip(':').replace('_', ' ') for e in emojis]

        # 4) Remove only URLs and mentions (keep hashtags and emoji placeholders)
        remove_pat = re.compile(
            f"({self.url_reg.pattern})|"
            f"({self.mention_reg.pattern})"
        )
        intermediate = remove_pat.sub('', demojized)

        # 5) Collapse whitespace
        clean_text = re.sub(r'\s+', ' ', intermediate).strip()

        return {
            "clean_text": clean_text,
            "mentions": mentions,
            "hashtags": hashtags,
            "links": sorted(links),
            "emojis": emojis,
            "emoji_names": emoji_names
        }    
