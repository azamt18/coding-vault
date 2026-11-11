"""Tests for try_eleven_v4.py. The ElevenLabs client is mocked; no network."""

from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

import try_eleven_v4 as v4

HERE = Path(__file__).parent


@pytest.fixture
def client():
    c = mock.MagicMock()
    c.text_to_speech.convert.return_value = iter([b"ab", b"cd"])
    c.voices.ivc.create.return_value = SimpleNamespace(voice_id="clone123")
    c.voices.get_all.return_value = SimpleNamespace(
        voices=[SimpleNamespace(name="Aria", voice_id="aria_id")]
    )
    return c


@pytest.fixture
def env(tmp_path, monkeypatch, client):
    """Key set, client factory patched, all paths pointed into tmp_path."""
    monkeypatch.setenv("ELEVEN_KEY", "k")
    monkeypatch.setattr(v4, "make_client", lambda key: client)
    text = tmp_path / "sharaf_p1.txt"
    text.write_text("Zamonaviy dunyoda o'zimizga\n", encoding="utf-8")
    ref = tmp_path / "reference.wav"
    ref.write_bytes(b"RIFF")
    base = [
        "--text-file", str(text),
        "--audio-dir", str(tmp_path / "audio"),
        "--voice-id-file", str(tmp_path / ".eleven_voice_id"),
        "--reference", str(ref),
    ]
    return SimpleNamespace(tmp=tmp_path, base=base, client=client)


def test_default_text_file_is_committed_sample():
    assert v4.DEFAULT_TEXT_FILE == HERE / "samples" / "sharaf_p1.txt"
    assert v4.DEFAULT_TEXT_FILE.read_text(encoding="utf-8").startswith(
        "Zamonaviy dunyoda qanday qilib"
    )


def test_convert_called_with_v4_uz_and_file_text(env):
    assert v4.main(env.base) == 0
    kw = env.client.text_to_speech.convert.call_args.kwargs
    assert kw["model_id"] == "eleven_v4"
    assert kw["language_code"] == "uz"
    assert kw["text"] == "Zamonaviy dunyoda o'zimizga"
    assert kw["output_format"] == "mp3_44100_128"
    assert kw["voice_id"] == "aria_id"  # preset name resolved to id


def test_preset_output_path_and_bytes(env):
    v4.main(env.base + ["--voice", "Aria"])
    out = env.tmp / "audio" / "v4_aria_sharaf_p1.mp3"
    assert out.read_bytes() == b"abcd"


def test_unknown_voice_is_used_as_id(env):
    v4.main(env.base + ["--voice", "XyZ123"])
    assert env.client.text_to_speech.convert.call_args.kwargs["voice_id"] == "XyZ123"


def test_clone_creates_once_and_saves_id(env):
    assert v4.main(env.base + ["--clone"]) == 0
    env.client.voices.ivc.create.assert_called_once()
    assert (env.tmp / ".eleven_voice_id").read_text().strip() == "clone123"
    assert env.client.text_to_speech.convert.call_args.kwargs["voice_id"] == "clone123"
    assert (env.tmp / "audio" / "v4_clone_sharaf_p1.mp3").exists()


def test_clone_reuses_saved_id(env):
    (env.tmp / ".eleven_voice_id").write_text("saved42\n")
    v4.main(env.base + ["--clone"])
    env.client.voices.ivc.create.assert_not_called()
    assert env.client.text_to_speech.convert.call_args.kwargs["voice_id"] == "saved42"


def test_missing_key_exits_nonzero(env, monkeypatch, capsys):
    monkeypatch.delenv("ELEVEN_KEY")
    with pytest.raises(SystemExit) as e:
        v4.main(env.base)
    assert e.value.code != 0
    assert "ELEVEN_KEY" in capsys.readouterr().err
    env.client.text_to_speech.convert.assert_not_called()
