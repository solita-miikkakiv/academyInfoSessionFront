<script>
	import { browser } from "$app/environment";
	import { goto } from "$app/navigation";
	import { login } from "../lib/api";
	import { session } from "../store/session";

    let username = "";
    let password = "";
    let error = ""

    const handleLogin = () => {
        //  just simulate login
        if (username === "test_user" && password === "secret") {
            const access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6InRlc3RfdXNlciIsImlhdCI6MTUxNjIzOTAyMn0.4AwOuCRrzIseAuLiHjmDj994w-fwAxcol68pU06WsHg"
            localStorage.setItem("jwt", access_token)
            session.set(access_token)
            setTimeout(() => goto('/dashboard'), 0);
            console.log('login success')
        } else {
            error = "Invalid username or password"
        }
        // login(username, password).then((res) => {
        //     if (res.statusCode == 401) {
        //         error = "Invalid username or password";
        //     } else if (res.access_token) {
        //         localStorage.setItem("jwt", res.access_token);
        //         session.set(res.access_token);
        //         goto("/dashboard");
        //     }
        // })
    }
</script>

<h1>Login</h1>
<form class="loginform">
    <input type="text" id="username" placeholder="Username" bind:value={username}>
    <input type="password" id="password" placeholder="Password" bind:value={password}>
    <button on:click={handleLogin} id="login-button">Login</button>
</form>
<div class="error">{error}</div>
<a href="/create-user">Create new user</a>

<style>
    .loginform {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    input {
        margin-bottom: 1rem;
    }

    .error {
        color: red;
        margin-top: 1rem;
    }
</style>