var $player, player

function sendStatus() {
    var data = {
        src: player.src,
        paused: player.paused,
        currentTime: player.currentTime.toFixed(2),
        duration: player.duration.toFixed(2),
        volume: player.volume,
        muted: player.muted
    }
    socket.emit('update status', data)
}

function setPlayer(data){
    if(data.src && player.src !== data.src) {
        player.src = data.src
        player.load()
        player.play()
    }
    if(data.paused !== undefined) {
        if(data.paused) {
            player.pause()
        } else {
            player.play()
        }
    }
    $.each(["currentTime", "volume", "muted"], function(i, prop){
        if(data[prop] !== undefined) {
            player[prop] = data[prop]
        }
    })
}

/* SocketIO listeners */
if(!window.socket) {
    socket = io.connect('http://' + document.domain + ':' + location.port + socketNamespace)
}
socket.on('connect', function() {
    socket.emit('register consumer', {})
})
socket.on('play', setPlayer)

$(document).ready(function(){
    $player = $("#player")
    player= $player.get(0)

    var lastUpdate
    $player
        .on("play", sendStatus)
        .on("pause", sendStatus)
        .on("timeupdate", function(){
            var now = + new Date()
            if(!lastUpdate || (lastUpdate + 1000) < now ){
                lastUpdate = now
                sendStatus()
            }
        })

    $("#video-controls").append(can.view("#player-controls", statusMap))
})
