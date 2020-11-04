const refreshPost = (posts) => {
    //post-container
    console.log(posts)
    let postContainerDiv = document.getElementById('post-container')

    if(postContainerDiv.hasChildNodes()) {
        // Supprime tout les posts
        while(postContainerDiv.firstChild) {
            postContainerDiv.removeChild(postContainerDiv.firstChild)
        }
    }

    if(posts.post.length !== 0) {
        for(const post of posts.post) {
            let noPost = document.createElement('p')
            noPost.textContent = "Nom du post : " + post.NomPost + "   Contenu du post : " + post.ContenuPost + "   Date de post : " +  post.DatePost + " ||  "
            postContainerDiv.append(noPost)
        }
    } else {
        let noPost = document.createElement('p')
        noPost.textContent = "Il n'y a aucun post !"

        postContainerDiv.append(noPost)
    }
}

window.onload = () => {
    document.getElementById("btnDeconnect").onclick = () => {
        window.location.replace("/logout");
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
            fetch('/api/post', {
                method: 'post',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if(!data.errors) { // Si il n'y a pas d'erreur
                        // Le post a bien été crée
                        //window.location.reload()
                        fetch('/api/post')
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