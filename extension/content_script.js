let problem = location.href.split('/').pop();
let elems = document.querySelectorAll('#task-statement span.lang-ja > div.part pre');
var samples = [];
for (var i = 0; i < elems.length; i += 2) {
  samples.push({
    input: elems[i].textContent,
    output: elems[i+1].textContent,
    id: elems[i+1].id,
  });
}

var socket = new WebSocket('ws://localhost:8080/');
socket.addEventListener('open', function (event) {
  socket.send(JSON.stringify({
    problem: problem,
    samples: samples,
  }));
});
socket.addEventListener('message', function (event) {
  var data = JSON.parse(event.data);
  let previousElems = document.querySelectorAll('.acs-appended');
  previousElems.forEach(function(elem) {
    elem.parentNode.removeChild(elem);
  });

  data.samples.forEach(function(sample) {
    var target = document.getElementById(sample.id);
    if (sample.output == sample.stdout) {
      target.style.backgroundColor = 'green';
    } else {
      target.style.backgroundColor = 'red';
      var std = document.createElement('pre');
      std.className = 'acs-appended'
      var stdText = document.createTextNode(sample.stdout + sample.stderr);
      std.appendChild(stdText);
      target.parentNode.insertBefore(std, target.nextSibling);
    }
  });

  let statement = document.querySelector('#task-statement');
  var source = document.createElement('pre');
  source.className = 'acs-appended'
  var sourceText = document.createTextNode(data.source);
  source.appendChild(sourceText);
  statement.parentNode.insertBefore(source, statement.nextSibling);
  console.log(data);
});
