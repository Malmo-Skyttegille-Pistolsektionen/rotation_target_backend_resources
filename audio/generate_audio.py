#!/usr/bin/env python3
import os
import mimetypes
import struct
from google import genai
from google.genai import types

messages = [
    {"text": "Serie", "filename": "serie.wav"},
    {"text": "Provserie", "filename": "provserie.wav"},
    {"text": "Serie nummer 1", "filename": "serie_nummer_1.wav"},
    {"text": "Serie nummer 2", "filename": "serie_nummer_2.wav"},
    {"text": "Serie nummer 3", "filename": "serie_nummer_3.wav"},
    {"text": "Serie nummer 4", "filename": "serie_nummer_4.wav"},
    {"text": "Serie nummer 5", "filename": "serie_nummer_5.wav"},
    {"text": "Serie nummer 6", "filename": "serie_nummer_6.wav"},
    {"text": "Serie nummer 7", "filename": "serie_nummer_7.wav"},
    {"text": "Serie nummer 8", "filename": "serie_nummer_8.wav"},
    {"text": "Serie nummer 9", "filename": "serie_nummer_9.wav"},
    {"text": "Serie nummer 10", "filename": "serie_nummer_10.wav"},
    {"text": "Serie nummer 11", "filename": "serie_nummer_11.wav"},
    {"text": "Serie nummer 12", "filename": "serie_nummer_12.wav"},
    {"text": "Omskjutning", "filename": "omskjutning.wav"},
    {"text": "Färdigskjutning 1", "filename": "fardigskjutning_1.wav"},
    {"text": "Färdigskjutning 2", "filename": "fardigskjutning_2.wav"},
    {
        "text": "Färdigskjutning 1 10 sekunder",
        "filename": "fardigskjutning_1_10_sekunder.wav",
    },
    {
        "text": "Färdigskjutning 2 10 sekunder",
        "filename": "fardigskjutning_2_10_sekunder.wav",
    },
    {
        "text": "Färdigskjutning 1 8 sekunder",
        "filename": "fardigskjutning_1_8_sekunder.wav",
    },
    {
        "text": "Färdigskjutning 2 8 sekunder",
        "filename": "fardigskjutning_2_8_sekunder.wav",
    },
    {
        "text": "Färdigskjutning 1 6 sekunder",
        "filename": "fardigskjutning_1_6_sekunder.wav",
    },
    {
        "text": "Färdigskjutning 2 6 sekunder",
        "filename": "fardigskjutning_2_6_sekunder.wav",
    },
    {"text": "1", "filename": "nummer_1.wav"},
    {"text": "2", "filename": "nummer_2.wav"},
    {"text": "3", "filename": "nummer_3.wav"},
    {"text": "4", "filename": "nummer_4.wav"},
    {"text": "5", "filename": "nummer_5.wav"},
    {"text": "6", "filename": "nummer_6.wav"},
    {"text": "7", "filename": "nummer_7.wav"},
    {"text": "8", "filename": "nummer_8.wav"},
    {"text": "9", "filename": "nummer_9.wav"},
    {"text": "10", "filename": "nummer_10.wav"},
    {"text": "11", "filename": "nummer_11.wav"},
    {"text": "12", "filename": "nummer_12.wav"},
    {"text": "13", "filename": "nummer_13.wav"},
    {"text": "14", "filename": "nummer_14.wav"},
    {"text": "15", "filename": "nummer_15.wav"},
    {"text": "16", "filename": "nummer_16.wav"},
    {"text": "17", "filename": "nummer_17.wav"},
    {"text": "18", "filename": "nummer_18.wav"},
    {"text": "19", "filename": "nummer_19.wav"},
    {"text": "20", "filename": "nummer_20.wav"},
    {"text": "10 sekunder", "filename": "10_sekunder.wav"},
    {"text": "8 sekunder", "filename": "8_sekunder.wav"},
    {"text": "6 sekunder", "filename": "6_sekunder.wav"},
    {"text": "Ladda!", "filename": "ladda.wav"},
    {"text": "Färdiga!", "filename": "fardiga_utrop.wav"},
    {"text": "*Färdiga", "filename": "fardiga.wav"},
    {"text": "Eld!", "filename": "eld.wav"},
    {"text": "Eld upphör!", "filename": "eld_upphor_utrop.wav"},
    {"text": "*Eld upphör", "filename": "eld_upphor.wav"},
    {"text": "10 sekunder kvar!", "filename": "10_sekunder_kvar.wav"},
    {"text": "Några funktionsfel?", "filename": "nagrafunktionsfel.wav"},
    {
        "text": "Patron ur, proppa och lägg ned vapnet!",
        "filename": "patron_ur_proppa_lagg_ned_vapnet.wav",
    },
    {"text": "Patron ur, proppa vapen!", "filename": "patron_ur_proppa_vapen.wav"},
    {"text": "Visitation", "filename": "visitation.wav"},
]


def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"Ljudfil sparad som {file_name}")


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        chunk_size,
        b"WAVE",
        b"fmt ",
        16,
        1,
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size,
    )
    return header + audio_data


def parse_audio_mime_type(mime_type: str) -> dict:
    bits_per_sample = 16
    rate = 24000
    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro-preview-tts"

    STYLE = (
        "En skånsk kvinnlig röst ger instruktioner/kommandon till skyttar under en skyttetävling. "
        "Det behöver vara tydligt och lite bestämd. Rader som börjar med * ska vara utdragna och ta 2.9 sekunder"
    )

    for msg in messages:
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

        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
            part = chunk.candidates[0].content.parts[0]
            if (
                hasattr(part, "inline_data")
                and part.inline_data
                and part.inline_data.data
            ):
                file_name = msg["filename"]
                inline_data = part.inline_data
                data_buffer = inline_data.data
                file_extension = os.path.splitext(file_name)[1]
                if not file_extension:
                    file_extension = (
                        mimetypes.guess_extension(inline_data.mime_type) or ".wav"
                    )
                    file_name += file_extension
                if file_extension != ".wav":
                    data_buffer = convert_to_wav(
                        inline_data.data, inline_data.mime_type
                    )
                    file_name = os.path.splitext(file_name)[0] + ".wav"
                save_binary_file(file_name, data_buffer)
            else:
                if hasattr(chunk, "text") and chunk.text:
                    print(chunk.text)


if __name__ == "__main__":
    for item in messages:
        if isinstance(item, list):
            for subitem in item:
                print(f"{subitem['text']}")  # \n{subitem['filename']}")
        else:
            print(f"{item['text']}")  # \n{item['filename']}")

    # generate()
