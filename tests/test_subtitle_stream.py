#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

import pytest

from fese import FFprobeSubtitleStream
from fese import LanguageNotFound


@pytest.fixture
def sub_stream():
    return {
        "index": 3,
        "codec_name": "ass",
        "codec_long_name": "ASS (Advanced SSA) subtitle",
        "codec_type": "subtitle",
        "codec_tag_string": "[0][0][0][0]",
        "codec_tag": "0x0000",
        "r_frame_rate": "0/0",
        "avg_frame_rate": "0/0",
        "time_base": "1/1000",
        "start_pts": 0,
        "start_time": "0.000000",
        "duration_ts": 1218718,
        "duration": "1218.718000",
        "disposition": {
            "default": 1,
            "dub": 0,
            "original": 0,
            "comment": 0,
            "lyrics": 0,
            "karaoke": 0,
            "forced": 0,
            "hearing_impaired": 0,
            "visual_impaired": 0,
            "clean_effects": 0,
            "attached_pic": 0,
            "timed_thumbnails": 0,
        },
        "tags": {"language": "eng", "title": "English"},
    }


@pytest.fixture
def subtitle(sub_stream):
    return FFprobeSubtitleStream(sub_stream)


def test_init(subtitle):
    assert subtitle.extension == "ass"
    assert subtitle.duration == pytest.approx(1218.71800)


def test_language(subtitle):
    assert subtitle.language.alpha3 == "eng"


def test_suffix(subtitle):
    assert subtitle.suffix == "en.ass"


def test_disposition(subtitle):
    assert subtitle.disposition.hearing_impaired == False


def test_wo_language(sub_stream):
    new_stream = copy.copy(sub_stream)
    new_stream["tags"].update({"language": "Unknown"})
    with pytest.raises(LanguageNotFound):
        FFprobeSubtitleStream(new_stream)


def test_language_converter_exception(sub_stream):
    new_stream = copy.copy(sub_stream)
    new_stream["tags"].update({"language": "fil"})
    with pytest.raises(LanguageNotFound):
        FFprobeSubtitleStream(new_stream)


@pytest.mark.parametrize(
    "content,alpha3,expected_country",
    [
        ("brazil", "por", "BR"),
        ("latino", "spa", "MX"),
        ("braSil", "por", "BR"),
        ("mExico", "spa", "MX"),
    ],
)
def test_w_custom_language(sub_stream, content, alpha3, expected_country):
    new_stream = copy.copy(sub_stream)
    new_stream["tags"].update({"title": content, "language": alpha3})
    sub = FFprobeSubtitleStream(new_stream)
    assert sub.language.country == expected_country
