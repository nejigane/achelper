let problem = location.href.split('/').pop();

let previousCMs = document.querySelectorAll('.CodeMirror.cm-s-default');
previousCMs.forEach(function(cm) {
  cm.parentNode.removeChild(cm);
});
var editor = CodeMirror.fromTextArea(document.querySelector('textarea.editor'), {
  viewportMargin: Infinity,
  lineNumbers: true
});


let sampleElems = document.querySelectorAll('#task-statement span.lang-ja > div.part pre');
var samples = [];
for (var i = 0; i < sampleElems.length; i += 2) {
  samples.push({
    input: sampleElems[i].textContent,
    output: sampleElems[i+1].textContent,
    id: sampleElems[i+1].id,
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

  editor.setValue(data.source);
  console.log(data);
});
