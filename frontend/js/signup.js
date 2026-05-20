async function signup(){

let username = document.getElementById("username").value
let email = document.getElementById("email").value
let password = document.getElementById("password").value

let response = await signupAPI({
username:username,
email:email,
password:password
})

document.getElementById("message").innerText = response.message
if(response.message === "User registered"){
    setTimeout(() => {
        window.location.href="login.html";
    }, 1500);
}
}