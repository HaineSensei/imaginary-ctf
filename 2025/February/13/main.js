window.onload = function() {
    function checkPin() {
        const pin = document.getElementById('pin').value.padStart(8, '0');
        if (pin.length !== 8 || !/^\d+$/.test(pin)) {
            showResult("Invalid PIN format", false);
            return;
        }

        const result = Module.ccall('check_pin', 'boolean', ['number'], [parseInt(pin)]);

        fetch('/verify', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `pin=${pin}&result=${result}`
        })
        .then(response => response.json())
        .then(data => {
            showResult(data.success ? data.flag : data.message, data.success);
        });
    }

    function showResult(message, success) {
        const resultDiv = document.getElementById('result');
        const vaultBox = document.getElementById('vault-box');
        const successSound = document.getElementById('success-sound');
        const errorSound = document.getElementById('error-sound');
            
        resultDiv.style.color = success ? 'green' : 'red';
        resultDiv.textContent = message;

        if (success) {
            successSound.play();
            vaultBox.classList.add('animate-pulse');
            setTimeout(() => vaultBox.classList.remove('animate-pulse'), 1000);
        } else {
            errorSound.play();
            vaultBox.classList.add('shake');
            setTimeout(() => vaultBox.classList.remove('shake'), 500);
        }
    }

    document.querySelector("button").onclick = checkPin;
};
