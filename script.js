
const API_URL = "http://127.0.0.1:8000/api";

const apiStatus = document.getElementById("apiStatus");
const predictBtn = document.getElementById("predictBtn");
const result = document.getElementById("result");

async function checkAPI() {
    try {
        const response = await fetch(`${API_URL}/health`);

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        const data = await response.json();
        apiStatus.textContent = data.status === "healthy"
            ? "Online"
            : "Unavailable";
    } catch (error) {
        apiStatus.textContent = "Offline";
    }
}

predictBtn.addEventListener("click", async () => {
    const heartRate = Number(
        document.getElementById("heartRate").value
    );

    const temperature = Number(
        document.getElementById("temperature").value
    );

    if (
        !Number.isFinite(heartRate) ||
        !Number.isFinite(temperature) ||
        heartRate < 30 ||
        heartRate > 220 ||
        temperature < 30 ||
        temperature > 45
    ) {
        result.textContent =
            "Please enter valid values within the displayed ranges.";
        return;
    }

    predictBtn.disabled = true;
    predictBtn.textContent = "Analyzing...";
    result.textContent = "Connecting to SecurePulse API...";

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                heart_rate: heartRate,
                temperature: temperature
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Prediction request failed.");
        }

        result.textContent =
            `Demo Risk Level: ${data.risk_level}. ` +
            (data.message || data.note || "Illustrative result only.");
    } catch (error) {
        result.textContent =
            "Could not connect to the API. Make sure the SecurePulse backend is running.";
    } finally {
        predictBtn.disabled = false;
        predictBtn.textContent = "Analyze Demo Risk";
    }
});

checkAPI();
