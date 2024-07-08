# from utils import string_to_bit_sequence
from cmath import sin


class MD5:
    _message = None

    # Organizar esse método : TODO
    @classmethod
    def digest(cls, message):
        cls._message = message

        preprocessed_message = cls.append_length(cls.add_padding_bits())
        # Process & Output
        return cls.formatted_output(cls.process_message(preprocessed_message))

    @staticmethod
    def string_to_bit_sequence(s):
        # Converte a string para uma sequência de bits
        bit_sequence = "".join(format(ord(char), "08b") for char in s)
        return bit_sequence

    # Step 1. Add Padding Bits: bit_sequence length mod 512 has to be equal to 448
    @classmethod
    def add_padding_bits(cls):
        # Convert the message to a bit sequence
        bit_sequence = cls.string_to_bit_sequence(cls._message)

        # Append '1' as per MD5 padding requirements
        padded_bit_sequence = bit_sequence + "1"

        # Calculate the number of '0's needed to pad the sequence
        remaining_bits_len = (448 - (len(bit_sequence) + 1) % 512) % 512
        padded_bit_sequence += "0" * remaining_bits_len

        return padded_bit_sequence

    # Step 2. This class method appends the 64-bit representation of the original message size,
    # in little-endian format (least significant byte first), to the padded bit sequence.
    @classmethod
    def append_length(cls, padded_bit_sequence):
        # Convert the original string to a bit sequence
        bit_sequence = cls.string_to_bit_sequence(cls._message)

        # Get the size of the original message in bits
        size = len(bit_sequence)

        # Convert the size to a 64-bit representation in little-endian format
        # size_64bits = (size * 8).to_bytes(8, byteorder="little", signed=False)
        size_64bits = (size).to_bytes(8, byteorder="little", signed=False)

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
    def process_message(cls, preprocessed_message):
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

        # All operations are wrapped with modulo 2**32 to ensure the result remains within the 32-bit limit
        mod = 2**32

        # Process the padded message in 512bits blocks
        num_blocks = len(preprocessed_message) // 512

        A, B, C, D = cls.initialize_md_buffer()

        for block in range(num_blocks):
            start = block * 512
            # Break blocks into 16 words of 32bits
            X = [
                int(preprocessed_message[start + (x * 32) : start + (x * 32) + 32], 2)
                for x in range(16)
            ]

            a, b, c, d = A, B, C, D

            # for i in range(64):
            #     if i in range(15):
            #         aux = F(b, c, d)
            #         k = i
            #         s = [7, 12, 17, 22]
            #     elif i in range(16, 31):
            #         aux = G(b, c, d)
            #         k = (5 * i + 1) % 16
            #         s = [5, 9, 14, 20]
            #     elif i in range(32, 47):
            #         aux = H(b, c, d)
            #         k = (3 * i + 5) % 16
            #         s = [4, 11, 16, 23]
            #     elif i in range(48, 63):
            #         aux = I(b, c, d)
            #         k = (7 * i) % 16
            #         s = [6, 10, 15, 21]

            for i in range(64):
                if 0 <= i <= 15:
                    aux = F(b, c, d)
                    k = i
                    s = [7, 12, 17, 22]
                elif 16 <= i <= 31:
                    aux = G(b, c, d)
                    k = (5 * i + 1) % 16
                    s = [5, 9, 14, 20]
                elif 32 <= i <= 47:
                    aux = H(b, c, d)
                    k = (3 * i + 5) % 16
                    s = [4, 11, 16, 23]
                else:
                    aux = I(b, c, d)
                    k = (7 * i) % 16
                    s = [6, 10, 15, 21]

                aux = (aux + X[k] + T[i] + a) % mod
                # Swap
                a = d
                d = c
                c = b
                b = (b + rotate_left(aux, s[i % 4])) % mod
            # Update buffer
            A = (A + a) % mod
            B = (B + b) % mod
            C = (C + c) % mod
            D = (D + d) % mod
        return [A, B, C, D]

    # Step 5.
    staticmethod

    def formatted_output(words):
        output = ""
        for word in words:
            # Transforma as palavras em little endian
            bytes_little_endian = word.to_bytes(4, byteorder="little", signed=False)
            # Converte os bytes para uma representação hexadecimal
            hex_representation = "".join(
                format(byte, "02x") for byte in bytes_little_endian
            )
            # Concatena numa string
            output += hex_representation
        return output
