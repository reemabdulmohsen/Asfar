
function changeLanguage() {
    // Example: change the language of the welcome message and secondary message
    var welcomeLanguages = ['Welcome to the Kingdom of Saudi Arabia', 'सऊदी अरब साम्राज्य में आपका स्वागत है', '欢迎来到沙特阿拉伯王国'];
    var secondaryLanguages = ['Talk to me in your language...', 'अपनी भाषा में मुझसे बात करें...', '用您的语言与我交谈...'];

    var currentWelcomeLanguage = welcomeMessage.textContent.trim();
    var currentSecondaryLanguage = secondaryMessage.textContent.trim();

    var nextWelcomeLanguage = welcomeLanguages[(welcomeLanguages.indexOf(currentWelcomeLanguage) + 1) % welcomeLanguages.length];
    var nextSecondaryLanguage = secondaryLanguages[(secondaryLanguages.indexOf(currentSecondaryLanguage) + 1) % secondaryLanguages.length];

    // Apply fade-out animation to both welcome message and secondary message
    welcomeMessage.classList.add('fade-out');
    secondaryMessage.classList.add('fade-out');

    // After the fade-out animation completes, update the text and apply fade-in animation for both messages
    setTimeout(function () {
        welcomeMessage.textContent = nextWelcomeLanguage;
        secondaryMessage.textContent = nextSecondaryLanguage;

        welcomeMessage.classList.remove('fade-out');
        welcomeMessage.classList.add('fade-in');

        secondaryMessage.classList.remove('fade-out');
        secondaryMessage.classList.add('fade-in');
    }, 1000); // Assuming the fade-out animation duration is 1 second
}

console.log('test');
document.addEventListener('DOMContentLoaded', () => {
    console.log('test');

	setInterval(changeLanguage, 3000);


    const recordButton = document.getElementById('recordButton');
	


    let isRecording = false;
    let gumStream;
    let recorder;
    let audioChunks = [];


    recordButton.addEventListener('click', start);
    //stopButton.addEventListener('click', stopRecording);

	function start(){
		if(recordButton.innerHTML=="Start Recording"){
            console.log('httl')
			startRecording()
            
		} else {
            console.log(recordButton.innerHTML)
			stopRecording()
		}
	}

    function startRecording() {
        console.log("startRecording() called");

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then((stream) => {
                gumStream = stream;
                audioContext = new AudioContext();
                input = audioContext.createMediaStreamSource(stream);

                recorder = new WebAudioRecorder(input, {
                
                    workerDir: "js/",
                    encoding: "wav",
                    numChannels: 1,
                    onEncoderLoading: function (recorder, encoding) {
                        console.log("Loading " + encoding + " encoder...");
                    },
                    onEncoderLoaded: function (recorder, encoding) {
                        console.log(encoding + " encoder loaded");
                    }
                });

                recorder.onComplete = function (recorder, blob) {
                    console.log("Encoding complete");
                    sendAudioToBackend(blob);
                };

                recorder.setOptions({
                
                    timeLimit: 4,
                    encodeAfterRecord: true,
                    ogg: { quality: 0.5 },
                    mp3: { bitRate: 160 }
                });

                recorder.startRecording();
                console.log("Recording started");
            })
            .catch((error) => {
                console.error('Error accessing microphone:', error);
            });
			recordButton.innerHTML = "Stop Recording";
			document.querySelector('.wrapper').classList.add('recording');
			
		   
    }

    function stopRecording() {
        console.log("stopRecording() called");

        gumStream.getAudioTracks()[0].stop();

        recorder.finishRecording();
        console.log('Recording stopped');
		recordButton.innerHTML = "Start Recording";
		document.querySelector('.wrapper').classList.remove('recording');
    }

    function sendAudioToBackend(blob) {
        const formData = new FormData();
        formData.append('file', blob, 'recording.wav');

        fetch('http://localhost:2333/upload_audio', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                console.log('Audio sent to backend:', data);
				const detectedCountry = data.detected_country;
				
				localStorage.setItem('detectedCountry', detectedCountry);
				// Redirect to the loading page with the detected country information
				window.location.href = `loading.html?country=${detectedCountry}`;
            })
            .catch(error => {
                console.error('Error sending audio to backend:', error);
            });

		
    }
	
});
