const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Fill with white background before drawing starts for smooth conversion to grayscale later
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

let drawing = false;

function getMousePos(evt) {
  const rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

canvas.addEventListener("mousedown", (e) => {
  drawing = true;
  const pos = getMousePos(e);
  ctx.beginPath();
  ctx.moveTo(pos.x, pos.y);
});

canvas.addEventListener("mousemove", (e) => {
  if (!drawing) return;
  const pos = getMousePos(e);
  ctx.lineTo(pos.x, pos.y);
  ctx.strokeStyle = "black";
  ctx.lineWidth = 10;
  ctx.lineCap = "round";
  ctx.stroke();
});

canvas.addEventListener("mouseup", () => {
  drawing = false;
});

canvas.addEventListener("mouseleave", () => {
  drawing = false;
});

function clearCanvas() {
  //ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function submitDrawing() {
    const dataURL = canvas.toDataURL() // returns current content of canvas as image

    fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({image: dataURL})
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.message);
    });
}
