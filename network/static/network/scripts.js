document.addEventListener("DOMContentLoaded", () => {


    // Set dynamic page height
    if (!document.querySelector('.alert')) {
        document.querySelector('.content').style.height = `calc(100vh - ${document.querySelector('.navbar').offsetHeight}px)`;
    } else {
        document.querySelector('.content').style.height = `calc(100vh - ${document.querySelector('.navbar').offsetHeight}px - ${document.querySelector('.alert').offsetHeight}px)`;
    }

    // Auto fill location input when user types
    new Autocomplete('#autocomplete', {
        search: input => {
            // console.log(input)
            const url = `get_hometown/?search=${input}`
            return new Promise(resolve => {
                fetch(url)
                .then(response => response.json())
                .then(data => {
                    // console.log(data.payload)
                    resolve(data.payload)
                })
            })
        },
    })
})

