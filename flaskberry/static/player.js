var $player, player

var sendStatus = function() {
    var data = {
        nowPlaying: player.src,
        paused: player.paused,
        currentTime: player.currentTime.toFixed(2),
        duration: player.duration.toFixed(2),
        volume: player.volume,
        muted: player.muted
    }
    socket.emit('update status', data)
}

/* SocketIO listeners */
var socket = io.connect('http://' + document.domain + ':' + location.port + socketNamespace);
socket.on('connect', function() {
    socket.emit('register consumer', {})
})
socket.on('play', function(data){
    if(data.url) {
        $player.attr("src", data.url)
        player.load()
        player.play()
    } else if(data.toggle) {
        if(player.paused) {
            player.play()
        } else {
            player.pause()
        }
    }
    $.each(["currentTime", "volume", "muted"], function(i, prop){
        if(data[prop] !== undefined) {
            player[prop] = data[prop]
        }
    })
})

$(document).ready(function(){
    $player = $("#player")
    player= $player.get(0)

    $player
        .on("play", sendStatus)
        .on("pause", sendStatus)
        .on("timeupdate", sendStatus)
})
