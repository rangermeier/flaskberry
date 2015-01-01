if(!window.socket) {
    socket = io.connect('http://' + document.domain + ':' + location.port + socketNamespace);
}

$(document).ready(function(){
    $("a.movie").on("click", function(ev){
        ev.preventDefault()
        var url = moviesUrl + $(this).attr("href")
        socket.emit('play', {
            src: url
        })
    })

    $("#video-controls").append(can.view("#player-controls", statusMap))

    $("#fullscreen").hide()
})
