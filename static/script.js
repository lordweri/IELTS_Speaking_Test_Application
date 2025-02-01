document.addEventListener("DOMContentLoaded", () => {
    let mode = "practice";
    let recording = false;
    let audioFile = "";
    let questionIndex = 0;
    let questions = [];
    let conversations = [];



    const practiceModeBtn = document.getElementById("practiceMode");
    const testModeBtn = document.getElementById("testMode");
    const questionElement = document.getElementById("question");
    const startListeningBtn = document.getElementById("button");
    const evaluateBtn = document.getElementById("evaluate");
    const nextQuestionBtn = document.getElementById("next");
    const finishBtn = document.getElementById("finish");
    const newQuestionBtn = document.getElementById("newQuestion");
    const resultBlock = document.querySelector(".result-block");
    const evaluationBlock = document.querySelector(".evaluation-block");
    const startBtn = document.getElementById("start-btn");
    const downloadBtn = document.getElementById("download-btn");

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function changeQuestion() {
        fetch('/practice-question')
            .then(response => response.json())
            .then(data => {
                questionElement.textContent = data.question;
            })
            .catch(error => {
                console.error("Error fetching question:", error);
            });
    }

    function partChangeQuestion() {
        fetch('/part-question')
            .then(response => response.json())
            .then(data => {
                questions = data.questions; 
                questionElement.textContent = questions[questionIndex];
                conversations.push(questions[questionIndex]);
            })
            .catch(error => console.error('Error fetching questions:', error));
    }


    function setMode(selectedMode) {
        mode = selectedMode;
        testPart = 1; 
        questionCount = 0;

        practiceModeBtn.classList.toggle("active", mode === "practice");
        testModeBtn.classList.toggle("active", mode === "test");

        const part1Header = document.querySelector("#part1 h2");
        part1Header.style.display = mode === "practice" ? "none" : "block"

        if (mode === "practice") {
            questionElement.textContent = ""
            changeQuestion();
            evaluateBtn.classList.remove("hidden");
            nextQuestionBtn.classList.add("hidden");
            newQuestionBtn.classList.remove("hidden");
            finishBtn.classList.add("hidden");
            resultBlock.style.display = "block";
            evaluationBlock.style.display = "block";
            startBtn.classList.add("hidden");
            downloadBtn.classList.remove("hidden");
        } else {
            evaluateBtn.classList.add("hidden");
            nextQuestionBtn.classList.add("hidden");
            newQuestionBtn.classList.add("hidden");
            resultBlock.style.display = "none";
            evaluationBlock.style.display = "none";
            questionElement.textContent = "Press Start To Begin";
            startBtn.classList.remove("hidden");
            startListeningBtn.classList.add("hidden");
            downloadBtn.classList.add("hidden");
        }

    }

    practiceModeBtn.addEventListener("click", () => setMode("practice"));
    testModeBtn.addEventListener("click", () => setMode("test"));

    newQuestionBtn.addEventListener("click", () => {
        questionElement.textContent = "";
        changeQuestion();
    });
    
    startListeningBtn.addEventListener("click", async () => {
        if (!recording) {
            // Clear previous speech & evaluation only when starting a new recording
            document.getElementById("transcription").textContent = "";
            document.getElementById("evaluation").textContent = "";
    
            // Start recording
            recording = true;
            startListeningBtn.textContent = "Stop Listening";
            startListeningBtn.classList.remove("start-listening");
            startListeningBtn.classList.add("recording");
    
            try {
                await fetch('/start-recording', { method: "POST" });
            } catch (error) {
                console.error("Error starting recording:", error);
                startListeningBtn.textContent = "Start Listening";
                startListeningBtn.classList.remove("recording");
                startListeningBtn.classList.add("start-listening");
                recording = false;
            }
        } else {
            // Stop recording
            recording = false;
            startListeningBtn.textContent = "Start Listening";
            startListeningBtn.classList.remove("recording");
            startListeningBtn.classList.add("start-listening");
    
            try {
                let response = await fetch('/stop-recording', { method: "POST" });
                let data = await response.json();
    
                if (data.status === "recording stopped") {
                    audioFile = data.audio_file;
    
                    let processResponse = await fetch('/process-audio', {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ audio_file: audioFile })
                    });
    
                    let processData = await processResponse.json();
                    document.getElementById("transcription").textContent = processData.transcription;

                    if (mode === "test") {
                        conversations.push(processData.transcription);
                    }

                    if (mode === "practice") {
                        finishBtn.classList.add("hidden");
                    } else {
                        nextQuestionBtn.classList.remove("hidden");
                    }
                }
            } catch (error) {
                console.error("Error stopping recording:", error);
            }
        }
    });
    
    evaluateBtn.addEventListener("click", async () => {
        evaluateBtn.textContent = "Evaluating..."; // Show evaluating text
    
        try {
            // Get the question and transcription from the UI
            let question = document.getElementById("question").textContent;
            let transcription = document.getElementById("transcription").textContent;
    
            let processResponse = await fetch('/evaluate-response', {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: question, transcription: transcription }) // Send correct data
            });
    
            let processData = await processResponse.json();
    
            // Check if evaluation exists in response
            if (processData.evaluation) {
                document.getElementById("evaluation").innerHTML = processData.evaluation;
            } else {
                document.getElementById("evaluation").textContent = "Error: No evaluation received.";
            }
    
        } catch (error){
            console.error("Error during evaluation:", error);
            document.getElementById("evaluation").textContent = "Error. Try again!";
        }
    
        // Revert button text after the process is complete
        setTimeout(() => {
            evaluateBtn.textContent = "Evaluate";
        }, 3000);
    });
    
    nextQuestionBtn.addEventListener("click", () => {
        if (mode === "test") { 
            if (questionIndex < 6) { 
                questionIndex++; // Go to next question
                questionElement.textContent = questions[questionIndex];
                conversations.push(questions[questionIndex]);
                console.log("Response:", conversations);
            } else { 
                questionElement.textContent = "Click Finish to see your results!";
                finishBtn.classList.remove("hidden");
                startListeningBtn.classList.add("hidden");
                nextQuestionBtn.classList.add("hidden");
                downloadBtn.classList.remove("hidden");

 
            }
        }
    });
    
    finishBtn.addEventListener("click", async () => {
        if (mode === "test") {
            try {
                // Show loading state
                finishBtn.disabled = true;
                finishBtn.textContent = "Analyzing...";

                console.log("Sending conversations:", conversations);  
    
                // Send the conversations list to the backend
                const response = await fetch('/analyze-response', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ conversations: conversations })
                });
    
                const data = await response.json();
    
                if (data.feedback) {
                    // Display the feedback
                    document.getElementById("evaluation").innerHTML = data.feedback;
                    evaluationBlock.style.display = "block";
                } else if (data.error) {
                    // Display the error message
                    document.getElementById("evaluation").textContent = data.error;
                }
            } catch (error) {
                console.error("Error analyzing response:", error);
                document.getElementById("evaluation").textContent = "Error analyzing response. Please try again.";
            } finally {
                // Reset the button
                finishBtn.classList.add("hidden");
            }
        }
    });

    startBtn.addEventListener("click", () => {
        if (mode === "test") {
            startBtn.classList.add("hidden");
            nextQuestionBtn.classList.remove("hidden");
            startListeningBtn.classList.remove("hidden"); 
            partChangeQuestion();
        }
    });
    downloadBtn.addEventListener("click", function () {
        const { jsPDF } = window.jspdf; 
        const doc = new jsPDF();

        const feedback = document.getElementById("evaluation").innerText;

        doc.setFont("helvetica", "bold");
        doc.setFontSize(18);
        doc.text("IELTS Speaking Test Feedback", 10, 10);
    

        doc.setFont("helvetica", "normal");
        doc.setFontSize(12);
        let y = 20;


        const lines = doc.splitTextToSize(feedback, 180);
        lines.forEach(line => {
            doc.text(line, 10, y);
            y += 7;
        });
        doc.save("IELTS_Feedback.pdf");
    });
    

    setMode("practice");
});
