#!/usr/bin/env python3
import argparse
import json
import re
import sys
import random
import time

def extract_video_id(url_or_id: str) -> str:
    url_or_id = url_or_id.strip()
    patterns = [
        r'(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id

def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
    ]
    return random.choice(user_agents)

def get_free_proxies():
    try:
        import urllib.request
        url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=US&ssl=all&anonymity=all'
        proxies = urllib.request.urlopen(url, timeout=10).read().decode('utf-8').split()
        return [p.strip() for p in proxies if p.strip()]
    except Exception:
        return []

def fetch_transcript(video_id: str, languages: list = None):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        import requests
    except ImportError:
        print("Error: youtube-transcript-api or requests not installed. Run: pip install youtube-transcript-api requests", file=sys.stderr)
        sys.exit(1)

    # Strategy 1: Direct fetch with random User-Agent (Cleanest, lowest latency)
    session = requests.Session()
    session.headers.update({"User-Agent": get_random_user_agent(), "Accept-Language": "en-US,en;q=0.9"})
    api = YouTubeTranscriptApi(http_client=session)
    
    try:
        if languages:
            result = api.fetch(video_id, languages=languages)
        else:
            result = api.fetch(video_id)
        return [{"text": seg.text, "start": seg.start, "duration": seg.duration} for seg in result]
    except Exception as e:
        error_msg = str(e).lower()
        if "disabled" in error_msg or "no transcript" in error_msg:
            raise e # Real error, not a block
        # Strategy 2: Rotating Proxies + Random Delays
        print("Attempt 1 failed. Rotating User-Agent and trying proxies...", file=sys.stderr)

    proxies = get_free_proxies()
    random.shuffle(proxies)
    
    max_retries = min(5, len(proxies) if proxies else 3)
    last_error = None
    
    for i in range(max_retries):
        time.sleep(random.uniform(1.0, 3.0)) # Throttling
        session = requests.Session()
        session.headers.update({"User-Agent": get_random_user_agent(), "Accept-Language": "en-US,en;q=0.9"})
        
        if proxies:
            proxy = proxies.pop()
            session.proxies.update({"http": f"http://{proxy}", "https": f"http://{proxy}"})
            
        api = YouTubeTranscriptApi(http_client=session)
        try:
            if languages:
                result = api.fetch(video_id, languages=languages)
            else:
                result = api.fetch(video_id)
            return [{"text": seg.text, "start": seg.start, "duration": seg.duration} for seg in result]
        except Exception as e:
            last_error = e
            continue
            
    raise last_error

def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript as JSON")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--language", "-l", default=None, help="Comma-separated language codes (e.g. en,tr). Default: auto")
    parser.add_argument("--timestamps", "-t", action="store_true", help="Include timestamped text in output")
    parser.add_argument("--text-only", action="store_true", help="Output plain text instead of JSON")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    languages = [l.strip() for l in args.language.split(",")] if args.language else None

    try:
        segments = fetch_transcript(video_id, languages)
        if args.text_only:
            text = " ".join([seg['text'] for seg in segments])
            print(text)
        else:
            print(json.dumps(segments))
    except Exception as e:
        error_msg = str(e)
        if "disabled" in error_msg.lower():
            print(json.dumps({"error": "Transcripts are disabled for this video."}))
        elif "no transcript" in error_msg.lower():
            print(json.dumps({"error": f"No transcript found. Try specifying a language with --language."}))
        else:
            print(json.dumps({"error": error_msg}))
        sys.exit(1)

if __name__ == "__main__":
    main()
