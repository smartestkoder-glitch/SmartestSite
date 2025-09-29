


async function create() {
    const form = document.querySelector('#create-form');
    const data = new FormData(form);
    fetch('/create', {
        method: 'POST',
        body: data
    })
        .then(res => {
            if (res.redirected) {
                window.location.href = res.url;
            }
        });


}