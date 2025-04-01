#include <iostream>
#include <vector>
#include <string>
#include <cstdint>

// The key insight is to understand what the original encryption function does:
// In C++, the encryption function would be:
void encrypt(const uint8_t* matrix, char& c1, char& c2) {
    // Save original c1
    char orig_c1 = c1;
    
    // Encrypt the two characters
    c1 = (c1 * matrix[0] + c2 * matrix[1]) % 256;
    c2 = (c2 * matrix[3] + orig_c1 * matrix[2]) % 256;
}

// In the original code, this function is called in a loop on consecutive pairs of characters
// Let's simulate the original encryption to verify our understanding
std::string test_encrypt(const std::string& input, const std::vector<std::vector<uint8_t>>& matrices) {
    if (input.length() < 2) return input;
    
    std::string result = input;
    
    for (size_t i = 0; i < result.length() - 1; i++) {
        size_t matrix_idx = i % 8;
        encrypt(matrices[matrix_idx].data(), result[i], result[i+1]);
    }
    
    return result;
}

// Try to find the original character pair that produces a given encrypted pair
std::pair<char, char> find_original_pair(uint8_t enc1, uint8_t enc2, const uint8_t* matrix) {
    // Brute force all possible character pairs and see which one encrypts to our target
    for (int c1 = 0; c1 < 256; c1++) {
        for (int c2 = 0; c2 < 256; c2++) {
            char test1 = c1;
            char test2 = c2;
            
            encrypt(matrix, test1, test2);
            
            if ((uint8_t)test1 == enc1 && (uint8_t)test2 == enc2) {
                return {(char)c1, (char)c2};
            }
        }
    }
    
    // If no solution found, return a pair of question marks
    return {'?', '?'};
}

int main() {
    // The encrypted flag bytes from DAT_001040c0
    std::vector<uint8_t> encrypted = {
        0x0a, 0x81, 0xae, 0x98, 0xa4, 0x0d, 0x63, 0x7a, 
        0x5e, 0x21, 0xb1, 0xdd, 0x69, 0xda, 0xb3, 0x7b, 
        0x91, 0x8a, 0x37, 0x65, 0x71, 0x82, 0x1f, 0x2b, 
        0x20, 0xb9, 0xbe, 0xf9, 0xad, 0x72, 0x77, 0x50, 
        0xd5, 0x6b, 0xc9
    };
    
    // The 8 coefficient matrices from DAT_001040a0
    std::vector<std::vector<uint8_t>> matrices = {
        {0x57, 0xa9, 0xa2, 0xa7}, // Matrix 0
        {0x87, 0x44, 0xd6, 0xcf}, // Matrix 1
        {0x9b, 0x92, 0x57, 0x31}, // Matrix 2
        {0xfd, 0xb8, 0x98, 0x85}, // Matrix 3
        {0xa8, 0x4f, 0xd9, 0x4c}, // Matrix 4
        {0xa6, 0xad, 0x79, 0x84}, // Matrix 5
        {0x85, 0x3f, 0xdb, 0x48}, // Matrix 6
        {0x81, 0x99, 0x7f, 0x5a}  // Matrix 7
    };
    
    // Convert the encrypted bytes to a string for easier manipulation
    std::string encrypted_str;
    for (uint8_t byte : encrypted) {
        encrypted_str.push_back(byte);
    }
    
    // Decryption approach 1: Start from the end and work backwards
    std::string decrypted1 = encrypted_str;
    
    // We need to process pairs from right to left to undo the transformations
    for (int i = encrypted_str.length() - 2; i >= 0; i--) {
        int matrix_idx = i % 8;
        
        // Find the original pair that would encrypt to our current pair
        auto [orig1, orig2] = find_original_pair((uint8_t)decrypted1[i], (uint8_t)decrypted1[i+1], matrices[matrix_idx].data());
        
        decrypted1[i] = orig1;
        decrypted1[i+1] = orig2;
    }
    
    // Alternative approach 2: Try common flag prefixes and see if they match
    std::vector<std::string> common_prefixes = {"flag{", "FLAG{", "ctf{", "CTF{", "SECCON{"};
    std::string best_match;
    
    for (const auto& prefix : common_prefixes) {
        // Start with the prefix and see if it encrypts to match our target
        std::string test = prefix;
        // Pad to the length of the encrypted string
        test.resize(encrypted_str.length(), '_');
        
        std::string encrypted_test = test_encrypt(test, matrices);
        
        // Check how many characters match at the start
        size_t match_count = 0;
        while (match_count < encrypted_test.length() && 
               (uint8_t)encrypted_test[match_count] == encrypted[match_count]) {
            match_count++;
        }
        
        std::cout << "Prefix \"" << prefix << "\" matches first " << match_count << " characters" << std::endl;
        
        if (match_count >= prefix.length()) {
            std::cout << "Found a potential match with prefix: " << prefix << std::endl;
            
            // If we found a good prefix match, let's try to decrypt the rest
            if (match_count > best_match.length()) {
                best_match = prefix;
            }
        }
    }
    
    // If we found a good prefix, use it to decrypt
    std::string decrypted2;
    if (!best_match.empty()) {
        decrypted2 = best_match;
        decrypted2.resize(encrypted_str.length(), '_');
        
        // Apply encryption and adjust characters to make it match
        for (size_t i = best_match.length(); i < encrypted_str.length() - 1; i++) {
            // Try all printable characters for this position
            for (char c = 32; c < 127; c++) {
                decrypted2[i] = c;
                
                // Check if this produces a match for this position
                std::string test = decrypted2.substr(0, i+2); // Include the current character and the next one
                test.resize(encrypted_str.length(), '_');     // Pad to full length
                
                std::string encrypted_test = test_encrypt(test, matrices);
                
                if ((uint8_t)encrypted_test[i] == encrypted[i]) {
                    // We found a match for this position
                    break;
                }
            }
        }
    }
    
    // Print results
    std::cout << "\nApproach 1 - Brute force decryption:" << std::endl;
    std::cout << "Decrypted (as characters): ";
    for (unsigned char c : decrypted1) {
        if (c >= 32 && c < 127)
            std::cout << c;
        else
            std::cout << "\\x" << std::hex << (int)c << std::dec;
    }
    std::cout << std::endl;
    
    std::cout << "\nApproach 2 - Prefix-based decryption:" << std::endl;
    if (!best_match.empty()) {
        std::cout << "Decrypted (using prefix \"" << best_match << "\"): " << decrypted2 << std::endl;
    } else {
        std::cout << "No matching prefix found." << std::endl;
    }
    
    return 0;
}