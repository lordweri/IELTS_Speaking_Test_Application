document.addEventListener("DOMContentLoaded", () => {
    let mode = "practice";
    let recording = false;

    const practiceModeBtn = document.getElementById("practiceMode");
    const testModeBtn = document.getElementById("testMode");
    const questionElement = document.getElementById("question");
    const startListeningBtn = document.getElementById("button");
    const evaluateBtn = document.getElementById("evaluate");
    const nextQuestionBtn = document.getElementById("next");
    const finishBtn = document.getElementById("finish");

    const resultBlock = document.querySelector(".result-block");
    const evaluationBlock = document.querySelector(".evaluation-block");

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

        practiceModeBtn.classList.toggle("active", mode === "practice");
        testModeBtn.classList.toggle("active", mode === "test");

        if (mode === "practice") {
            evaluateBtn.classList.remove("hidden");
            nextQuestionBtn.classList.add("hidden");
            finishBtn.classList.add("hidden");
            resultBlock.style.display = "block";
            evaluationBlock.style.display = "block";
        } else {
            evaluateBtn.classList.add("hidden");
            nextQuestionBtn.classList.remove("hidden");
            finishBtn.classList.remove("hidden");
            resultBlock.style.display = "none";
            evaluationBlock.style.display = "none";
        }

        changeQuestion();
    }

    practiceModeBtn.addEventListener("click", () => setMode("practice"));
    testModeBtn.addEventListener("click", () => setMode("test"));

    startListeningBtn.addEventListener("click", async () => {
        if (!recording) {
            // Start recording
            recording = true;
            startListeningBtn.textContent = "Stop Listening";

            try {
                await fetch('/start-recording', { method: "POST" });
            } catch (error) {
                console.error("Error starting recording:", error);
                startListeningBtn.textContent = "Start Listening";
                recording = false;
            }

        } else {
            // Stop recording
            recording = false;
            startListeningBtn.textContent = "Start Listening";

            try {
                let response = await fetch('/stop-recording', { method: "POST" });
                let data = await response.json();

                if (data.status === "recording stopped") {
                    let audioFile = data.audio_file;

                    let processResponse = await fetch('/process-audio', {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ audio_file: audioFile })
                    });

                    let processData = await processResponse.json();
                    document.getElementById("result").textContent = processData.transcription;

                    if (mode === "practice") {
                        document.getElementById("evaluation").textContent = `Score: ${processData.score}`;
                        evaluateBtn.classList.remove("hidden");
                    } else {
                        nextQuestionBtn.classList.remove("hidden");
                    }
                }
            } catch (error) {
                console.error("Error stopping recording:", error);
            }
        }
    });

    evaluateBtn.addEventListener("click", () => {
        evaluateBtn.textContent = "Evaluating...";
        setTimeout(() => {
            evaluateBtn.textContent = "Evaluate";
        }, 3000);
    });

    nextQuestionBtn.addEventListener("click", () => {
        if (mode === "test") {
            resultBlock.style.display = "none";
            evaluationBlock.style.display = "none";
            changeQuestion();
            nextQuestionBtn.classList.add("hidden");
        }
    });

    finishBtn.addEventListener("click", () => {
        if (mode === "test") {
            resultBlock.style.display = "block";
            evaluationBlock.style.display = "block";
        }
    });

    setMode("practice");
});
