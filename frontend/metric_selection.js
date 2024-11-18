const steps = document.querySelectorAll(".step");
const progressLine = document.querySelector(".progress-line");
let currentStep = 0;

function updateProgress() {
    // Update progress line width
    const progressWidth = (currentStep / (steps.length - 1)) * 100;
    progressLine.style.width = `${progressWidth}%`;

    // Update active steps
    steps.forEach((step, index) => {
        if (index <= currentStep) {
            step.classList.add("active");
        } else {
            step.classList.remove("active");
        }
    });
}

function nextStep() {
    if (currentStep < steps.length - 1) {
        currentStep++;
        updateProgress();
    }
}

function prevStep() {
    if (currentStep > 0) {
        currentStep--;
        updateProgress();
    }
}

// Initialize progress on page load
updateProgress();
