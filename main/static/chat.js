// when index.html has been loaded
$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    // get the user id which has been passed and the message when user hits submit
    $("#messageform").on("submit", function() {
        newMessage($(this));
        newUserid($(this));
        console.log(document.getElementById('usrid').innerHTML)
        return false;
    });
    // get the user id which has been passed and the message or when user hits enter
    $("#messageform").on("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            newUserid($(this));
            return false;
        }
    });
    $("#message").select();
    // $("#usrid").select();
    updater.start();
});
// function for getting the message
function newMessage(form) {
    var message = form.formToDict();
    updater.socket.send(JSON.stringify(message));
    
    form.find("input[type=text]").val("").select();
}
// function for getting the userid
function newUserid(form) {
    var userid = form.formToDict();
    // updater.socket.send(JSON.stringify(userid));
    
    form.find("input[type=text]").val("").select();
    
}
jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/chatsocket";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }
};