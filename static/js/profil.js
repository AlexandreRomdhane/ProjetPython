window.onload = () => {
    document.getElementById("btnDeconnect").onclick = () => {
        window.location.replace("logout");
    }

    document.getElementById("btnIndex").onclick = () => {
        window.location.replace("/")
    }
};