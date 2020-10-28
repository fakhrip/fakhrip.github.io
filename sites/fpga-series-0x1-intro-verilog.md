Tags: Embedded-System|Series
Times: 5 mins read
TLDR: Verilog merupakan salah satu HDL yang dipakai untuk FPGA Programming
--+--+--+--
# FPGA Series: (0x1) Intro to Verilog 

Dimulai dari sekedar tugas kuliah yang tiba tiba datang dikala pandemi, tiba tiba saja saya terasa tertarik dan tertantang dengan yang namanya `embedded-system`, ketertarikan saya ini lebih terasa lagi disaat adanya mata kuliah yang berhubungan dengan FPGA yaitu **Sistem Chipset Tunggal**.

Setelah saya *crawling the internet* dalam beberapa hari, akhirnya saya menemukan kombinasi [tech-stack](https://mixpanel.com/topics/what-is-a-technology-stack/) yang menurut saya sangat pas apalagi mereka semua [open-source](https://id.wikipedia.org/wiki/Sumber_terbuka).

Maka dari itu saya membuat FPGA Series dalam blog saya ini untuk membagikan ilmu yang sudah saya dapatkan, sekaligus tempat untuk mengingat kembali hal-hal yang sudah saya pelajari sebelumnya (karena saya pelupa XD).

Without futher ado, let's get started...

### The series 

Series nya ini saya bentuk secara berurut menggunakan penomoran dalam bentuk hexadecimal (bagi yang belum tau) maka dari itu pada series pertama ini atau `series 0x1` saya mulai dengan pembahasan paling sederhana dan mudah-mudahan paling mudah dipahami.

`[Pendahuluan pada verilog]` -> berikut tertera ToC (Table of Content) dari artikel ini :  

| Pembahasan |
| --- |
| [Apa itu FPGA](#jadi-apa-itu-fpga) |  
| [Hubungan dengan Verilog](#tapi-apa-hubungannya-dengan-verilog) |  
| [Why Verilog ?](#why-verilog) |  
| [What's next ?](#whats-next) |  

<div id="jadi-apa-itu-fpga"></div>
### Jadi, apa itu FPGA ?

FPGA merupakan singkatan dari Field-Programmable Gate Array (so mouthful isnt it).

FPGA ini pada dasarnya merupakan persatuan dari banyak **gerbang logika (*logic gate*)** yang disatukan menjadi suatu hal yang dinamakan dengan **Logic Block**, dan karena FPGA ini programmable maka Logic Block nya ini juga **Configurable** yang dalam artian lain, FPGA ini menggunakan suatu hal yang disebut dengan [CLB(Configurable Logic Block)](https://www.ni.com/documentation/en/labview-comms/latest/fpga-targets/configurable-logic-blocks/) yang disatukan sedemikian rupa sehingga antar satu blok dengan lainnya saling ter-interkonesi.

![Hmm i think i know some of these words](https://media.giphy.com/media/KxhIhXaAmjOVy/giphy.gif)  
Yah, saya pun berekpresi sama saat pertama kali mendengar hal ini wkwk.

Jadi, intinya FPGA adalah blok berisi gerbang logika yang bisa kita konfigurasi sesuai kemauan kita sendiri.

<div id="tapi-apa-hubungannya-dengan-verilog"></div>
### Tapi, apa hubungannya dengan Verilog ?

TLDR; mereka punya hubungan yang kuat :v

Sebelum ke verilog, mari kita bahas terlebih dahulu tentang HDL(Hardware Description Language).

HDL Merupakan sebuah bahasa yang digunakan untuk mendeskripsikan suatu rangkaian elektronika maupun rangkaian logika.

Nah, Verilog merupakan salah satu HDL yang bisa kita gunakan untuk mem-program FPGA nya ini, dalam artian lain anggaplah FPGA ini sebagai sebuah arduino, maka bahasa C merupakan Verilog nya.

<div id="why-verilog"></div>
### Why Verilog ?

Sebenarnya ada beberapa bahasa yang bisa digunakan diantaranya adalah :  
- VHDL (Dibuat tahun 1983)  
- Verilog (Dibuat tahun 1984)  
- SystemC (Dibuat tahun 1999)  
- SystemVerilog (Dibuat tahun 2002)  
- [Dan masih banyak lagi](https://en.wikipedia.org/wiki/List_of_HDL_simulators)  

Bahkan sekarang sudah banyak yang buat [transpiler](https://devopedia.org/transpiler) dalam bentuk python, rust, java, dan bahasa bahasa lainnya.

Tapi, kenapa verilog ?

Sebenarnya alasannya cukup sederhana, karena ini diawali dengan tugas jadi ya saya terpaksa menggunakan bahasa yang disuruh oleh dosennya XD, walaupun bisa saja saya menggunakan python seperti yang saya sebutkan diatas lalu saya convert ke verilog menggunakan transpiler nya (More on this later).

<div id="whats-next"></div>
### What's next ?

Selanjutnya saya akan membahas **setup** dari beberapa tech-stack yang saya gunakan (yang pastinya open-source) untuk bisa **hands-on langsung** dengan yang namanya Verilog ini.

### Last word

Semoga artikel nya mudah dipahami dan menyenangkan, jika memang dirasa bermanfaat silahkan sebarkan kepada yang lainnya agar ilmu nya tidak berhenti disini saja.

Terimakasih kepada Allah SWT dan juga para pembaca disini, semua yang buruk datangnya dari saya dan yang baik hanya datang dari-Nya, mohon maaf bila ada kesalahan 🙏.