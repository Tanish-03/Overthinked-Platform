APP_NAME="Dump & Breathe"
TAGLINE="A safe, anonymous spave for overthinkers - write, release, and recieve kindness"
THEME = {
    "primary" : "#4A90E2",
    "bg_light" :"#f7f9fc",
    "card_bg":"#ffffff",
    "text_muted":"#6b7280"
}
GROQ_MODEL = "llama-3.1-8b-instant"  # fast, low-cost

# Try these in order if a model is unavailable/deprecated
GROQ_MODEL_CANDIDATES = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]
