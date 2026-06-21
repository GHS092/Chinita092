#!/usr/bin/env python3
"""
Fetch a YouTube video transcript and output it as structured JSON.

Usage:
    python fetch_transcript.py <url_or_video_id> [--language en,tr] [--timestamps]

Output (JSON):
    {
        "video_id": "...",
        "language": "en",
        "segments": [{"text": "...", "start": 0.0, "duration": 2.5}, ...],
        "full_text": "complete transcript as plain text",
        "timestamped_text": "00:00 first line\n00:05 second line\n..."
    }

Install dependency:  pip install youtube-transcript-api
"""

import argparse
import json
import re
import sys


def extract_video_id(url_or_id: str) -> str:
    """Extract the 11-character video ID from various YouTube URL formats."""
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
    """Convert seconds to HH:MM:SS or MM:SS format."""
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


import random
import urllib.request

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"
]

def fetch_proxies():
    try:
        req = urllib.request.Request(
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=US&ssl=yes&anonymity=elite',
            headers={'User-Agent': random.choice(USER_AGENTS)}
        )
        res = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        proxies = [p.strip() for p in res.split('\n') if p.strip()]
        random.shuffle(proxies)
        return proxies[:10]
    except:
        return []

def fetch_transcript(video_id: str, languages: list = None):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("Error: youtube-transcript-api not installed. Run: pip install youtube-transcript-api", file=sys.stderr)
        sys.exit(1)

    # Intento 1: Directo con rotación de User-Agent (puede fallar si Railway esta baneado)
    import requests
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        api = YouTubeTranscriptApi(http_client=session)
        if languages:
            result = api.fetch(video_id, languages=languages)
        else:
            result = api.fetch(video_id)
        return [{"text": seg.text, "start": seg.start, "duration": seg.duration} for seg in result]
    except Exception as e:
        error_msg = str(e).lower()
        if "blocking requests from your ip" not in error_msg and "too many requests" not in error_msg:
            raise e # Es un error real (no tiene subs, esta desactivado, etc)
        
        # BAN DETECTADO: Usamos nuestra magia de proxies rotativos
        proxies_list = fetch_proxies()
        if not proxies_list:
            raise Exception("IP de Railway baneada por YouTube y falló la extracción de proxies de rescate.")
        
        import requests
        last_err = e
        for proxy in proxies_list:
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            session = requests.Session()
            session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
            session.proxies.update(proxy_dict)
            
            try:
                api = YouTubeTranscriptApi(http_client=session)
                if languages:
                    result = api.fetch(video_id, languages=languages)
                else:
                    result = api.fetch(video_id)
                return [{"text": seg.text, "start": seg.start, "duration": seg.duration} for seg in result]
            except Exception as proxy_e:
                error_msg_proxy = str(proxy_e).lower()
                # Si falló por proxy malo o baneado, intentamos el siguiente
                if "blocking requests" in error_msg_proxy or "proxy" in error_msg_proxy or "timeout" in error_msg_proxy or "connection" in error_msg_proxy or "too many requests" in error_msg_proxy:
                    last_err = proxy_e
                    continue
                raise proxy_e # Otro error real
                
        raise Exception(f"Fallo al evadir el baneo IP de YouTube tras intentar con {len(proxies_list)} proxies. Último error: {last_err}")


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript as JSON")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--language", "-l", default=None,
                        help="Comma-separated language codes (e.g. en,tr). Default: auto")
    parser.add_argument("--timestamps", "-t", action="store_true",
                        help="Include timestamped text in output")
    parser.add_argument("--text-only", action="store_true",
                        help="Output plain text instead of JSON")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    languages = [l.strip() for l in args.language.split(",")] if args.language else None

    try:
        segments = fetch_transcript(video_id, languages)
    except Exception as e:
        error_msg = str(e)
        if "disabled" in error_msg.lower():
            print(json.dumps({"error": "Transcripts are disabled for this video."}))
        elif "no transcript" in error_msg.lower():
            print(json.dumps({"error": f"No transcript found. Try specifying a language with --language."}))
        else:
            print(json.dumps({"error": error_msg}))
        sys.exit(1)

    full_text = " ".join(seg["text"] for seg in segments)
    timestamped = "\n".join(
        f"{format_timestamp(seg['start'])} {seg['text']}" for seg in segments
    )

    if args.text_only:
        print(timestamped if args.timestamps else full_text)
        return

    result = {
        "video_id": video_id,
        "segment_count": len(segments),
        "duration": format_timestamp(segments[-1]["start"] + segments[-1]["duration"]) if segments else "0:00",
        "full_text": full_text,
    }
    if args.timestamps:
        result["timestamped_text"] = timestamped

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
