const form = document.getElementById("prediction-form");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const resultBox = document.getElementById("result-box");

    resultBox.style.display = "block";
    resultBox.className = "";
    resultBox.innerText = "Running prediction...";

    const payload = {

        location: document.getElementById("location").value,

        total_sqft: document.getElementById("total_sqft").value,

        bhk: document.getElementById("bhk").value,

        bath: document.getElementById("bath").value,

        balcony: document.getElementById("balcony").value

    };

    try{

        const response = await fetch("/predict", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(payload)

        });

        const data = await response.json();

        if(data.success){

            resultBox.classList.add("success");

            resultBox.innerText =
                `Estimated Price : ₹ ${data.predicted_price>0 ? data.predicted_price : "Property does not meet our predicting criteria"} Lakhs`;

        }
        else{

            resultBox.classList.add("error");

            resultBox.innerText =
                data.error || "Prediction failed.";

        }

    }
    catch(error){

        resultBox.classList.add("error");

        resultBox.innerText =
            "Unable to connect to backend server.";

    }

});