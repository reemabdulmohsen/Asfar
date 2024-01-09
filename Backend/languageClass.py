# import torchaudio
from speechbrain.pretrained import EncoderClassifier
import tensorflow as tf
import tensorflow_io as tfio

language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")


def classify_audio(path):
    signal = language_id.load_audio(path)
    prediction = language_id.classify_batch(signal)
    predicted_language = prediction[-1]
    language = predicted_language[0].split(': ')[1]

    country = 'other'
    if language == "English":
        country = 'United States'
    elif language == "Chinese":
        country = 'China'
    elif language == "Hindi":
        country = 'India'
    else:
        country = 'other'

    return country


def reshape(filename):
    file_contents = tf.io.read_file(filename)
    wav, sample_rate = tf.audio.decode_wav(file_contents, desired_channels=1)
    # Removes trailing axis
    wav = tf.squeeze(wav, axis=-1)
    sample_rate = tf.cast(sample_rate, type=tf.int64)
    # Goes from 44100Hz to 16000hz - amplitude of the audio signal
    wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=16000)
    print(wav)
    return wav
