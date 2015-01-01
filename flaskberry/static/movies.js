var movieClicked = function(ev) {
    ev.preventDefault()
    var url = moviesUrl + $(this).attr("href")

    window.scrollTo(0, 0)
    var player = $("#player")
        .attr("src", url)
        .get(0)
    player.load()
    player.play()
}

/* DOM event listeners */
$(document).ready(function(){
    $("a.movie").on("click", movieClicked)
})
