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
    //TODO Rajkouter une row
    //Header
    let divPost = document.createElement('div')
    divPost.className = 'col-md-12'
    postContainerDiv.append(divPost)
    //
    let divRowHeaderPost = document.createElement('div')
    divRowHeaderPost.className = 'row'
    divPost.append(divRowHeaderPost)
    //
    let divHeaderPost = document.createElement('div')
    divHeaderPost.className = 'col-md-12'
    divRowHeaderPost.append(divHeaderPost)
    //
    let nomPost = document.createElement('h4')
    nomPost.className = 'text-primary'
    nomPost.textContent = post.NomPost
    divHeaderPost.append(nomPost)
    //Fin header
    //Contenu
    let divRowContentPost = document.createElement('div')
    divRowContentPost.className = 'row'
    divPost.append(divRowContentPost)
    //
    let divContentLeftPost = document.createElement('div')
    divContentLeftPost.className = 'col-md-6'
    divRowContentPost.append(divContentLeftPost)
    //
    let contentPost = document.createElement('p')
    contentPost.textContent = post.ContenuPost
    divContentLeftPost.append(contentPost)
    //
    let divContentRightPost = document.createElement('div')
    divContentRightPost.className = 'col-md-6'
    divRowContentPost.append(divContentRightPost)
    //
    let btnDelete = document.createElement('button')
    btnDelete.type = "button"
    btnDelete.innerHTML = "Supprimer"
    btnDelete.className = "btn btn-outline-primary"
    //
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
    divContentRightPost.append(btnDelete)
    //Fin contenu
    //Date
    let divRowFooterPost = document.createElement('div')
    divRowFooterPost.className = 'row'
    divPost.append(divRowFooterPost)
    //
    let divFooterPost = document.createElement('div')
    divFooterPost.className = 'col-md-12'
    divRowFooterPost.append(divFooterPost)
    //
    let dateFooterPost = document.createElement('p')
    //dateFooterPost.textContent = post.DatePost.toLocaleString()
    const date = new Date(post.DatePost)
    dateFooterPost.textContent = 'Posté le '+date.toLocaleString()
    divFooterPost.append(dateFooterPost)
    //Fin date
}

const getPost = () => {
    return fetch('/api/post')
        .then(response => {
            return response.json()
        })
}

window.onload = () => {
    refreshPost()
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