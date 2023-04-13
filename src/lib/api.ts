const server = "http://localhost:3000"

export const login = async(user: string, password: string) => {
    const data = {
        username: user,
        password: password
    }

    const result = await fetch(`${server}/auth/login`, {
        method: "POST",
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify(data)
    })

    return await result.json()
}

export const validateSession = async() => {
    const jwt = await getJwt();

    const result = await fetch(`${server}/users/me`, {
        method: "GET",
        headers: {
            'Content-Type': "application/json",
            'Authorization': `Bearer ${jwt}`
        },
        credentials: "include",
    })

    return await result.json()
}

export const getLoginCount = async(id: number) => {
    const jwt = await getJwt();

    const result = await fetch(`${server}/users/logindata/${id}`, {
        method: "GET",
        headers: {
            'Content-Type': "application/json",
            'Authorization': `Bearer ${jwt}`
        },
        credentials: "include",
    })

    return await result.json()
}

const getJwt = async() => {
    return await localStorage.getItem("jwt");
}