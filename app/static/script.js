console.log("Script loaded successfully!");

const canvas = document.getElementById('stickmanCanvas');
const ctx = canvas.getContext('2d');

// Prevent entering numbers
document.addEventListener('DOMContentLoaded', function() {
    const letterInput = document.getElementById('letter');

    if (letterInput) {
        letterInput.addEventListener('input', function() {
            const value = letterInput.value;
            if (!/^[a-zA-Z]$/.test(value)) {
                letterInput.value = '';
                alert('Please enter a valid letter (A-Z only).');
            }
        });
    }
});

function drawGallows() {
    // Base
    ctx.beginPath();
    ctx.moveTo(10, 230);
    ctx.lineTo(190, 230);
    ctx.stroke();

    // Pole
    ctx.beginPath();
    ctx.moveTo(50, 230);
    ctx.lineTo(50, 20);
    ctx.stroke();

    // Top bar
    ctx.beginPath();
    ctx.moveTo(50, 20);
    ctx.lineTo(150, 20);
    ctx.stroke();

    // Rope
    ctx.beginPath();
    ctx.moveTo(150, 20);
    ctx.lineTo(150, 50);
    ctx.stroke();
}

function drawStickman(wrongGuesses) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 🎨 Always draw the gallows first
    drawGallows();

    // 🧍 Only draw stickman parts based on wrong guesses
    if (wrongGuesses > 0) { // draw head
        ctx.beginPath();
        ctx.arc(150, 70, 20, 0, Math.PI * 2);
        ctx.stroke();
    }
    if (wrongGuesses > 1) { // draw body
        ctx.beginPath();
        ctx.moveTo(150, 90);
        ctx.lineTo(150, 150);
        ctx.stroke();
    }
    if (wrongGuesses > 2) { // left arm
        ctx.beginPath();
        ctx.moveTo(150, 110);
        ctx.lineTo(120, 130);
        ctx.stroke();
    }
    if (wrongGuesses > 3) { // right arm
        ctx.beginPath();
        ctx.moveTo(150, 110);
        ctx.lineTo(180, 130);
        ctx.stroke();
    }
    if (wrongGuesses > 4) { // left leg
        ctx.beginPath();
        ctx.moveTo(150, 150);
        ctx.lineTo(120, 190);
        ctx.stroke();
    }
    if (wrongGuesses > 5) { // right leg
        ctx.beginPath();
        ctx.moveTo(150, 150);
        ctx.lineTo(180, 190);
        ctx.stroke();
    }
}

// 🎯 Automatically draw the stickman when page loads
window.onload = function() {
    const wrongGuesses = parseInt(document.getElementById('wrongGuesses').value);
    drawStickman(wrongGuesses);
}