#!/usr/bin/env python3

import json
from pathlib import Path
from supertonic import TTS

LANG = "sv"
SPEED = 0.9
TOTAL_STEPS = 8
VOICE_NAMES = ["F1", "F2", "F3", "F4", "F5", "M1", "M2", "M3", "M4", "M5"]
SAMPLE_IDS = ["26", "31", "33", "34", "36", "37", "39"]
OUTPUT_DIR = Path("voice_comparison_supertonic")


def generate(messages):
    tts = TTS(auto_download=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for voice_name in VOICE_NAMES:
        voice_style = tts.get_voice_style(voice_name)

        for key, value in messages.items():
            phrase = value["phrase"]

            print(f"[{voice_name}] Generating {key}: {phrase}")
            wav, duration = tts.synthesize(
                phrase,
                voice_style=voice_style,
                lang=LANG,
                total_steps=TOTAL_STEPS,
                speed=SPEED,
            )

            out_path = OUTPUT_DIR / f"{key}_{voice_name}.wav"
            tts.save_audio(wav, str(out_path))
            print(f"Saved {out_path} ({duration[0]:.2f}s)")


if __name__ == "__main__":
    with open("audios.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
        filtered = {k: v for k, v in messages.items() if k in SAMPLE_IDS}
        generate(filtered)
