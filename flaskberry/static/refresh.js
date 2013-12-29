var extractElement = function(targetId, str){
    var doc = (new DOMParser).parseFromString(str, 'text/html')
    return doc.querySelector(targetId)
}

var replaceElements = function(targetId, element){
    var target = document.querySelector(targetId)
    target.parentElement.replaceChild(element, target)
}

var sendRequest = function(){
    var req =  new XMLHttpRequest()
    req.open('GET', window.location.pathname, true)
    req.onreadystatechange = function () {
        if(req.readyState === 4 && req.status === 200){
            replaceElements(refreshTarget, extractElement(refreshTarget, req.response))
        }
    }
    req.send()
}

if(typeof XMLHttpRequest === "function" && refreshTarget){
    window.setInterval(sendRequest, 3000)
}
