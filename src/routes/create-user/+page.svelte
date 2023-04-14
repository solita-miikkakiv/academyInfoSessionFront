<script>
	import { createUser } from "../../lib/api";

    let username = "";
    let password = "";
    let isAdmin = false;
    let error = ""
    let success = false;

    const handleNewUser = () => {
        error = "";
        success = false;
        createUser(username, password, isAdmin).then((res) => {
            if (!res.username) {
                error = "Something went wrong";
            } else {
                [username, password] = "";
                isAdmin = false;
                success = true;
            }
        })
    }
</script>

<h1>Create new user</h1>
<form class="loginform">
    <input type="text" placeholder="Username" bind:value={username}>
    <input type="password" placeholder="Password" bind:value={password}>
    <div class="checkbox-row">
        <input name="checkbox" type="checkbox" bind:checked={isAdmin}>
        <label for="checkbox">Is admin?</label>
    </div>
    <button on:click={handleNewUser}>Create</button>
</form>
<div class="error">{error}</div>
{#if success}
    <div class="success">Success!</div>
{/if}
<a href="/">Login</a>

<style>
    .loginform {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .checkbox-row {
        display: flex;
        flex-direction: row;
    }

    input {
        margin-bottom: 1rem;
    }

    .error {
        color: red;
        margin-top: 1rem;
    }

    .success {
        color: greenyellow;
        margin-top: 1rem;
    }
</style>