from handle_audio import handle_audio_message
from unittest.mock import patch

@patch("handle_audio.transcribe_audio")
@patch("handle_audio.perform_classification")
def test_handle_audio_message_with_transcribed_text(mock_perform_classification, mock_transcribe_audio):
    mock_transcribe_audio.return_value = ("transcribed_text", 200)
    mock_perform_classification.side_effect = [["audio_intent1"], ["text_intent1"]]
    message = {"message": "text_message", "audio": "audio_blob"}
    handle_audio_message(message)
    mock_transcribe_audio.assert_called_once_with({"audio": "audio_blob"})
    mock_perform_classification.assert_any_call("text_message")
    mock_perform_classification.assert_any_call("transcribed_text")
    # Make assertions for the emit function as per your implementation.

@patch("handle_audio.transcribe_audio")
@patch("handle_audio.perform_classification")
def test_handle_audio_message_without_transcribed_text(mock_perform_classification, mock_transcribe_audio):
    mock_transcribe_audio.return_value = (None, 404)  # Simulating failure
    mock_perform_classification.return_value = ["text_intent1"]
    message = {"message": "text_message", "audio": "audio_blob"}
    handle_audio_message(message)
    mock_transcribe_audio.assert_called_once_with({"audio": "audio_blob"})
    mock_perform_classification.assert_called_once_with("text_message")
    # Make assertions for the emit function as per your implementation.

@patch("handle_audio.transcribe_audio")
@patch("handle_audio.perform_classification")
def test_handle_audio_message_with_empty_text(mock_perform_classification, mock_transcribe_audio):
    mock_transcribe_audio.return_value = ("transcribed_text", 200)
    mock_perform_classification.side_effect = [[], ["text_intent1"]]
    message = {"message": "", "audio": "audio_blob"}
    handle_audio_message(message)
    mock_transcribe_audio.assert_called_once_with({"audio": "audio_blob"})
    mock_perform_classification.assert_any_call("")
    mock_perform_classification.assert_any_call("transcribed_text")
    # Make assertions for the emit function as per your implementation.

@patch("handle_audio.transcribe_audio")
@patch("handle_audio.perform_classification")
def test_handle_audio_message_with_empty_audio(mock_perform_classification, mock_transcribe_audio):
    mock_transcribe_audio.return_value = ("transcribed_text", 200)
    mock_perform_classification.side_effect = [["audio_intent1"], []]
    message = {"message": "text_message", "audio": ""}
    handle_audio_message(message)
    mock_transcribe_audio.assert_called_once_with({"audio": ""})
    mock_perform_classification.assert_any_call("text_message")
    mock_perform_classification.assert_any_call("transcribed_text")
    # Make assertions for the emit function as per your implementation.
