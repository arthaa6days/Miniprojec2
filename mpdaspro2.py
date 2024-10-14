import uuid
from datetime import datetime
from prettytable import PrettyTable  


penggunaterdaftar = {
    'admin': {'password': 'lucky', 'role': 'admin'}  
}
tiketkonser = [] 
data_tiket = []  
penggunalogin = None  
stok_tiket = {'Exclusive': 0, 'Festival': 0}  

def register():
    username = input('Masukkan username: ')
    password = input('Masukkan password: ')

    if username in penggunaterdaftar:
        print("Username sudah terdaftar. Silakan login.")
    else:
        penggunaterdaftar[username] = {'password': password, 'role': 'user'}
        print('\n------ Registrasi berhasil! ------')
        login()


def login():
    global penggunalogin
    while True:
        username = input('Masukkan username: ')
        password = input('Masukkan password: ')

        if username in penggunaterdaftar and penggunaterdaftar[username]['password'] == password:
            penggunalogin = {'username': username, 'role': penggunaterdaftar[username]['role']}
            print(f'\nAnda berhasil login sebagai {username}')

            if penggunalogin['role'] == 'admin':
                menu_admin()
            else:
                menu_user()
            break
        else:
            print('Gagal login. Coba lagi.')

def pesanan(nama, jenistiket, jumlahtiket):
    jenistiket = jenistiket.title()
    if jenistiket not in ['Exclusive', 'Festival']:
        print("Jenis tiket tidak valid. Harus 'Exclusive' atau 'Festival'.")
        return

    if stok_tiket[jenistiket] < jumlahtiket:
        print(f"Stok {jenistiket} tidak mencukupi. Stok tersedia: {stok_tiket[jenistiket]}")
        return

    harga = jumlahtiket * (200000 if jenistiket == 'Exclusive' else 150000)
    stok_tiket[jenistiket] -= jumlahtiket
    waktupemesanan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pesanan_tiket = {
        'id': str(uuid.uuid4()),
        'nama': nama,
        'jenistiket': jenistiket,
        'jumlahtiket': jumlahtiket,
        'hargatiket': harga,
        'waktupemesanan': waktupemesanan
    }
    tiketkonser.append(pesanan_tiket)
    print(f"Tiket {jenistiket} untuk {nama} sebanyak {jumlahtiket} berhasil dipesan dengan total harga Rp{harga:,}.")
    print(f"Waktu pemesanan: {waktupemesanan}, ID Pesanan: {pesanan_tiket['id']}")


def tambah_stok():
    if penggunalogin and penggunalogin['role'] == 'admin':
        jenis_tiket = input("Masukkan jenis tiket yang ingin ditambah stoknya (Exclusive/Festival): ").title()
        try:
            jumlah_tambah = int(input("Masukkan jumlah tiket yang ingin ditambah: "))
            if jumlah_tambah <= 0:
                print("Jumlah tiket harus lebih dari 0.")
                return
        except ValueError:
            print("Jumlah tiket harus berupa angka yang valid.")
            return

        if jenis_tiket in stok_tiket:
            stok_tiket[jenis_tiket] += jumlah_tambah
            print(f"Stok tiket {jenis_tiket} berhasil ditambah. Stok sekarang: {stok_tiket[jenis_tiket]}")
        else:
            print("Jenis tiket tidak valid.")
    else:
        print("Anda tidak memiliki akses untuk menambah stok tiket.")


def lihat_stok():
    if penggunalogin and penggunalogin['role'] == 'admin':
        table = PrettyTable()
        table.field_names = ["Jenis Tiket", "Stok"]
        for jenis, stok in stok_tiket.items():
            table.add_row([jenis, stok])
        print(table)
    else:
        print("Anda tidak memiliki akses untuk melihat stok tiket.")

def tambah_data_tiket():
    if penggunalogin and penggunalogin['role'] == 'admin':
        jenis_tiket = input("Masukkan jenis tiket (Exclusive/Festival): ").title()
        harga = input("Masukkan harga tiket: ")
        data_tiket.append({'jenis': jenis_tiket, 'harga': harga})
        print(f"Data tiket {jenis_tiket} berhasil ditambahkan.")
    else:
        print("Anda tidak memiliki akses untuk menambah data tiket.")


def lihat_data_tiket():
    if data_tiket:
        table = PrettyTable()
        table.field_names = ["Jenis Tiket", "Harga"]
        for tiket in data_tiket:
            table.add_row([tiket['jenis'], tiket['harga']])
        print(table)
    else:
        print("Belum ada data tiket yang ditambahkan.")


def menu_admin():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Tambah Stok Tiket")
        print("2. Lihat Stok Tiket")
        print("3. Tambah Data Tiket")
        print("4. Keluar")

        pilihan = input("Pilih opsi (1-4): ")

        if pilihan == '1':
            tambah_stok()
        elif pilihan == '2':
            lihat_stok()
        elif pilihan == '3':
            tambah_data_tiket()
        elif pilihan == '4':
            print("Keluar dari menu admin.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def menu_user():
    while True:
        print("\n=== Menu Pengguna ===")
        print("1. Pesan Tiket")
        print("2. Lihat Data Tiket")
        print("3. Logout")

        pilihan = input("Pilih opsi (1-3): ")

        if pilihan == '1':
            if penggunalogin:
                nama = penggunalogin['username']
                jenistiket = input("Masukkan jenis tiket (Exclusive/Festival): ")
                try:
                    jumlahtiket = int(input("Masukkan jumlah tiket: "))
                    if jumlahtiket <= 0:
                        print("Jumlah tiket harus lebih dari 0.")
                        continue
                except ValueError:
                    print("Jumlah tiket harus berupa angka yang valid.")
                    continue

                pesanan(nama, jenistiket, jumlahtiket)
            else:
                print("\n[ALERT] Anda harus login terlebih dahulu untuk memesan tiket!")

        elif pilihan == '2':
            lihat_data_tiket()  
        elif pilihan == '3':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def menu():
    while True:
        print("\n=== Sistem Pemesanan Tiket ===")
        print("1. Register")
        print("2. Login")
        print("3. Keluar")

        pilihan = input("Pilih opsi (1-3): ")

        if pilihan == '1':
            register()
        elif pilihan == '2':
            login()
        elif pilihan == '3':
            print("Keluar dari sistem.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

menu()
