<script>
	import { browser } from "$app/environment";
	import { goto } from "$app/navigation";
	import { getLoginCount, validateSession } from "../../lib/api";

    let loginCount = 0;
    let user = "";

    if (browser) {
        validateSession().then((res) => {
            if (res.statusCode == 401) {
                localStorage.clear();
                goto("/");
                return
            }

            getLoginCount(res.id).then((resp) => {
                user = resp.username;
                loginCount = resp.loginCount;
            })
        })
    }
</script>

<h1>Login count</h1>
<div>Hello {user}! Your login count is: {loginCount}</div>