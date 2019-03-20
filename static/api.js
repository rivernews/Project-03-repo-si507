class API {
    static create (endpoint, data) {
        return fetch(endpoint, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then((res) => res.json()).then((parsedRes) => {
            console.log(parsedRes);
            return parsedRes;
        })
        .catch((error) => {
            console.error(error);
        })
    }

    static list(endpoint) {
        return fetch(endpoint, {
            method: 'GET',
        })
        .then((res) => res.json()).then((parsedRes) => {
            console.log(parsedRes);
            return parsedRes;
        })
        .catch((error) => {
            console.error(error);
        });
    }
}