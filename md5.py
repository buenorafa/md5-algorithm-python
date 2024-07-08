from cmath import sin


class MD5:
    _message = None

    @classmethod
    def digest(cls, message):
        cls._message = message
        # Step 1:
        padded_bits = cls.add_padding_bits()
        # Step 2:
        preprocessed_message = cls.append_length(padded_bits)
        # Step 3 & 4:
        processed_message = cls.process_message(preprocessed_message)
        # Step 5:
        return cls.formatted_output(processed_message)

    # Step 1. Add Padding Bits: bit_sequence length mod 512 has to be equal to 448
    @classmethod
    def add_padding_bits(cls):
        # Convert the message to a bit sequence
        message_bytes = cls._message.encode()

        # Append '1' as per MD5 padding requirements
        message_bytes += b"\x80"

        # Add '0's needed to pad the message
        while (len(message_bytes) * 8) % 512 != 448:
            message_bytes += b"\x00"

        return message_bytes

    # Step 2. This class method appends the 64-bit representation of the original message size,
    # in little-endian format (least significant byte first), to the padded bit sequence.
    @classmethod
    def append_length(cls, padded_message):
        # Message's size in bits
        original_size = len(cls._message * 8)

        # Convert the size to a 64-bit representation in little-endian format
        size_64bits = (original_size).to_bytes(8, byteorder="little", signed=False)
        # Concatenate the 64 bits representing the size to the padded bit sequence
        preprocessed_message = padded_message + size_64bits

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
        rotate_left = (
            lambda x, c: ((x & 0xFFFFFFFF) << c | (x & 0xFFFFFFFF) >> (32 - c))
            & 0xFFFFFFFF
        )

        # All operations are wrapped with modulo 2**32 to ensure the result remains within the 32-bit limit
        mod = 2**32

        # Initial buffer
        A, B, C, D = cls.initialize_md_buffer()

        for n in range(0, len(preprocessed_message), 64):
            chunk = preprocessed_message[n : n + 64]

            X = [int.from_bytes(chunk[j : j + 4], "little") for j in range(0, 64, 4)]

            a, b, c, d = A, B, C, D

            for i in range(64):
                if i < 16:
                    aux = F(b, c, d)
                    k = i
                    s = [7, 12, 17, 22]
                elif i < 32:
                    aux = G(b, c, d)
                    k = (5 * i + 1) % 16
                    s = [5, 9, 14, 20]
                elif i < 48:
                    aux = H(b, c, d)
                    k = (3 * i + 5) % 16
                    s = [4, 11, 16, 23]
                else:
                    aux = I(b, c, d)
                    k = (7 * i) % 16
                    s = [6, 10, 15, 21]

                aux = (aux + X[k] + T[i] + a) % mod
                a = d
                d = c
                c = b
                b = (b + rotate_left(aux, s[i % 4])) % mod

            A = (A + a) % mod
            B = (B + b) % mod
            C = (C + c) % mod
            D = (D + d) % mod

        return [A, B, C, D]

    # Step 5.
    staticmethod

    def formatted_output(processed_registers):
        output = b""
        for register in processed_registers:
            # Convert to little endian
            output += register.to_bytes(4, byteorder="little", signed=False)
        return output.hex()
