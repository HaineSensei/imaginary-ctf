def extract_message(filename):
    with open(filename, 'rb') as f:
        # Skip BMP header
        f.seek(0x7A)
        
        # Read all data
        data = f.read(0x180)
        
        # Extract bits - message data is in the LSB after masking
        message_bits = []
        
        # First section 0-0x80
        for i in range(0x80):
            byte = data[i]
            # Data is in LSB after masking with pattern
            message_bits.append(byte & 1)
            
        # Second section 0x80-0x180
        for i in range(0x80, 0x180):
            byte = data[i]
            # Same extraction pattern
            message_bits.append(byte & 1)
        
        # Convert bits to bytes
        message_bytes = []
        for i in range(0, len(message_bits), 8):
            bits = message_bits[i:i+8]
            if len(bits) == 8:
                byte = sum(bit << i for i, bit in enumerate(reversed(bits)))
                if byte == 0:  # Stop at null terminator
                    break
                message_bytes.append(byte)
        
        try:
            return bytes(message_bytes).decode('utf-8')
        except UnicodeDecodeError:
            return f"Raw bytes: {' '.join(f'{b:02x}' for b in message_bytes)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <bitmap_file>")
        sys.exit(1)
    
    message = extract_message(sys.argv[1])
    print("Extracted message:", message)