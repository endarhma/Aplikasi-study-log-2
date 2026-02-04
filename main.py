import datetime

catatan = []  # daftar berisi dict: {'mapel': str, 'topik': str, 'durasi': int, 'tanggal': 'YYYY-MM-DD'}


# Palet pastel (256-color) dan utilitas kecil untuk tampilan aesthetic

def _fg_code(n):
    return f"\033[38;5;{n}m"

def _bg_code(n):
    return f"\033[48;5;{n}m"

RESET = "\033[0m"
BOLD = "\033[1m"
# Warna-warna pastel (nuansa lembut)
FG_CYAN = _fg_code(159)       # pastel biru-cerah
FG_MAGENTA = _fg_code(183)    # pastel magenta/lavender
FG_YELLOW = _fg_code(228)     # pastel kuning
FG_GREEN = _fg_code(151)      # pastel hijau
FG_BLUE = _fg_code(153)       # pastel biru muda
FG_RED = _fg_code(203)        # pastel coral
FG_PEACH = _fg_code(215)      # pastel peach/soft

# Background lembut
BG_HEADER = _bg_code(189)
BG_ROW1 = _bg_code(254)
BG_ROW2 = _bg_code(251)
BG_ACCENT = _bg_code(224)


# Mode tampilan sederhana tanpa warna
SIMPLE_TABLE = True  # default: simple table (tanpa warna)


def toggle_color_mode():
    """Toggle SIMPLE_TABLE antara True/False dan tampilkan status sebagai tabel."""
    global SIMPLE_TABLE
    SIMPLE_TABLE = not SIMPLE_TABLE
    status = "Color: ON (warna aktif)" if not SIMPLE_TABLE else "Color: OFF (warna dimatikan)"
    headers = ['Status']
    rows_plain = [[status]]
    rows_display = [[_col(status)]]
    print(_render_table(headers, rows_plain, rows_display))


def _col(text, code=None):
    """Mengembalikan teks; jika SIMPLE_TABLE True, kembalikan tanpa kode warna.
    code bisa berupa kode ANSI atau kombinasi, tapi akan diabaikan di mode sederhana."""
    if SIMPLE_TABLE:
        return text
    return f"{code or ''}{text}{RESET}"


def _bar(value, max_value, width=20):
    """Buat progress bar; jika SIMPLE_TABLE True, kembalikan bar tanpa warna."""
    if max_value <= 0:
        return ""
    filled = int((value / max_value) * width)
    plain_bar = '█' * filled + '─' * (width - filled)
    if SIMPLE_TABLE:
        return plain_bar
    filled_part = _col("█" * filled, FG_BLUE + BG_ROW1)
    empty_part = _col('─' * (width - filled), FG_PEACH + BG_ROW2)
    return filled_part + empty_part


def render_menu_table():
    """Render menu sebagai tabel boxed (sederhana dan rapi)."""
    headers = ['Pilihan', 'Aksi']
    rows_plain = [
        ['1', '✨ Tambah catatan belajar'],
        ['2', '📚 Lihat catatan belajar'],
        ['3', '🕒 Total waktu belajar'],
        ['5', '📊 Ringkasan mingguan (pengembangan)'],
        ['6', '🎨 Toggle warna (On/Off)'],
        ['4', '✖️ Keluar'],
    ]
    # rows_display menggunakan plain text (emoji + label) sehingga tampil rapi tanpa warna
    rows_display = [list(r) for r in rows_plain]
    menu_box = _render_table(headers, rows_plain, rows_display, header_style=BOLD, align=['center', 'left'])
    print(menu_box)


def tambah_catatan():
    """Meminta input mapel, topik, durasi (menit) dan menyimpan ke list catatan."""
    print(f"\n{_col('✨ Tambah Catatan Belajar ✨', BOLD + FG_MAGENTA)}")
    while True:
        mapel = input(_col("Mapel: ", FG_YELLOW)).strip()
        if mapel:
            break
        print(_col("Mapel tidak boleh kosong. Silakan masukkan lagi.", FG_RED))

    while True:
        topik = input(_col("Topik: ", FG_YELLOW)).strip()
        if topik:
            break
        print(_col("Topik tidak boleh kosong. Silakan masukkan lagi.", FG_RED))

    while True:
        durasi_raw = input(_col("Durasi belajar (menit): ", FG_YELLOW)).strip()
        try:
            durasi = int(durasi_raw)
            if durasi <= 0:
                raise ValueError
            break
        except ValueError:
            print(_col("Masukkan durasi dalam angka menit, mis. 45. Harus > 0.", FG_RED))

    tanggal = datetime.date.today().isoformat()
    catatan_baru = {
        'mapel': mapel,
        'topik': topik,
        'durasi': durasi,
        'tanggal': tanggal,
    }
    catatan.append(catatan_baru)
    # Tampilkan konfirmasi sebagai tabel kecil
    headers = ['Status', 'Tanggal', 'Mapel', 'Topik', 'Durasi']
    rows_plain = [[ 'SUKSES', tanggal, mapel, topik, f"{durasi} m" ]]
    rows_display = [[ _col('✅ SUKSES', FG_GREEN), _col(tanggal, FG_BLUE), _col(mapel, FG_MAGENTA), _col(topik, FG_PEACH), _col(f"{durasi} m", BOLD + FG_GREEN) ]]
    print(_render_table(headers, rows_plain, rows_display))


def _render_table(headers, rows_plain, rows_display, header_style=BOLD + FG_YELLOW, align=None):
    """Renderer tabel boxed yang lebih rapi dan konsisten.
    - headers: list of header strings (plain)
    - rows_plain: list of rows (each row is list of plain strings for width calculation)
    - rows_display: list of rows (each row is list of display strings that may include ANSI codes)
    - align: optional list of 'left'/'right'/'center' per column
    """
    if align is None:
        align = ['left'] * len(headers)

    # hitung lebar kolom berdasarkan teks plain
    col_widths = [max(len(h), *(len(r[i]) for r in rows_plain)) for i, h in enumerate(headers)]

    # helpers untuk membuat garis
    def _line(left, mid, right):
        return left + mid.join('─' * (w + 2) for w in col_widths) + right

    top = _line('┌', '┬', '┐')
    sep = _line('├', '┼', '┤')
    bottom = _line('└', '┴', '┘')

    # header dengan background lembut dan teks rata tengah
    header_cells = []
    for i, h in enumerate(headers):
        content = h.center(col_widths[i])
        header_cells.append(' ' + _col(content, header_style + BG_HEADER) + ' ')
    header_line = '│' + '│'.join(header_cells) + '│'

    # rows (alternating background untuk keterbacaan)
    row_lines = []
    for idx, (plain_row, disp_row) in enumerate(zip(rows_plain, rows_display)):
        cells = []
        bg = BG_ROW1 if idx % 2 == 0 else BG_ROW2
        for i, (p, d) in enumerate(zip(plain_row, disp_row)):
            # alignment
            if align[i] == 'right':
                content_plain = p.rjust(col_widths[i])
            elif align[i] == 'center':
                content_plain = p.center(col_widths[i])
            else:
                content_plain = p.ljust(col_widths[i])

            # disp_row d mungkin sudah memiliki color codes; tambahkan bg for consistency
            cells.append(' ' + _col(d + (' ' * (col_widths[i] - len(p))), bg) + ' ')
        row_lines.append('│' + '│'.join(cells) + '│')

    # footer line for separation
    return '\n'.join([top, header_line, sep] + row_lines + [bottom])


def lihat_catatan():
    """Menampilkan semua catatan belajar sebagai tabel boxed yang aesthetic."""
    print(f"\n{_col('📚 Daftar Catatan Belajar', BOLD + FG_BLUE)}")
    if not catatan:
        headers = ['Info']
        msg = "Belum ada catatan belajar. Silakan tambahkan catatan dulu."
        rows_plain = [[msg]]
        rows_display = [[_col(msg, FG_RED)]]
        print(_render_table(headers, rows_plain, rows_display))
        return

    # siapkan rows
    max_durasi = max(c['durasi'] for c in catatan)
    headers = ['No', 'Tanggal', 'Mapel', 'Topik', 'Durasi', 'Progress', '']
    rows_plain = []
    rows_display = []

    for i, c in enumerate(catatan, start=1):
        plain_bar = _bar(c['durasi'], max_durasi, width=10).strip(RESET)
        # plain_bar masih berisi warna jika _bar dipakai; buat plain manual
        filled = int((c['durasi'] / max_durasi) * 10)
        plain_bar = '█' * filled + '─' * (10 - filled)

        emoji = '📝' if 'ujian' in c['topik'].lower() or 'tugas' in c['topik'].lower() else '🎯'

        plain_row = [str(i), c['tanggal'], c['mapel'], c['topik'], f"{c['durasi']} m", plain_bar, emoji]
        color = FG_CYAN if i % 2 == 1 else FG_MAGENTA
        disp_row = [
            _col(str(i), color),
            _col(c['tanggal'], color),
            _col(c['mapel'], color),
            _col(c['topik'], color),
            _col(f"{c['durasi']} m", BOLD + FG_GREEN),
            _col(plain_bar, FG_CYAN),
            emoji,
        ]
        rows_plain.append(plain_row)
        rows_display.append(disp_row)

    table = _render_table(headers, rows_plain, rows_display, align=['right','center','left','left','right','center','center'])
    print(table)

    total_menit = sum(c['durasi'] for c in catatan)
    print('\n' + _col(f"✨ Total sesi: {len(catatan)}  |  Total waktu: {total_menit} menit", BOLD + FG_BLUE))


def total_waktu():
    """Menghitung total durasi belajar dari semua catatan dan menampilkan estetis."""
    print(f"\n{_col('🕒 Total Waktu Belajar', BOLD + FG_BLUE)}")
    if not catatan:
        headers = ['Info']
        msg = "Belum ada catatan. Total waktu = 0 menit."
        rows_plain = [[msg]]
        rows_display = [[_col(msg, FG_RED)]]
        print(_render_table(headers, rows_plain, rows_display))
        return

    total_menit = sum(c['durasi'] for c in catatan)
    jam = total_menit // 60
    menit = total_menit % 60
    rincian = f"{jam} jam {menit} menit" if jam > 0 else f"{total_menit} menit"
    headers = ['Total Sesi', 'Total Menit', 'Rincian']
    rows_plain = [[str(len(catatan)), str(total_menit), rincian]]
    rows_display = [[_col(str(len(catatan)), FG_CYAN), _col(str(total_menit), FG_GREEN), _col(rincian, FG_YELLOW)]]
    print(_render_table(headers, rows_plain, rows_display))


# Fitur pengembangan mandiri: Ringkasan mingguan
def ringkasan_mingguan():
    """Menampilkan ringkasan untuk 7 hari terakhir: total menit, jumlah sesi, dan ringkasan per mapel sebagai tabel."""
    print(f"\n{_col('📊 Ringkasan Mingguan (7 hari terakhir)', BOLD + FG_MAGENTA)}")
    if not catatan:
        print(_col("Belum ada catatan. Tidak ada yang bisa diringkas.", FG_RED))
        return

    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=6)  # 7 hari termasuk hari ini

    catatan_minggu = [c for c in catatan if start_date <= datetime.date.fromisoformat(c['tanggal']) <= today]

    if not catatan_minggu:
        headers = ['Info']
        msg = "Tidak ada catatan dalam 7 hari terakhir."
        rows_plain = [[msg]]
        rows_display = [[_col(msg, FG_YELLOW)]]
        print(_render_table(headers, rows_plain, rows_display))
        return

    total_menit = sum(c['durasi'] for c in catatan_minggu)
    jumlah_sesi = len(catatan_minggu)

    # Ringkasan per mapel
    per_mapel = {}
    for c in catatan_minggu:
        per_mapel.setdefault(c['mapel'], 0)
        per_mapel[c['mapel']] += c['durasi']

    headers = ['Periode', 'Jumlah sesi', 'Total waktu']
    periode = f"{start_date.isoformat()} sampai {today.isoformat()}"
    rows_plain = [[periode, str(jumlah_sesi), f"{total_menit} m"]]
    rows_display = [[_col(periode, FG_BLUE), _col(str(jumlah_sesi), FG_CYAN), _col(f"{total_menit} menit", BOLD + FG_GREEN)]]
    print(_render_table(headers, rows_plain, rows_display))

    rows = sorted(per_mapel.items(), key=lambda x: x[1], reverse=True)

    headers = ['No', 'Mapel', 'Menit', '%', 'Progress']
    rows_plain = []
    rows_display = []
    max_m = rows[0][1]

    for i, (m, menit_mapel) in enumerate(rows, start=1):
        pct = int((menit_mapel / total_menit) * 100)
        filled = int((menit_mapel / max_m) * 20)
        plain_bar = '█' * filled + '─' * (20 - filled)
        emoji = '📚' if i == 1 else '🌈'

        plain_row = [str(i), m, str(menit_mapel), f"{pct}%", plain_bar]
        disp_row = [
            _col(str(i), FG_CYAN),
            _col(m, FG_MAGENTA),
            _col(str(menit_mapel), FG_GREEN),
            _col(f"{pct}%", FG_YELLOW),
            _col(plain_bar, FG_CYAN) + ' ' + emoji,
        ]
        rows_plain.append(plain_row)
        rows_display.append(disp_row)

    table = _render_table(headers, rows_plain, rows_display, align=['right','left','right','right','left'])
    print('\n' + table)


def menu():
    print()
    render_menu_table()
    print(_col("Pilih menu dengan memasukkan angka di kolom 'Pilihan' (mis. 1)", FG_PEACH))


while True:
    menu()
    pilihan = input(_col('Pilih menu: ', FG_YELLOW))

    if pilihan == "1":
        tambah_catatan()
    elif pilihan == "2":
        lihat_catatan()
    elif pilihan == "3":
        total_waktu()
    elif pilihan == "4":
        print(_col("Terima kasih, terus semangat belajar! 🎉", FG_GREEN))
        break
    elif pilihan == "5":
        ringkasan_mingguan()
    elif pilihan == "6":
        toggle_color_mode()
    else:
        print(_col("Pilihan tidak valid", FG_RED))