# SOS Oyunu: 2 kişilik, sıra tabanlı terminal oyunu

def create_board(size):
    """Belirtilen boyutta boş bir oyun tahtası oluşturur."""
    return [[" " for _ in range(size)] for _ in range(size)]


def print_board(board):
    """Oyun tahtasını ekrana yazdırır."""
    size = len(board)
    print("  " + " ".join(str(i) for i in range(size)))  # Üstte sütun numaraları
    for i in range(size):
        print(str(i) + " " + " ".join(board[i]))  # Sol yanda satır numaraları


def check_sos(board, row, col, letter):
    """Tahtadaki belirli konumda SOS oluşturulup oluşturulmadığını kontrol eder."""
    size = len(board)
    sos_count = 0

    directions = [
        (-1, 0), (1, 0),   # dikey
        (0, -1), (0, 1),   # yatay
        (-1, -1), (1, 1),  # çapraz \
        (-1, 1), (1, -1)   # çapraz /
    ]

    for dr, dc in directions:
        try:
            # S harfi konulmuşsa kontrol: S - O - S
            if letter == "S":
                r1, c1 = row + dr, col + dc
                r2, c2 = row + 2 * dr, col + 2 * dc
                if 0 <= r1 < size and 0 <= c1 < size and 0 <= r2 < size and 0 <= c2 < size:
                    if board[r1][c1] == "O" and board[r2][c2] == "S":
                        sos_count += 1
            # O harfi konulmuşsa kontrol: S - O - S
            elif letter == "O":
                r1, c1 = row - dr, col - dc
                r2, c2 = row + dr, col + dc
                if 0 <= r1 < size and 0 <= c1 < size and 0 <= r2 < size and 0 <= c2 < size:
                    if board[r1][c1] == "S" and board[r2][c2] == "S":
                        sos_count += 1
        except IndexError:
            continue  # Tahta sınırlarını aşarsa geç

    return sos_count


def is_board_full(board):
    """Tahtada boş yer kalıp kalmadığını kontrol eder."""
    for row in board:
        if " " in row:
            return False
    return True


def play_game():
    size = 3  # Tahta boyutu
    board = create_board(size)
    scores = [0, 0]  # Oyuncu 1 ve 2'nin puanları
    player = 0       # 0 = Oyuncu 1, 1 = Oyuncu 2

    print("SOS Oyununa Hoşgeldiniz!")
    print("Oyuncular sırayla 'S' veya 'O' harfi koyacak.")
    print_board(board)

    while not is_board_full(board):
        print(f"\nOyuncu {player + 1}'in sırası")
        try:
            row = int(input(f"Satır (0-{size-1}): "))
            col = int(input(f"Sütun (0-{size-1}): "))
            if board[row][col] != " ":
                print("Bu hücre dolu! Başka bir yer seçin.")
                continue
            letter = input("Harf girin (S veya O): ").upper()
            if letter not in ("S", "O"):
                print("Hatalı giriş! Yalnızca S veya O olabilir.")
                continue

            board[row][col] = letter
            sos_formed = check_sos(board, row, col, letter)
            scores[player] += sos_formed

            print_board(board)
            print(f"Şu anki skor: Oyuncu 1 = {scores[0]} | Oyuncu 2 = {scores[1]}")

            # Eğer puan alındıysa tekrar oynar
            if sos_formed == 0:
                player = 1 - player  # Oyuncu değiştir

        except (ValueError, IndexError):
            print("Geçersiz giriş! Lütfen tekrar deneyin.")

    print("\nOyun bitti!")
    print(f"Final Skor: Oyuncu 1 = {scores[0]} | Oyuncu 2 = {scores[1]}")
    if scores[0] > scores[1]:
        print("🏆 Oyuncu 1 kazandı!")
    elif scores[1] > scores[0]:
        print("🏆 Oyuncu 2 kazandı!")
    else:
        print("🤝 Berabere!")


# Oyunu başlat
if __name__ == "__main__":
    play_game()
