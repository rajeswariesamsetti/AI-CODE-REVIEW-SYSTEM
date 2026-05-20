const API_URL = "http://127.0.0.1:5000";

async function signupAPI(data){

let res = await fetch(API_URL + "/signup",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify(data)
})

return res.json()

}

async function loginAPI(data){

let res = await fetch(API_URL + "/login",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify(data)
})

return res.json()

}

async function reviewAPI(code){

let res = await fetch(API_URL + "/review",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({code:code})
})

return res.json()

}