from utils import string_to_bit_sequence
from cmath import sin


class MD5:
    _message = None

    # Step 1. Add Padding Bits: bit_sequence length mod 512 has to be equal to 448
    def add_padding_bits(cls):
        # Convert the message to a bit sequence
        bit_sequence = string_to_bit_sequence(cls._message)

        # Append '1' as per MD5 padding requirements
        padded_bit_sequence = bit_sequence + "1"

        # Calculate the number of '0's needed to pad the sequence
        remaining_bits_len = (448 - len(bit_sequence) % 512) % 512
        padded_bit_sequence += "0" * remaining_bits_len

        return padded_bit_sequence

    # Step 2. This class method appends the 64-bit representation of the original message size,
    # in little-endian format (least significant byte first), to the padded bit sequence.
    @classmethod
    def append_length(cls, padded_bit_sequence):
        # Convert the original string to a bit sequence
        bit_sequence = string_to_bit_sequence(cls._message)

        # Get the size of the original message in bits
        size = len(bit_sequence)

        # Convert the size to a 64-bit representation in little-endian format
        size_64bits = (size * 8).to_bytes(8, byteorder="little", signed=False)

        # Convert bytes to bits
        size_bit_sequence = "".join(format(byte, "08b") for byte in size_64bits)

        # Concatenate the 64 bits representing the size to the padded bit sequence
        preprocessed_message = padded_bit_sequence + size_bit_sequence

        # After these two preprocessing steps (adding padding bits and appending length),
        # the preprocessed message length will be a multiple of 512 bits.
        return preprocessed_message

    # Step 3. Initialize MD5 Buffer return initial values defined in the rfc
    @staticmethod
    def initialize_md_buffer():
        A = 0x67452301
        B = 0xEFCDAB89
        C = 0x98BADCFE
        D = 0x10325476

        return A, B, C, D

    # Step 4.
    @classmethod
    def digest(cls, preprocessed_message):
        # Auxiliary functions defined in RFC
        # each take as input three 32-bit words and return one 32-bit word
        F = lambda x, y, z: (x & y) | (~x & z)
        G = lambda x, y, z: (x & z) | (y & ~z)
        H = lambda x, y, z: x ^ y ^ z
        I = lambda x, y, z: y ^ (x | ~z)

        # Creates table T as specified in the RFC
        T = [int(4294967296 * abs(sin(i + 1))) for i in range(64)]

        # Define the left rotation function, which rotates `x` left `n` bits.
        rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

        # Modular_add lambda ensures that the result of the addition will never exceed the 32-bit limit
        modular_add = lambda x, y: (x + y) % 2**32
