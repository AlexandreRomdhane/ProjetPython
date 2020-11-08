const refreshPost = () => {
    //post-container
    getPost() // A terme rechercher avec le nom d'utilisateur
        .then(posts => {
            let postContainerDiv = document.getElementById('post-container')

            if (postContainerDiv.hasChildNodes()) {
                // Supprime tout les posts
                while (postContainerDiv.firstChild) {
                    postContainerDiv.removeChild(postContainerDiv.firstChild)
                }
            }

            if (posts.post.length !== undefined) {
                for (const post of posts.post) {
                    createPostHTML(post)
                }
            } else {
                let noPost = document.createElement('p')
                noPost.textContent = "Il n'y a aucun post !"

                postContainerDiv.append(noPost)
            }
        })
}

const createPostHTML = (post) => {
    let postContainerDiv = document.getElementById('post-container')
    let noPost = document.createElement('p')
    noPost.textContent = "Nom du post : " + post.NomPost + "   Contenu du post : " + post.ContenuPost + "   Date de post : " +  post.DatePost + " ||  "
    postContainerDiv.append(noPost)

    let btnDelete = document.createElement('button')
    btnDelete.type = "button"
    btnDelete.innerHTML = "Supprimer"
    btnDelete.className = "btn btn-outline-primary"

    btnDelete.onclick = () => {
        let formData = new FormData()
        formData.append('postID', post.PostID)
        fetch('/api/post', {
            method: 'delete',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if(!data.errors) {
                    //alert(data.message)
                    refreshPost()
                } else {
                    alert(data.message)
                }
            })
    }

    postContainerDiv.append(btnDelete)
}

const getPost = () => {
    return fetch('/api/post')
        .then(response => {
            return response.json()
        })
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