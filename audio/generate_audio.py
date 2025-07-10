#!/usr/bin/env python3

import os
import wave
import json
from google import genai
from google.genai import types

messages = [
    # NUMBERS: 1..20
    {"text": "1", "filename": "1"},
    {"text": "2", "filename": "2"},
    {"text": "3", "filename": "3"},
    {"text": "4", "filename": "4"},
    {"text": "5", "filename": "5"},
    {"text": "6", "filename": "6"},
    {"text": "7", "filename": "7"},
    {"text": "8", "filename": "8"},
    {"text": "9", "filename": "9"},
    {"text": "10", "filename": "10"},
    {"text": "11", "filename": "11"},
    {"text": "12", "filename": "12"},
    {"text": "13", "filename": "13"},
    {"text": "14", "filename": "14"},
    {"text": "15", "filename": "15"},
    {"text": "16", "filename": "16"},
    {"text": "17", "filename": "17"},
    {"text": "18", "filename": "18"},
    {"text": "19", "filename": "19"},
    {"text": "20", "filename": "20"},
    # PRE-FIRE commands starting from 21
    {"text": "Banan är öppen", "filename": "21"},
    {"text": "Förberedelsetid start", "filename": "22"},
    {"text": "Förberedelsetid stop", "filename": "23"},
    {"text": "Alla klara?", "filename": "24"},
    {"text": "Ladda!", "filename": "25"},
    {"text": "10 sekunder kvar!", "filename": "26"},
    {"text": "10 sekunder", "filename": "27"},
    {"text": "8 sekunder", "filename": "28"},
    {"text": "6 sekunder", "filename": "29"},
    {"text": "Färdiga!", "filename": "30"},
    {"text": "Färdiga (utdraget)", "filename": "31"},
    # FIRE and POST-FIRE commands starting from 32
    {"text": "Eld!", "filename": "32"},
    {"text": "Eld upphör!", "filename": "33"},
    {"text": "Eld upphör (utdraget)", "filename": "34"},
    {"text": "Några funktioneringsfel?", "filename": "35"},
    {"text": "Patron ur, proppa och lägg ned vapnet!", "filename": "36"},
    {"text": "Patron ur, proppa vapen!", "filename": "37"},
    {"text": "Visitation!", "filename": "38"},
    {"text": "Markera!", "filename": "39"},
    # Provserie: 40
    {"text": "Provserie", "filename": "40"},
    # Serie nummer 1..12: 41..52
    {"text": "Serie nummer 1", "filename": "41"},
    {"text": "Serie nummer 2", "filename": "42"},
    {"text": "Serie nummer 3", "filename": "43"},
    {"text": "Serie nummer 4", "filename": "44"},
    {"text": "Serie nummer 5", "filename": "45"},
    {"text": "Serie nummer 6", "filename": "46"},
    {"text": "Serie nummer 7", "filename": "47"},
    {"text": "Serie nummer 8", "filename": "48"},
    {"text": "Serie nummer 9", "filename": "49"},
    {"text": "Serie nummer 10", "filename": "50"},
    {"text": "Serie nummer 11", "filename": "51"},
    {"text": "Serie nummer 12", "filename": "52"},
    {"text": "Serie", "filename": "53"},
    {"text": "Serie nummer 1 10 sekunder", "filename": "54"},
    {"text": "Serie nummer 2 10 sekunder", "filename": "55"},
    {"text": "Serie nummer 3 10 sekunder", "filename": "56"},
    {"text": "Serie nummer 4 10 sekunder", "filename": "57"},
    {"text": "Serie nummer 1 8 sekunder", "filename": "58"},
    {"text": "Serie nummer 2 8 sekunder", "filename": "59"},
    {"text": "Serie nummer 3 8 sekunder", "filename": "60"},
    {"text": "Serie nummer 4 8 sekunder", "filename": "61"},
    {"text": "Serie nummer 1 6 sekunder", "filename": "62"},
    {"text": "Serie nummer 2 6 sekunder", "filename": "63"},
    {"text": "Serie nummer 3 6 sekunder", "filename": "64"},
    {"text": "Serie nummer 4 6 sekunder", "filename": "65"},
    # The rest (keep original numbering for other texts)
    {"text": "Omskjutning", "filename": "70"},
    # start with 40
    {"text": "Färdigskjutning 1", "filename": "71"},
    {"text": "Färdigskjutning 2", "filename": "72"},
    {"text": "Färdigskjutning", "filename": "73"},
    {"text": "Färdigskjutning 1 10 sekunder", "filename": "74"},
    {"text": "Färdigskjutning 2 10 sekunder", "filename": "75"},
    {"text": "Färdigskjutning 1 8 sekunder", "filename": "76"},
    {"text": "Färdigskjutning 2 8 sekunder", "filename": "77"},
    {"text": "Färdigskjutning 1 6 sekunder", "filename": "78"},
    {"text": "Färdigskjutning 2 6 sekunder", "filename": "79"},
]


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    print(
        f"WAV file saved as {filename} (channels={channels}, rate={rate}, width={sample_width})"
    )


def generate(messages):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro-preview-tts"

    STYLE = (
        "En skånsk kvinnlig röst ger instruktioner/kommandon till skyttar under en skyttetävling. "
        "Det behöver vara tydligt och lite bestämd. Texten '(utdraget)' ska inte läsas ut utan då ska frasen vara utdragen och ta 2.9 sekunder.\n\n"
    )

    index = {}

    for msg in messages:
        file_name = msg["filename"] + ".wav"

        print(f"Generating audio for: {msg['text']} (filename: {file_name})")
        prompt = STYLE + msg["text"]
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr")
                )
            ),
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        part = response.candidates[0].content.parts[0]
        if hasattr(part, "inline_data") and part.inline_data and part.inline_data.data:
            print(
                f"Saving {file_name} with {len(part.inline_data.data)} bytes of PCM data"
            )
            wave_file(
                file_name, part.inline_data.data, channels=1, rate=24000, sample_width=2
            )
            # Add entry to index
            index[msg["filename"]] = {"title": msg["text"], "filename": file_name}
        else:
            if hasattr(response, "text") and response.text:
                print(response.text)

    # Save index.json
    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print("index.json saved.")


if __name__ == "__main__":
    generate(messages[:1])
