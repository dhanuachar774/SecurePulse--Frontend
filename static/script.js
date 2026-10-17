const API_URL = "/api";

const apiStatus = document.getElementById("apiStatus");
const form = document.getElementById("riskForm");
const result = document.getElementById("result");
const button = document.getElementById("checkButton");

async function checkAPI() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (!response.ok) throw new Error("API unavailable");

        const data = await response.json();
        apiStatus.textContent = data.status === "healthy" ? "Online" : "Check API";
    } catch (error) {
        apiStatus.textContent = "Unavailable";
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const heartRate = Number(document.getElementById("heartRate").value);
    const temperature = Number(document.getElementById("temperature").value);

    button.disabled = true;
    button.textContent = "Checking...";
    result.hidden = false;
    result.textContent = "Contacting SecurePulse API...";

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                heart_rate: heartRate,
                temperature: temperature
            })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Prediction request failed");
        }

        document.getElementById("heartDisplay").innerHTML =
            `${data.heart_rate} <small>bpm</small>`;
        document.getElementById("tempDisplay").innerHTML =
            `${data.temperature} <small>°C</small>`;

        result.textContent =
            `Illustrative risk category: ${data.risk_level}. ` +
            `${data.message || "Demo result only."}`;
    } catch (error) {
        result.textContent =
            `Could not reach the API: ${error.message}. Check the server connection.`;
    } finally {
        button.disabled = false;
        button.textContent = "Check Risk";
    }
});

checkAPI();
