var movieClicked = function() {
    window.scrollTo(0, 0)
    var player = document.querySelector("#player")
    player.setAttribute("src", moviesUrl + this.dataset.movie)
    player.load()
    player.play()
}

var initListeners = function() {
    var elements = document.querySelectorAll("a.movie")
    for(var i = 0; i < elements.length; i++) {
        elements[i].onclick = movieClicked
    }
}

document.addEventListener('DOMContentLoaded', initListeners, false);
