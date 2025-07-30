import tkinter as tk  # Grafik arayüz oluşturmak için tkinter kütüphanesini içe aktarıyoruz
from tkinter import messagebox  # Bilgi kutusu göstermek için
import random  # Rastgele kelime seçimi için kullanılır

# Oyun için örnek kelimeler listesi
WORD_LIST = ["PYTHON", "BILGISAYAR", "PROGRAMLAMA", "KOD", "GELISTIRICI", "VERITABANI", "ALGORITMA"]

# Ana sınıf: Adam Asmaca Oyunu
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Adam Asmaca Oyunu")

        # Rastgele bir kelime seçilir ve harf tahminleri takip edilir
        self.word = random.choice(WORD_LIST)
        self.guessed = set()  # Tahmin edilen harfleri tutar
        self.max_tries = 6  # En fazla 6 yanlış hak
        self.wrong_guesses = 0  # Başlangıçta yanlış tahmin sıfır

        # Arayüz elemanlarını başlat
        self.create_ui()

    # Arayüz oluşturma fonksiyonu
    def create_ui(self):
        # Çizim alanı: Adamı çizeceğimiz tuval
        self.canvas = tk.Canvas(self.root, width=200, height=250)
        self.canvas.pack(pady=10)
        self.draw_gallow()  # İskelet (gallows) çizilir

        # Tahmin edilen kelimeyi gösteren label (örnek: _ _ _ _ _)
        self.word_label = tk.Label(self.root, text=self.get_display_word(), font=("Courier", 24))
        self.word_label.pack(pady=10)

        # Harf girişi için giriş kutusu
        self.entry = tk.Entry(self.root, font=("Helvetica", 16), width=5, justify="center")
        self.entry.pack()
        self.entry.bind("<Return>", self.guess_letter)  # Enter tuşu ile tahmin yapılır

        # Bilgi etiketi
        self.info_label = tk.Label(self.root, text="Bir harf gir ve Enter'a bas", font=("Helvetica", 12))
        self.info_label.pack(pady=5)

        # Tahmin edilen harflerin listelendiği alan
        self.guessed_label = tk.Label(self.root, text="Tahmin edilenler: ", font=("Helvetica", 12))
        self.guessed_label.pack()

    # Ekranda görünen kelimeyi hazırlar (örnek: P _ T H O N)
    def get_display_word(self):
        return " ".join([letter if letter in self.guessed else "_" for letter in self.word])

    # Harf tahmini yapıldığında çalışacak fonksiyon
    def guess_letter(self, event):
        # Giriş kutusundan harfi al, büyük harfe çevir, temizle
        letter = self.entry.get().strip().upper()
        self.entry.delete(0, tk.END)

        # Geçersiz giriş kontrolü: sadece 1 harf ve alfabetik olmalı
        if not letter.isalpha() or len(letter) != 1:
            self.info_label.config(text="Lütfen sadece bir harf gir.")
            return

        # Aynı harf tekrar girildiyse uyarı ver
        if letter in self.guessed:
            self.info_label.config(text="Bu harfi zaten denedin.")
            return

        self.guessed.add(letter)  # Harfi tahmin edilenlere ekle

        # Harf doğruysa kelimeyi güncelle
        if letter in self.word:
            self.word_label.config(text=self.get_display_word())
            self.info_label.config(text="Doğru tahmin!")
        else:
            # Yanlış tahmin: çizimi güncelle
            self.wrong_guesses += 1
            self.draw_next_part()
            self.info_label.config(text="Yanlış tahmin!")

        # Tahmin edilen harfleri güncelle
        self.guessed_label.config(text="Tahmin edilenler: " + ", ".join(sorted(self.guessed)))

        # Kazanma durumu kontrolü
        if "_" not in self.get_display_word():
            self.end_game(True)
        # Kaybetme durumu kontrolü
        elif self.wrong_guesses >= self.max_tries:
            self.end_game(False)
# Adam Asmaca Oyunu
    
    # Oyun bittiğinde çalışacak fonksiyon
    def end_game(self, won):
        if won:
            messagebox.showinfo("Tebrikler!", f"Tebrikler, kazandın! 🎉\nKelime: {self.word}")
        else:
            self.word_label.config(text=" ".join(self.word))  # Kelimeyi göster
            messagebox.showinfo("Oyun Bitti", f"Kaybettin! 😞\nKelime: {self.word}")
        self.root.quit()  # Programı kapat

    # Direği (gallow) çizen fonksiyon – sabit yapı
    def draw_gallow(self):
        self.canvas.create_line(50, 230, 150, 230)  # taban
        self.canvas.create_line(100, 230, 100, 50)  # dik direk
        self.canvas.create_line(100, 50, 160, 50)   # üst çubuk
        self.canvas.create_line(160, 50, 160, 70)   # ip

    # Her yanlış tahminde sırayla vücut parçası çizen fonksiyon
    def draw_next_part(self):
        parts = [
            lambda: self.canvas.create_oval(140, 70, 180, 110),       # kafa
            lambda: self.canvas.create_line(160, 110, 160, 160),      # gövde
            lambda: self.canvas.create_line(160, 120, 140, 140),      # sol kol
            lambda: self.canvas.create_line(160, 120, 180, 140),      # sağ kol
            lambda: self.canvas.create_line(160, 160, 140, 190),      # sol bacak
            lambda: self.canvas.create_line(160, 160, 180, 190),      # sağ bacak
        ]
        # Hatalı tahmin sayısına göre çizim yapılır
        if self.wrong_guesses <= self.max_tries:
            parts[self.wrong_guesses - 1]()  # Örneğin 1. yanlışsa kafa çizilir

# Uygulama başlatılıyor
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
