import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.RailFence import Ui_MainWindow  # Điều chỉnh theo tên file UI đã sinh ra
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.Decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        """Gọi API mã hóa Rail Fence và hiển thị kết quả."""
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        key_text = self.ui.KeyText.toPlainText().strip()
        
        # Kiểm tra khóa có phải là số nguyên dương không
        try:
            key = int(key_text)
            if key <= 1:
                raise ValueError("Khóa phải lớn hơn 1")
        except ValueError:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa phải là một số nguyên dương lớn hơn 1.")
            return

        payload = {
            "plain_text": self.ui.PlainText.toPlainText().strip(),
            "key": key
        }

        if not payload["plain_text"]:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập văn bản gốc.")
            return

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.CipherText.setPlainText(data["encrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Mã hóa thành công")
                msg.exec_()
            else:
                print("Lỗi khi gọi API")
        except requests.RequestException as e:
            print(f"Lỗi: {str(e)}")

    def call_api_decrypt(self):
        """Gọi API giải mã Rail Fence và hiển thị kết quả."""
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        key_text = self.ui.KeyText.toPlainText().strip()
        
        # Kiểm tra khóa có phải là số nguyên dương không
        try:
            key = int(key_text)
            if key <= 1:
                raise ValueError("Khóa phải lớn hơn 1")
        except ValueError:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa phải là một số nguyên dương lớn hơn 1.")
            return

        payload = {
            "cipher_text": self.ui.CipherText.toPlainText().strip(),
            "key": key
        }

        if not payload["cipher_text"]:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập văn bản mã hóa.")
            return

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.PlainText.setPlainText(data["decrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Giải mã thành công")
                msg.exec_()
            else:
                print("Lỗi khi gọi API")
        except requests.RequestException as e:
            print(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())