const refreshPost = (posts) => {

}

window.onload = () => {
    document.getElementById("btnDeconnect").onclick = () => {
        window.location.replace("logout");
    }

    document.getElementById("btnIndex").onclick = () => {
        window.location.replace("/")
    }

    document.getElementById("btnPoster").onclick = () => {
        let namePost = document.getElementById("namePost").value
        let contentPost = document.getElementById("contentPost").value
        if(namePost.length != 0 && contentPost.length != 0) {
            let formData = new FormData()
            formData.append('namePost', namePost)
            formData.append('contentPost', contentPost)
            fetch('post', {
                method: 'post',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if(data.error) {
                        // Le post a bien été crée
                        //window.location.reload()
                        fetch('post')
                            .then(response => response.json())
                            .then(data => refreshPost(data))
                        document.getElementById("namePost").value = ""
                        document.getElementById("contentPost").value = ""
                    }
                })
                .catch(error => console.error(error))
        }
    }
}