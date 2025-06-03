class PlayfairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [letter for letter in alphabet if letter not in key_set]

        matrix = list(key)
        for letter in remaining_letters:
            if letter not in matrix:  # Tránh trùng lặp
                matrix.append(letter)
            if len(matrix) == 25:
                break

        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return None  # Trả về None nếu không tìm thấy

    def playfair_encrypt(self, plain_text, matrix):
        # Làm sạch văn bản: chỉ giữ chữ cái, chuyển J thành I, và thành chữ hoa
        plain_text = ''.join(c for c in plain_text.upper().replace("J", "I") if c.isalpha())
        encrypted_text = ""

        # Chia văn bản thành các cặp ký tự
        i = 0
        while i < len(plain_text):
            pair = plain_text[i:i+2]
            if len(pair) == 1:
                pair += "X"  # Thêm X nếu cặp không đủ
            elif pair[0] == pair[1]:
                pair = pair[0] + "X"  # Thêm X nếu hai ký tự giống nhau
                i -= 1  # Quay lại để xử lý lại ký tự hiện tại

            # Tìm tọa độ của hai ký tự
            coords1 = self.find_letter_coords(matrix, pair[0])
            coords2 = self.find_letter_coords(matrix, pair[1])

            # Kiểm tra nếu ký tự không tìm thấy trong ma trận
            if coords1 is None or coords2 is None:
                raise ValueError(f"Ký tự '{pair[0] if coords1 is None else pair[1]}' không tìm thấy trong ma trận")

            row1, col1 = coords1
            row2, col2 = coords2

            # Quy tắc mã hóa Playfair
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]

            i += 2

        return encrypted_text