import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.PlayFail import Ui_MainWindow  # Adjusted to match the UI file name
import requests
import json

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.Decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.KeyText.textChanged.connect(self.update_matrix)

    def update_matrix(self):
        """Update the Playfair matrix display when the key changes."""
        key = self.ui.KeyText.toPlainText().strip()
        if not key:
            self.ui.Matrix.setPlainText("")
            return

        url = "http://127.0.0.1:5000/api/playfair/creatematrix"
        payload = {"key": key}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                matrix = data["playfair_matrix"]
                # Format the matrix as a 5x5 grid for display
                matrix_text = "\n".join([" ".join(row) for row in matrix])
                self.ui.Matrix.setPlainText(matrix_text)
            else:
                self.ui.Matrix.setPlainText("Error generating matrix")
        except requests.RequestException as e:
            self.ui.Matrix.setPlainText(f"Error: {str(e)}")

    def call_api_encrypt(self):
        """Call the Playfair encrypt API and display the result."""
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        payload = {
            "plain_text": self.ui.PlainText.toPlainText().strip(),
            "key": self.ui.KeyText.toPlainText().strip()
        }

        if not payload["plain_text"] or not payload["key"]:
            QMessageBox.warning(self, "Input Error", "Please provide both plaintext and key.")
            return

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.CipherText.setPlainText(data["encrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.RequestException as e:
            print(f"Error: {str(e)}")

    def call_api_decrypt(self):
        """Call the Playfair decrypt API and display the result."""
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        payload = {
            "cipher_text": self.ui.CipherText.toPlainText().strip(),
            "key": self.ui.KeyText.toPlainText().strip()
        }

        if not payload["cipher_text"] or not payload["key"]:
            QMessageBox.warning(self, "Input Error", "Please provide both ciphertext and key.")
            return

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.PlainText.setPlainText(data["decrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.RequestException as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())