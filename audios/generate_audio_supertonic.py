#!/usr/bin/env python3

import json
from pathlib import Path
from supertonic import TTS

VOICE_NAME = "F1"
LANG = "sv"
SPEED = 1.0
TOTAL_STEPS = 8
OUTPUT_DIR = Path("files_supertonic")


def generate(messages):
    tts = TTS(auto_download=True)
    voice_style = tts.get_voice_style(VOICE_NAME)

    for key, value in messages.items():
        filename = value["filename"]
        phrase = value["phrase"]

        print(f"Generating audio for {key}: {phrase} (filename: {filename})")
        wav, duration = tts.synthesize(
            phrase,
            voice_style=voice_style,
            lang=LANG,
            total_steps=TOTAL_STEPS,
            speed=SPEED,
        )

        out_path = OUTPUT_DIR / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        tts.save_audio(wav, str(out_path))
        print(f"Saved {out_path} ({duration[0]:.2f}s)")


if __name__ == "__main__":
    FROM_ID = 1
    TO_ID = 999
    with open("audios.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
        filtered = {k: v for k, v in messages.items() if FROM_ID <= int(k) <= TO_ID}
        generate(filtered)
