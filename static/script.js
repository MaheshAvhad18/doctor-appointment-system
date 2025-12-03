const API_BASE = "https://acclivous-sectorial-towanda.ngrok-free.dev/api";

const hospitalSelect = document.getElementById("hospital");
const doctorSelect = document.getElementById("doctor");
const statusBox = document.getElementById("status");

// -------------------------------------
// LOAD HOSPITALS
// -------------------------------------
fetch(`${API_BASE}/hospitals/`)
    .then(res => res.json())
    .then(data => {

        hospitalSelect.innerHTML = `<option value="">Select hospital</option>`;

        data.forEach(h => {
            hospitalSelect.innerHTML += `
                <option value="${h.id}">${h.name}</option>
            `;
        });

    });


// -------------------------------------
// LOAD DOCTORS WHEN HOSPITAL SELECTED
// -------------------------------------
hospitalSelect.addEventListener("change", () => {

    const hospitalId = hospitalSelect.value;

    doctorSelect.innerHTML = `<option value="">Loading doctors...</option>`;

    if(!hospitalId){
        doctorSelect.innerHTML = `<option value="">Select hospital first</option>`;
        return;
    }

    fetch(`${API_BASE}/doctors/${hospitalId}/`)
        .then(res => res.json())
        .then(data => {

            doctorSelect.innerHTML = `<option value="">Select doctor</option>`;

            data.forEach(d => {
                doctorSelect.innerHTML += `
                    <option value="${d.id}">${d.name}</option>
                `;
            });

        });

});


// -------------------------------------
// BOOK APPOINTMENT
// -------------------------------------
document.getElementById("bookingForm").addEventListener("submit", function(e){

    e.preventDefault();

    statusBox.innerHTML = `<span style="color:#fff;">⏳ Booking appointment...</span>`;

    const payload = {
        patient_name: document.getElementById("patient_name").value,
        patient_phone: document.getElementById("patient_phone").value,
        hospital: hospitalSelect.value,
        doctor: doctorSelect.value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value
    };

    fetch(`${API_BASE}/book/`, {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {

        if(data.token){

            statusBox.innerHTML = `
                <div style="
                    background:rgba(0,255,200,0.15);
                    padding:15px;
                    border-radius:12px;
                    box-shadow:0 0 20px rgba(0,255,200,0.5);
                    color:#ffffff;
                ">
                    ✅ Appointment Confirmed! <br><br>
                    🎟 <b style="font-size:18px;">Your Token: ${data.token}</b>
                </div>
            `;

        } else {

            statusBox.innerHTML = `
                <span style="color:red;">
                    ❌ ${data.error || "Booking failed"}
                </span>
            `;

        }

    })
    .catch(() => {
        statusBox.innerHTML = `<span style="color:red;">❌ Server error</span>`;
    });

});
