const fs = require('fs');
const wasmBuffer = fs.readFileSync('./vault.wasm');

// We need to convert vault.wasm.c into something we can use directly in Node
// From analyzing the code, we really just need the check_pin function

const env = {
    memory: new WebAssembly.Memory({ initial: 256, maximum: 256 }),
};

WebAssembly.instantiate(wasmBuffer, { env }).then(wasmModule => {
    const instance = wasmModule.instance;
    
    // Function to test a range of PINs
    function testPINRange(start, end) {
        const results = [];
        for(let i = start; i <= end; i++) {
            const pin = i.toString().padStart(8, '0');
            try {
                // Call the check_pin function from our wasm instance
                const result = instance.exports.check_pin(parseInt(pin));
                if(result) {
                    results.push(pin);
                    console.log(`Found valid PIN: ${pin}`);
                }
            } catch(e) {
                console.error(`Error on PIN ${pin}:`, e);
            }
            
            // Show progress every 100000 attempts
            if(i % 100000 === 0) {
                console.log(`Progress: ${((i-start)/(end-start)*100).toFixed(2)}%`);
            }
        }
        return results;
    }

    // Test from 0 to 99999999 in batches
    const BATCH_SIZE = 1000000;
    let currentStart = 0;

    function runNextBatch() {
        const end = Math.min(currentStart + BATCH_SIZE - 1, 99999999);
        console.log(`Testing PINs from ${currentStart} to ${end}`);
        const validPins = testPINRange(currentStart, end);
        console.log(`Found ${validPins.length} valid PINs in this batch`);
        
        if(end < 99999999) {
            currentStart += BATCH_SIZE;
            runNextBatch();
        }
    }

    runNextBatch();
}).catch(err => {
    console.error('Failed to load WASM:', err);
});