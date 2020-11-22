var client_id = Date.now();
var loc = window.location,
  new_uri;

if (loc.protocol === "https:") {
  new_uri = "wss:";
} else {
  new_uri = "ws:";
}
new_uri += "//" + loc.host;
new_uri += `${loc.pathname}ws/${client_id}`;

var ws = new WebSocket(`${new_uri}`);
ws.onmessage = function (event) {
  var message = document.getElementById("message");
  var time = document.getElementById("time");
  data = JSON.parse(event.data);
  message.innerHTML = data.message;
  time.innerHTML = data.current_time;
  if (data.status == 0) {
    document.getElementById("thumbs").classList.remove("fa-thumbs-up");
    document.getElementById("thumbs").classList.add("fa-thumbs-down");
  } else {
    document.getElementById("thumbs").classList.remove("fa-thumbs-down");
    document.getElementById("thumbs").classList.add("fa-thumbs-up");
  }
};
