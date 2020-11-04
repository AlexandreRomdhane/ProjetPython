window.onload = () => {
    document.getElementById("btnProfil").onclick = () => {
        fetch('/api/user')
            .then(response => response.json())
            .then(data => {
                if(!data.errors) {
                    window.location.replace("profil/"+data.username)
                } else {
                    alert(data.message)
                    console.log(data.message)
                }
            })
    }
}