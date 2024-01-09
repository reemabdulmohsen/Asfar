from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
from IPython.display import Audio
import soundfile as sf
from datasets import load_dataset
import gtts
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")

speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")


# tokenize the input text
def TTS_input(story):
    save_path = "output_audio.wav"
    # for testing
    # story = "Once upon time, In ancient Bombay, Ali was a merchant who traveled far to bring back silk and spices for the bustling market. His journeys through India's majestic valleys and vast landscapes brought back tales of faraway lands, gorgeous traders, and common folk alike. Despite the dangers, Ali's passion for travel and adventure never waned, and he continued to bring back treasures and stories that would enchant generations."
    inputs = processor(text=story, return_tensors="pt")
    print(inputs["input_ids"].shape)
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
    audio_data = speech[0].numpy()

    # Reshape the array to have two dimensions
    audio_data = speech.squeeze().numpy()
    # Save the audio to a local file
    sf.write(save_path, audio_data, 16000, 'PCM_16')

    audio = Audio(data=speech, rate=16000)


