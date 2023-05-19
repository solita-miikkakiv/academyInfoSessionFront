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

export const createUser = async(user: string, password: string, isAdmin: Boolean) => {
    const data = {
        username: user,
        password: password,
        isAdmin: isAdmin
    }

    const result = await fetch(`${server}/users/`, {
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

    // const result = await fetch(`${server}/users/me`, {
    //     method: "GET",
    //     headers: {
    //         'Content-Type': "application/json",
    //         'Authorization': `Bearer ${jwt}`
    //     },
    //     credentials: "include",
    // })

    if (jwt !== null) {
        return {
            username: "test_user",
            id: "1234567890",
            isAdmin: true,
            statusCode: 200
        }
    } else {
        return {
            statusCode: 401,
            id: "asdasd"
        }
    }

}

export const getLoginCount = async(id: string) => {
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