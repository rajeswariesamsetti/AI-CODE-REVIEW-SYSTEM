async function login(){

let email = document.getElementById("email").value
let password = document.getElementById("password").value

let response = await loginAPI({
email:email,
password:password
})

document.getElementById("message").innerText = response.message

if(response.message === "Login successful"){
window.location.href="dashboard.html"
}

}