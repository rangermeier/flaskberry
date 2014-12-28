var m_status = {}

var movieClicked = function(ev) {
    ev.preventDefault()
    var url = moviesUrl + $(this).attr("href")
    if(!!m_status.consumers) {
        socket.emit('play', {
            url: url
        })
    } else {
        window.scrollTo(0, 0)
        var player = $("#player")
            .attr("src", url)
            .get(0)
        player.load()
        player.play()
    }
}

var controlClicked = function() {
    socket.emit('play', {
        toggle: true
    })
}

var sliderClicked = function(ev) {
    var percent = ev.offsetX / $(this).width()
    var property = $(this).data("property")
    var factor = property === "currentTime" ? m_status.duration : 1
    var data = {}
    data[property] = percent * factor
    socket.emit('play', data)
}

var mutedClicked = function(ev) {
    socket.emit('play', {
        muted: !m_status.muted
    })
}

var togglePlayerRemote = function(remote) {
    $("#video-container").toggle(!remote)
    $("#video-remote").toggle(remote)
    if(remote) {
        $("#player").get(0).pause()
    }
}

var formatTime = function(dur) {
    dur = parseInt(dur)
    var sec = dur % 60
    var min = Math.floor(dur/60)
    return min + ":" + sec
}

var showStatus = function() {
    togglePlayerRemote(!!m_status.consumers)

    if(m_status.nowPlaying) {
        var file = decodeURI(m_status.nowPlaying).split("/").pop()
        $("#now_playing").text(file)
    }

    if(m_status.paused !== undefined) {
        $(".glyphicon-pause").toggle(!m_status.paused)
        $(".glyphicon-play").toggle(m_status.paused)
    }

    if(m_status.currentTime && m_status.duration) {
        $(".jumpt-to").show()
        $("#duration").text(formatTime(m_status.duration))
        $(".jump-to .progress-bar").width(Math.round(m_status.currentTime * 100 / m_status.duration) + "%")
            .text(formatTime(m_status.currentTime))
    } else {
        $(".jumpt-to").hide()
    }
    if(m_status.volume !== undefined) {
        $(".volume .progress-bar").width(Math.round(m_status.volume * 100) + "%")
        $(".muted i").toggleClass("glyphicon-volume-down", !m_status.muted && m_status.volume < 0.5)
        $(".muted i").toggleClass("glyphicon-volume-up", !m_status.muted && m_status.volume >= 0.5)
    }
    if(m_status.muted !== undefined) {
        $(".muted i").toggleClass("glyphicon-volume-off", m_status.muted)
    }
}


/* SocketIO listeners */
var socket = io.connect('http://' + document.domain + ':' + location.port + socketNamespace);
socket.on('connect', function() {
    socket.emit('register controller', {})
})
socket.on('status', function(data){
    m_status = $.extend(m_status, data)
    if(!m_status.nowPlaying) {
        delete m_status.currentTime
        delete m_status.duration
    }
    showStatus()
})


/* DOM event listeners */
$(document).ready(function(){
    $("a.movie").on("click", movieClicked)
    $("a.pause").on("click", controlClicked)
    $(".progress").on("click", sliderClicked)
    $(".muted").on("click", mutedClicked)
})
