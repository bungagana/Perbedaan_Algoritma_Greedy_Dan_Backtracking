#--------------------- LIBRARY ---------------------------------
import streamlit as st
import random
from streamlit_option_menu import option_menu
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from graphviz import Digraph
import numpy as np
import time

#### ----- NAVIGATION BAR ---- ####
selected = option_menu(
    menu_title="Perbandingan Algoritma Shortest Path",
    options=["Greedy",  "Backtracking"],
    orientation="horizontal",  # Mengubah orientasi menu menjadi vertikal
    styles={
        "container": {"padding": "0!important", "background-color": "black"},
        "nav-link": {
            "font-size": "15px",
            "font-colour": "white",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eeeee",
        },
        "nav-link-selected": {"background-color": "#696666"},
    },
)

#### ----- SECTION HOME ---- ####
if selected == "Greedy":
    # Definisi matriks jarak antar ruangan
    jarak = [
        [0, 5, 7, 3, float('inf')],  # A: [A, B, C, D, E]
        [5, 0, 4, float('inf'), 3],  # B: [A, B, C, D, E]
        [7, 4, 0, float('inf'), 5],  # C: [A, B, C, D, E]
        [3, float('inf'), float('inf'), 0, 4],  # D: [A, B, C, D, E]
        [float('inf'), float('inf'), 5, 4, 0]  # E: [A, B, C, D, E]
    ]

    # Fungsi untuk memilih ruangan selanjutnya berdasarkan jarak terdekat
    def pilih_ruangan_greedy(ruangan_sekarang, ruangan_tersedia):
        jarak_minimal = float('inf')
        ruangan_selanjutnya = None

        for ruangan in ruangan_tersedia:
            jarak_ruangan = jarak[ruangan_sekarang][ruangan]
            if jarak_ruangan is not None and jarak_ruangan < jarak_minimal:
                jarak_minimal = jarak_ruangan
                ruangan_selanjutnya = ruangan

        return ruangan_selanjutnya

    # Algoritma greedy
    def optimisasi_greedy():
        solusi = [0]  # Ruangan awal A
        jarak_total = 0
        ruangan_sekarang = 0  # Ruangan awal

        ruangan_tersedia = list(range(1, len(jarak)))

        while ruangan_tersedia:
            ruangan_selanjutnya = pilih_ruangan_greedy(ruangan_sekarang, ruangan_tersedia)
            if ruangan_selanjutnya is None:
                break
            solusi.append(ruangan_selanjutnya)
            jarak_total += jarak[ruangan_sekarang][ruangan_selanjutnya]

            ruangan_tersedia.remove(ruangan_selanjutnya)
            ruangan_sekarang = ruangan_selanjutnya

        jarak_total += jarak[ruangan_sekarang][0]  # Kembali ke ruangan A
        solusi.append(0)  # Menambahkan ruangan A ke solusi

        return solusi, jarak_total

    # Menjalankan algoritma greedy
    start_time = time.time()
    solusi_greedy, jarak_greedy = optimisasi_greedy()
    end_time = time.time()
    execution_time = end_time - start_time

    # Menampilkan hasil greedy
    st.header("Hasil Optimasi Greedy:")
    st.caption ("Jika pasien ingin melewati semua ruangan dengan titik awal dari A maka ruangan yang harus dilwati terlebih dulu adalah spt dibawah ini: ")
    st.write([chr(ruangan + ord('A')) for ruangan in solusi_greedy])
    st.write("Jarak Terbaik (Greedy):", jarak_greedy)
    st.write("Waktu Eksekusi:", execution_time, "detik")
    st.markdown("---")
    st.header("Hasil Pemilihan Jalur Terpendek Dari Ruang A ke Ruang B")

elif selected == "Backtracking":
    # Definisi matriks jarak antar ruangan
    jarak = [
        [0, 5, 7, 3, float('inf')],  # A: [A, B, C, D, E]
        [5, 0, 4, float('inf'), 3],  # B: [A, B, C, D, E]
        [7, 4, 0, float('inf'), 5],  # C: [A, B, C, D, E]
        [3, float('inf'), float('inf'), 0, 4],  # D: [A, B, C, D, E]
        [float('inf'), float('inf'), 5, 4, 0]  # E: [A, B, C, D, E]
    ]
    # Algoritma backtracking
    def optimisasi_backtracking(ruangan_sekarang, ruangan_tersedia, jarak_total, solusi):
        if not ruangan_tersedia:
            jarak_total += jarak[ruangan_sekarang][0]  # Kembali ke ruangan A
            solusi.append(0)  # Menambahkan ruangan A ke solusi
            return jarak_total, solusi

        jarak_minimal = float('inf')
        ruangan_selanjutnya = None

        for ruangan in ruangan_tersedia:
            jarak_ruangan = jarak[ruangan_sekarang][ruangan]
            if jarak_ruangan is not None and jarak_ruangan < jarak_minimal:
                jarak_minimal = jarak_ruangan
                ruangan_selanjutnya = ruangan

        ruangan_tersedia.remove(ruangan_selanjutnya)
        solusi.append(ruangan_selanjutnya)
        jarak_total += jarak[ruangan_sekarang][ruangan_selanjutnya]

        jarak_total, solusi = optimisasi_backtracking(
            ruangan_selanjutnya, ruangan_tersedia, jarak_total, solusi
        )

        return jarak_total, solusi

   # Menjalankan algoritma backtracking
    start_time = time.time()
    solusi_backtracking = []
    jarak_backtracking, solusi_backtracking = optimisasi_backtracking(
        0, list(range(1, len(jarak))), 0, solusi_backtracking
    )
    end_time = time.time()
    execution_time = end_time - start_time

    # Menampilkan hasil backtracking
    st.header("Hasil Optimasi Backtracking:")
    st.caption("Jika pasien ingin melewati semua ruangan dengan titik awal dari A maka ruangan yang harus dilwati terlebih dulu adalah spt dibawah ini: ")
    st.write(['A'] + [chr(ruangan + ord('A')) for ruangan in solusi_backtracking])  # Add 'A' at the beginning of the sequence
    st.write("Jarak Terbaik (Backtracking):", jarak_backtracking)
    st.markdown("---")
    st.header("Hasil Pemilihan Jalur Terpendek Dari Ruang A ke Ruang B")
# Fungsi untuk mencari rute terpendek dengan algoritma Backtracking
def backtracking_algorithm(graph, start, end, path, shortest_path, shortest_distance, current_distance):
    # Menambahkan simpul saat ini ke dalam path
    path.append(start)

    # Menampilkan rute yang sedang dijelajahi
    st.write("Rute saat ini:", ' -> '.join(path))

    # Jika sudah mencapai simpul tujuan
    if start == end:
        # Memeriksa apakah rute saat ini lebih pendek dari rute terpendek yang sudah ditemukan
        if current_distance < shortest_distance[0]:
            shortest_distance[0] = current_distance
            shortest_path[0] = path[:]
        return

    # Melanjutkan ke simpul tetangga yang belum dikunjungi
    for neighbor, distance in graph[start].items():
        if neighbor not in path:
            # Memanggil rekursif untuk menjelajahi rute berikutnya
            backtracking_algorithm(graph, neighbor, end, path, shortest_path, shortest_distance, current_distance + distance)

    # Menghapus simpul saat ini dari path untuk kembali ke level sebelumnya
    path.pop()

# Fungsi utama
def main():
    # Graph berisi jarak antara setiap simpul
    graph = {
        'A': {'D': 3},
        'D': {'A': 3, 'C': 4},
        'E': {'C': 5},
        'C': {'B': 4, 'A': 7},
        'B': {'A': 5}
    }

    start_node = 'A'
    end_node = 'B'

    # Inisialisasi variabel untuk menyimpan rute terpendek
    shortest_path = [None]
    shortest_distance = [float('inf')]

    # Tombol untuk memulai pencarian rute terpendek
    if st.button("Cari Rute Terpendek"):
        # Mencatat waktu awal
        start_time = time.time()

        # Memanggil algoritma Backtracking untuk mencari rute terpendek
        backtracking_algorithm(graph, start_node, end_node, [], shortest_path, shortest_distance, 0)

        # Menambahkan simpul awal ke rute terpendek (untuk kembali ke node A)
        shortest_path[0].append(start_node)

        # Menghitung jarak total rute terpendek
        total_distance = sum(graph[node1][node2] for node1, node2 in zip(shortest_path[0], shortest_path[0][1:]))

        # Mencatat waktu akhir dan menghitung waktu eksekusi
        end_time = time.time()
        execution_time = end_time - start_time

        # Menampilkan hasil
        if shortest_path[0]:
            st.write("\nRute terpendek:", ' -> '.join(shortest_path[0]))
            st.write("Jarak terpendek:", total_distance)
            st.write("Waktu eksekusi:", execution_time, "detik")
        else:
            st.write("\nTidak ada rute yang tersedia.")

if __name__ == '__main__':
    main()

