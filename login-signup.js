async function submitForm(event) {
  event.preventDefault();

  const formData = new FormData(document.getElementById("form"));
  const data = Object.fromEntries(formData.entries());
  console.log(JSON.stringify(data));
  const url = isSignup ? "http://localhost:8000/signup/" : "http://localhost:8000/login/";

  try {
      const response = await fetch(url, {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
      });

      const result = await response.json();

      if (!response.ok) {
          alert(result.detail);
      } else {
          alert(result.message);
          // Redirect to house price prediction page upon successful login
          window.location.href = "./house-price-prediction.html"; // Adjust URL as needed
      }
  } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
  }
}

function sign_up(event) {
  event.preventDefault();
  isSignup = true;
  document.querySelectorAll('.ul_tabs > li')[0].classList.remove("active");
  document.querySelectorAll('.ul_tabs > li')[1].classList.add("active");
  document.getElementById("confirm_password").style.display = "block";
  document.querySelector('.link_forgot_pass').style.display = "none";
  document.querySelector('.terms_and_cons').style.display = "block";
  document.querySelector('.btn_sign').textContent = "SIGN UP";
}

function sign_in(event) {
  event.preventDefault();
  isSignup = false;
  document.querySelectorAll('.ul_tabs > li')[0].classList.add("active");
  document.querySelectorAll('.ul_tabs > li')[1].classList.remove("active");
  document.getElementById("confirm_password").style.display = "none";
  document.querySelector('.link_forgot_pass').style.display = "block";
  document.querySelector('.terms_and_cons').style.display = "none";
  document.querySelector('.btn_sign').textContent = "SIGN IN";
}

window.onload = function () {
  document.querySelector('.cont_centrar').className = "cont_centrar cent_active";
}
