document.addEventListener('DOMContentLoaded', () => {

    getImage();


    
});


function getImage(){

    
    const detectedCountry = localStorage.getItem('detectedCountry');
    if(detectedCountry == 'other'){
        render('index.html')
    }
    document.body.style.background = 'black';

    // Update the country flag image source based on the detected country
    const countryFlag = document.getElementById('countryFlag');
    const countryMassg = document.getElementById('welcomeCountry');
    countryMassg.innerHTML = "Welcome to our virtual journey through the rich tapestry of Saudi and "+ detectedCountry+" history. While you wait patiently, we prepare an immersive experience that unveils the fascinating stories that connect our two countries. Your adventure will begin soon – thank you for joining us on this cultural experience!" ;
    
    if(detectedCountry=='United States'){
        countryFlag.innerHTML = '🇺🇸'
    }else if (detectedCountry == 'China'){
        countryFlag.innerHTML = '🇨🇳'
    }else if (detectedCountry == 'India'){
        countryFlag.innerHTML = '🇮🇳'
    }
    fetch('http://localhost:2333/image?country_name='+detectedCountry)
    .then(response => response.json())  // Parse the response as JSON
    .then(data => {
        // Replace loading message with the retrieved image
        const loadingContainer = document.getElementById('container');
        countryFlag.remove();
        countryMassg.remove();
       
        
        // Create an image element
        const imgElement = document.createElement('img');
        // Set the source of the image using the base64-encoded data and MIME type
        imgElement.src = `data:${data.mime_type};base64,${data.image}`;
        imgElement.alt = 'Detected Image';
        // Append the image element to the container
        loadingContainer.appendChild(imgElement);

        getAudio();

    })
    .catch(error => {
        console.error('Error fetching image from backend:', error);
    });

}

function getAudio(){
    const audioPlayer = document.getElementById('audioPlayer');

    // Fetch the audio file from the backend
    fetch('http://localhost:2333/story')
    .then(response => response.blob())
    .then(blob => {
        
        const audioUrl = URL.createObjectURL(blob);
        audioPlayer.src = audioUrl;
        
        
    })
    .catch(error => console.error('Error fetching audio:', error));

}