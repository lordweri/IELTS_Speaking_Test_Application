document.addEventListener("DOMContentLoaded", () => {
    let mode = "practice";
    
    const practiceModeBtn = document.getElementById("practiceMode");
    const testModeBtn = document.getElementById("testMode");
    const questionElement = document.getElementById("question");
    const startListeningBtn = document.getElementById("startListening");
    const evaluateBtn = document.getElementById("evaluate");
    const nextQuestionBtn = document.getElementById("nextQuestion");
    
    const part1Section = document.getElementById("part1");
    const part2Section = document.getElementById("part2");
    const part3Section = document.getElementById("part3");

    const questions = [
        "Describe a book you recently read.",
        "Talk about your favorite movie from childhood.",
        "Describe a memorable school event."
    ];

    function changeQuestion() {
        questionElement.textContent = questions[Math.floor(Math.random() * questions.length)];
    }

    function setMode(selectedMode) {
        mode = selectedMode;
        if (mode === "practice") {
            evaluateBtn.classList.remove("hidden");
            nextQuestionBtn.classList.add("hidden");
        } else {
            evaluateBtn.classList.add("hidden");
            nextQuestionBtn.classList.remove("hidden");
        }
        changeQuestion();
    }

    practiceModeBtn.addEventListener("click", () => setMode("practice"));
    testModeBtn.addEventListener("click", () => setMode("test"));

    startListeningBtn.addEventListener("click", () => {
        startListeningBtn.textContent = "Recording...";
        setTimeout(() => {
            startListeningBtn.textContent = "Start Listening";

            // Call /start-recording route to start audio recording
            fetch('/start-recording', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    console.log(data); // Handle the success response
                    // You can also handle the audio file here
                })
                .catch(error => {
                    console.error('Error:', error);
                });

            if (mode === "practice") {
                evaluateBtn.classList.remove("hidden");
            } else {
                nextQuestionBtn.classList.remove("hidden");
            }
        }, 5000);
    });


    evaluateBtn.addEventListener("click", () => {
        evaluateBtn.textContent = "Evaluating...";

        const audioFile = "audio.wav"; 
        
        fetch('/process-audio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audio_file: audioFile })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); 
            evaluateBtn.textContent = "Evaluate"; 
        })
        .catch(error => {
            console.error('Error:', error);
        });

        setTimeout(() => {
            evaluateBtn.textContent = "Evaluate";
        }, 3000);
    });


    nextQuestionBtn.addEventListener("click", () => {
        if (mode === "test") {
            const audioFile = "audio.wav";  
            fetch('/process-audio', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ audio_file: audioFile })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); 
                changeQuestion();
                nextQuestionBtn.classList.add("hidden"); 
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            changeQuestion();
            nextQuestionBtn.classList.add("hidden"); 
        }
    });
    
    // PART 2
    const startTimerBtn = document.getElementById("startTimer");
    const timerElement = document.getElementById("timer");
    const timeLeftSpan = document.getElementById("timeLeft");
    let timer = 60;

    startTimerBtn.addEventListener("click", () => {
        timerElement.classList.remove("hidden");
        startTimerBtn.classList.add("hidden");
        const interval = setInterval(() => {
            timeLeftSpan.textContent = `${timer} seconds`;
            timer--;
            if (timer < 0) {
                clearInterval(interval);
                document.getElementById("startListeningPart2").classList.remove("hidden");
            }
        }, 1000);
    });

    document.getElementById("nextPart").addEventListener("click", () => {
        part1Section.classList.add("hidden");
        part2Section.classList.remove("hidden");
    });

    document.getElementById("finish").addEventListener("click", () => {
        alert("Test Completed!");
    });

    changeQuestion();
});