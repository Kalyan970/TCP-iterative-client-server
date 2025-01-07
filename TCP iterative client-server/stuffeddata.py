def bit_stuff(data):
    stuffed_data = ""
    count = 0
    
    for bit in data:
        if bit == '1':
            count += 1
            stuffed_data += bit
        else:
            count = 0
            stuffed_data += bit
        
        if count == 5:  # If 5 consecutive 1's are found, stuff a 0 bit
            stuffed_data += '0'
            count = 0
    
    return stuffed_data

def bit_unstuff(stuffed_data):
    unstuffed_data = ""
    count = 0
    consecutive_ones = 0
    
    for bit in stuffed_data:
        if bit == '1':
            count += 1
            consecutive_ones += 1
            unstuffed_data += bit
        else:
            if count == 5 and consecutive_ones == 5:  # If 5 consecutive 1's are found, and the next bit is 0, remove the stuffed 0 bit
                count = 0
                consecutive_ones = 0
                continue
            else:
                count = 0
                consecutive_ones = 0
                unstuffed_data += bit
        
    return unstuffed_data

# Example usage:
data = "011111101111110"  # 15-bit example data with bit stuffing flag
print("Original data:", data)

stuffed_data = bit_stuff(data)
print("Stuffed data:", stuffed_data)

unstuffed_data = bit_unstuff(stuffed_data)
print("Unstuffed data:", unstuffed_data)