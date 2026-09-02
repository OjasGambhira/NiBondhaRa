import feedparser
from groq import Groq
from email_sender import send_email
from config import GROQ_API_KEY

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Stronger RSS feeds (more tech + AI content)
RSS_FEEDS = [
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://www.reuters.com/technology/rss",
    "https://news.ycombinator.com/rss",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.cnet.com/rss/news/",
]

def fetch_all_news():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:20]:  # increased to 20 per feed
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            if title and link:
                articles.append({"title": title, "summary": summary, "link": link})
    return articles

def build_llm_prompt(articles):
    text = """
You are an AI news analyst.

From the following articles:
- Identify ANY content related to AI, ML, LLMs, automation, robotics, chips, GPUs, cloud, data centers, or tech innovation.
- Even if the article is indirectly related, include it.
- If relevance is unclear, include it anyway.
- Output AT LEAST 5 items.
- Summarize concisely.
- Return ONLY <li> items in this format:

<li class="news-item">
    <strong>Title</strong>
    <p>Short summary</p>
    <a href="link">Read more</a>
</li>

Articles:
"""

    for i, a in enumerate(articles, start=1):
        text += f"{i}. Title: {a['title']}\nSummary: {a['summary']}\nLink: {a['link']}\n\n"

    return text

def wrap_html(content):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>AI Tech News Update</title>

<style>
    body {{
        margin: 0;
        padding: 0;
        background: #f2f2f2;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #111;
    }}

    .container {{
        max-width: 760px;
        margin: auto;
        padding: 45px;
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(12px);
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.6);
        box-shadow: 0 20px 50px rgba(0,0,0,0.08);
    }}

    .header {{
        text-align: center;
        padding-bottom: 30px;
        border-bottom: 1px solid #e5e5e5;
    }}

    .header h1 {{
        font-size: 32px;
        font-weight: 600;
        margin: 0;
        color: #111;
        letter-spacing: 0.6px;
    }}

    .header .tagline {{
        font-size: 15px;
        color: #666;
        margin-top: 8px;
        letter-spacing: 0.3px;
    }}

    .news-list {{
        margin-top: 35px;
        padding-left: 0;
        list-style: none;
    }}

    .news-item {{
        background: linear-gradient(145deg, #ffffff, #f7f7f7);
        padding: 26px 28px;
        margin-bottom: 22px;
        border-radius: 18px;
        border: 1px solid #e8e8e8;
        transition: 0.25s ease;
    }}

    .news-item:hover {{
        background: linear-gradient(145deg, #fafafa, #ffffff);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    }}

    .news-item strong {{
        font-size: 19px;
        font-weight: 600;
        color: #111;
    }}

    .news-item p {{
        margin: 10px 0 14px;
        font-size: 15px;
        color: #444;
        line-height: 1.55;
    }}

    .news-item a {{
        color: #007aff;
        text-decoration: none;
        font-weight: 500;
        font-size: 15px;
    }}

    .footer {{
        margin-top: 40px;
        text-align: center;
        font-size: 13px;
        color: #777;
        border-top: 1px solid #e5e5e5;
        padding-top: 18px;
    }}
</style>

</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Tech News Update</h1>
            <div class="tagline">Curated by your autonomous AI agent</div>
        </div>

        <ul class="news-list">
            {content}
        </ul>

        <div class="footer">
            This email was generated automatically by your AI News Agent.
        </div>
    </div>
</body>
</html>
"""

def summarize_with_llm(articles):
    if not articles:
        return "<h2>No articles fetched.</h2>"

    prompt = build_llm_prompt(articles)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # stable + supported
        messages=[
            {"role": "system", "content": "You write clean, concise HTML summaries."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content

def main():
    print("Fetching global tech/AI news from RSS...")
    articles = fetch_all_news()
    print(f"Fetched {len(articles)} articles.")

    print("Letting the model think and pick AI-related news...")
    llm_output = summarize_with_llm(articles)

    print("Wrapping in Tesla premium HTML...")
    html_content = wrap_html(llm_output)

    print("Sending email...")
    send_email("Your AI Tech News Update", html_content)

    print("Done.")

if __name__ == "__main__":
    main()
