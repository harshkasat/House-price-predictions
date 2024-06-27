async function submitForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById("prediction-form"));
    const data = Object.fromEntries(formData.entries());
    const response = await fetch("http://localhost:8000/predict/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        const result = await response.json();
        const predictionResult = document.getElementById("prediction-result");
        predictionResult.innerHTML = `<p>Predicted Price: ${result.predicted_price}</p>`;
    } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
    }
}
