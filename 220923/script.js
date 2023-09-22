async function getProduct(id) {
    await fetch(`https://dummyjson.com/products/${id}`)
    .then((response) => response.json())
        .then((json) => {
            console.log(json);
            respjson.innerHTML = imprime(json);
        });
    }