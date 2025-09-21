import os, json, requests
from typing import Dict, Tuple
from .config import GROQ_MODEL

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def _build_messages(user_text: str):
    system_prompt = (
        "You are a kind, concise listener for overthinkers. "
        "ALWAYS return a valid JSON object with EXACTLY these keys: "
        "suggestion (string), spiritual (string), action (string). "
        "Use a warm, respectful tone. For 'spiritual', you may include "
        "Sikh/Hindu-inspired lines in plain language. Keep each under 2–3 sentences."
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"User wrote:\n{user_text}\nReturn JSON only."}
    ]

def _parse_json_safe(text: str) -> Dict[str, str]:
    try:
        return json.loads(text)
    except Exception:
        import re
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        return {
            "suggestion": text.strip(),
            "spiritual": "Breathe gently; remember you are not your thoughts.",
            "action": "Set a 2-minute timer and write one next tiny step."
        }

def get_ai_response(user_text: str, api_key: str | None = None) -> Tuple[bool, Dict[str, str] | str]:
    key = api_key or os.getenv("GROQ_API_KEY", "")
    if not key:
        return False, "Missing GROQ_API_KEY. Add it in .streamlit/secrets.toml or as an environment variable."

    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": _build_messages(user_text),
        "temperature": 0.6,
        "response_format": {"type": "json_object"}
    }
    try:
        resp = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=45)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        data = _parse_json_safe(content)
        for k in ["suggestion", "spiritual", "action"]:
            data.setdefault(k, "")
        return True, data
    except requests.HTTPError as e:
        try:
            detail = resp.json()
        except Exception:
            detail = str(e)
        return False, f"HTTP error from Groq: {detail}"
    except Exception as e:
        return False, f"Unexpected error: {e}"
