let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// Voice recording functionality
document.getElementById('recordButton').addEventListener('click', async function() {
    const recordButton = this;
    const recordingStatus = document.getElementById('recordingStatus');

    if (!isRecording) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioChunks = [];
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                recordingStatus.textContent = 'Transcribing...';

                // Create form data with the audio file
                const formData = new FormData();
                formData.append('file', audioBlob, 'recording.webm');

                try {
                    const response = await fetch('/transcribe', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();
                    document.getElementById('query').value = data.text;
                    recordingStatus.textContent = '';
                } catch (error) {
                    console.error('Transcription error:', error);
                    recordingStatus.textContent = 'Error during transcription';
                }

                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            });

            mediaRecorder.start();
            isRecording = true;
            recordButton.textContent = '⏹ Stop Recording';
            recordButton.classList.add('recording');
            recordingStatus.textContent = 'Recording...';
        } catch (err) {
            console.error('Error accessing microphone:', err);
            recordingStatus.textContent = 'Error: Could not access microphone';
        }
    } else {
        mediaRecorder.stop();
        isRecording = false;
        recordButton.textContent = '🎤 Start Recording';
        recordButton.classList.remove('recording');
    }
});

// Existing form submission logic
document.getElementById('queryForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    fetch('/extract', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('departureAirport').value = data.departure_airport;
        document.getElementById('destinationAirport').value = data.destination_airport;
        document.getElementById('departureDate').value = data.departure_date;
        document.getElementById('returnDate').value = data.return_date;
        document.getElementById('airline').value = data.airlines.join(', ');
        document.getElementById('class').value = data.booking_class;
        document.getElementById('numberOfPersons').value = data.number_of_persons;
        document.getElementById('responseForm').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
