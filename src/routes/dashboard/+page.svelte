<script lang="ts">
	import { browser } from "$app/environment";
	import { goto } from "$app/navigation";
	import { validateSession } from "../../lib/api";

    let username = "";
    let isAdmin = false;

    const handleLogout = () => {
        localStorage.clear();
        goto("/");
    }

    if (browser) {
        validateSession().then((res) => {
            if (res.statusCode == 401) {
                goto("/");
                return;
            }

            username = res?.username!;
            isAdmin = res?.isAdmin!;
        })
    }
</script>

<h1>Dashboard</h1>
<div id="welcome">Welcome {username}</div>
<div><a href="/logincount">Login Count</a></div>
<div><button on:click={handleLogout}>Logout</button></div>
{#if isAdmin}
    <div>
        <button class="nukebutton">Drop nukes or smth</button>
    </div>
{/if}

<style>
    div {
        margin-top: 1rem;
    }

    .nukebutton {
        padding: 3rem;
        border-radius: 10px;
        background-color: red;
        font-size: 2rem;
    }
</style>