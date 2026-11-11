"""Tests for try_eleven_v4.py. The ElevenLabs client is mocked; no network."""

from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

from elevenlabs import VoiceSettings
from elevenlabs.core.api_error import ApiError

import try_eleven_v4 as v4

HERE = Path(__file__).parent


@pytest.fixture
def client():
    c = mock.MagicMock()
    c.text_to_speech.convert.return_value = iter([b"ab", b"cd"])
    c.voices.ivc.create.return_value = SimpleNamespace(voice_id="clone123")
    c.voices.get_all.return_value = SimpleNamespace(
        voices=[
            SimpleNamespace(name="George - Warm, Captivating Storyteller", voice_id="george_id"),
            SimpleNamespace(name="Aria", voice_id="aria_id"),
        ]
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
    assert kw["voice_id"] == "george_id"  # default preset George, resolved to id


def test_preset_output_path_and_bytes(env):
    v4.main(env.base + ["--voice", "Aria"])
    out = env.tmp / "audio" / "v4_aria_sharaf_p1.mp3"
    assert out.read_bytes() == b"abcd"


def test_default_output_is_labelled_george(env):
    v4.main(env.base)
    assert (env.tmp / "audio" / "v4_george_sharaf_p1.mp3").read_bytes() == b"abcd"


def test_name_matches_prefix_before_dash(env):
    v4.main(env.base + ["--voice", "george"])
    assert env.client.text_to_speech.convert.call_args.kwargs["voice_id"] == "george_id"


def test_voice_id_on_account_is_labelled_with_short_name(env):
    v4.main(env.base + ["--voice", "george_id"])
    assert env.client.text_to_speech.convert.call_args.kwargs["voice_id"] == "george_id"
    assert (env.tmp / "audio" / "v4_george_sharaf_p1.mp3").exists()


def test_no_voice_settings_by_default(env):
    v4.main(env.base)
    assert "voice_settings" not in env.client.text_to_speech.convert.call_args.kwargs


def test_stability_and_similarity_send_voice_settings(env):
    v4.main(env.base + ["--stability", "0.5", "--similarity", "0.75"])
    vs = env.client.text_to_speech.convert.call_args.kwargs["voice_settings"]
    assert isinstance(vs, VoiceSettings)
    assert (vs.stability, vs.similarity_boost) == (0.5, 0.75)


def test_one_setting_alone_sends_only_that_field(env):
    v4.main(env.base + ["--stability", "0.3"])
    vs = env.client.text_to_speech.convert.call_args.kwargs["voice_settings"]
    assert vs.stability == 0.3 and vs.similarity_boost is None


def test_setting_out_of_range_is_rejected(env):
    with pytest.raises(SystemExit) as e:
        v4.main(env.base + ["--similarity", "75"])
    assert e.value.code == 2
    env.client.text_to_speech.convert.assert_not_called()


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


def _failing_stream():
    yield b"partial"
    raise ApiError(status_code=404, body={"detail": {"status": "voice_not_found",
                                                    "message": "A voice with that ID was not found."}})


def test_failed_stream_leaves_no_output_file(env):
    env.client.text_to_speech.convert.return_value = _failing_stream()
    with pytest.raises(SystemExit):
        v4.main(env.base)
    audio = env.tmp / "audio"
    assert not list(audio.glob("*")) if audio.exists() else True


def test_api_error_prints_message_and_exits_nonzero(env, capsys):
    env.client.text_to_speech.convert.return_value = _failing_stream()
    with pytest.raises(SystemExit) as e:
        v4.main(env.base)
    assert e.value.code not in (0, None)
    err = capsys.readouterr().err
    assert "A voice with that ID was not found." in err
    assert "Traceback" not in err


def test_api_error_on_clone_prints_message(env, capsys):
    env.client.voices.ivc.create.side_effect = ApiError(
        status_code=401, body={"detail": {"status": "paid_plan_required",
                                          "message": "Instant voice cloning needs a paid plan."}})
    with pytest.raises(SystemExit) as e:
        v4.main(env.base + ["--clone"])
    assert e.value.code not in (0, None)
    assert "paid plan" in capsys.readouterr().err
    assert not (env.tmp / ".eleven_voice_id").exists()
