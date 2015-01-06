var statusMap = new can.Map({
    enabled: false
})

statusMap.bind("src", function(ev, newVal, oldVal){
    if(newVal) {
        statusMap.attr("fileName", decodeURI(newVal).split("/").pop())
    } else {
        statusMap.removeAttr("currentTime")
        statusMap.removeAttr("duration")
    }
})
statusMap.bind("consumers", function(ev, newVal, oldVal){
    statusMap.attr("enabled", newVal > 0)
})
statusMap.bind("fullscreen", function(ev, newVal, oldVal){
    if(newVal === false) {
        exitFullscreen()
    }
})

/* Mustache helper for localized strings */
Mustache.registerHelper("lbl", function(key){
    return lbl[key]
})

/* Play/Pause Button */
can.Component.extend({
    tag: "button-pause",
    template: can.view("#button-pause"),
    scope: statusMap,
    events: {
        click: function(){
            socket.emit('play', {
                paused: !statusMap.attr("paused")
            })
        }
    }
})


function enterFullscreen(el) {
    if (el && !document.fullscreenElement &&    // alternative standard method
            !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {  // current working methods

        if (el.requestFullscreen) {
            el.requestFullscreen();
        } else if (el.msRequestFullscreen) {
            el.msRequestFullscreen();
        } else if (el.mozRequestFullScreen) {
            el.mozRequestFullScreen();
        } else if (el.webkitRequestFullscreen) {
            el.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
        }
    }
}

function exitFullscreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
    } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
    }
}
/* Fullscreen Button */
can.Component.extend({
    tag: "button-fullscreen",
    template: can.view("#button-fullscreen"),
    scope: {
        visible: can.compute(function(){
            return statusMap.attr("fullscreen") || !!$("video").length
        })
    },
    events: {
        click: function(){
            enterFullscreen($("video").get(0))
            socket.emit('update status', {
                fullscreen: !statusMap.attr("fullscreen")
            })
        }
    }
})

/* Mute Button */
can.Component.extend({
    tag: "button-mute",
    template: can.view("#button-mute"),
    scope: {
        iconstate: function(){
            var volume = parseFloat(statusMap.attr("volume"))
            if(statusMap.attr("muted") || !volume) {
                return "off"
            }
            return (volume < 0.5) ? "down" : "up"
        }
    },
    events: {
        click: function(ev) {
            socket.emit('play', {
                muted: !statusMap.attr("muted")
            })
        }
    }
})


var sliderComponent = can.Component.extend({
    tag: "slider",
    template: can.view("#slider-progress"),
    events: {
        getCursorVal: function(el, ev){
            var percent = ev.offsetX / el.find(".progress").width()
            var factor = this.scope.property === "currentTime" ? statusMap.duration : 1
            return percent * factor
        },
        click: function(el, ev) {
            var data = {}
            data[this.scope.property] = this.getCursorVal(el, ev)
            socket.emit('play', data)
        },
        mousemove: function(el, ev) {
            var label = this.scope.formatTooltip(this.getCursorVal(el, ev))
            this.element.attr("title", label)
        }
    }
})

var formatTime = function(timeInSec) {
    var s = parseInt(timeInSec)
    var sec = (s % 60)+""
    return isNaN(s) ?
        "" :
        Math.floor(s/60) + ":" + (sec.length === 2 ? sec : "0"+sec)
}
/* Time/Duration Slider */
sliderComponent.extend({
    tag: "slider-progress",
    scope: {
        property: "currentTime",
        formatTooltip: formatTime,
        total: can.compute(function(){
            return formatTime(statusMap.attr("duration"))
        }),
        current: can.compute(function(){
            return formatTime(statusMap.attr("currentTime"))
        }),
        percent: can.compute(function() {
            return statusMap.attr("currentTime") ?
                parseInt((parseFloat(statusMap.attr("currentTime")) * 100) / parseFloat(statusMap.attr("duration"))) :
                0
        })
    }
})

/* Volume Slider */
sliderComponent.extend({
    tag: "slider-volume",
    scope: {
        property: "volume",
        formatTooltip: function(value){
            return parseInt(value * 100) + "%"
        },
        percent: can.compute(function() {
            return parseFloat(statusMap.attr("volume")) * 100
        })
    }
})

/* Subtitles Menu */
can.Component.extend({
    tag: "select-subtitles",
    template: can.view("#select-subtitles"),
    scope: {
        subtitles: []
    },
    helpers: {
        isActive: function(opts){
            var selected = statusMap.attr("subtitles")
            if(selected && opts.context.url.split("/").pop() === selected.split("/").pop()) {
                return opts.fn()
            } else {
                return opts.inverse()
            }
        }
    },
    events: {
        "button click": function() {
            var scope = this.scope
            if(statusMap.src) {
                $.getJSON("/movies/subtitles?src="+statusMap.src)
                .done(function(data){
                    scope.subtitles.replace(data.subtitles)
                })
            }
        },
        "a click": function(el, ev) {
            ev.preventDefault()
            socket.emit("play", {
                subtitles: el.data("url")
            })
        }
    }
})

/* SocketIO listeners */
if(!window.socket) {
    socket = io.connect('http://' + document.domain + ':' + location.port + socketNamespace);
}
socket.on('connect', function() {
    socket.emit('register controller', {})
})
socket.on('status', function(data){
    statusMap.attr(data)
})
