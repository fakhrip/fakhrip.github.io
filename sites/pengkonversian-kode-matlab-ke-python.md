Tags: Python|Programming
Times: 5 mins read
TLDR: Saya lebih prefer untuk memilih Python dibandingkan Matlab.
--+--+--+--
# Pengkonversian kode dari Matlab ke Python 

Sebenarnya, saya menulis artikel ini dengan tujuan ingin membagikan hal hal yang sudah saya dapatkan selama saya membantu salah satu teman saya untuk mengkonversi program yang sebelumnya ada di `Matlab` kedalam `Python` dengan alasan agar mempermudah dalam penambahan fitur dll (karena skill Matlab saya poor sekali XD).

Dalam proses mengkonversi saya menemukan beberapa hal yang menarik yang ada pada `Matlab` yang membuat saya semakin tidak menyukainya :v.

Salah satunya adalah fakta bahwa pada `Matlab`, array dimulai dari angka 1 (yeah, i know).

![what?!?!](https://media.giphy.com/media/8b9Xax6L7qtAkAimGm/giphy.gif)

Semua programmer yang sudah lama berkutat di dunia programming pasti keanehan dengan sebuah *weird quirk* yang dimiliki oleh `Matlab` ini.

Dan ada banyak hal lainnya yang saya secara pribadi karena datang dari bahasa bahasa pemrograman lainnya, merasa sedikit tidak nyaman saat ngoding di `Matlab`.

Dan sebenarnya juga semua kode yang dikonversi disini merupakan kode-kode yang sudah tersebar di internet dan mudah untuk dicari, akan tetapi saya tetap membuat artikel ini dengan tujuan lebih mempermudah pencarian kalian semuanya (looking at you code adventurer, i mean snippet explorer :v).

### So, lets convert 'em all

Disini saya akan langsung saja memberi tahu apa saja fungsi yang saya *convert*, sekaligus beberapa tautan ke website lainnya yang menurut saya punya resource yang sangat baik juga.

For a record, karena disini saya banyak menggunakannya fungsi fungsi yang berkaitan dengan **image processing**, beriringan dengan project yang saya bantu pada saat itu, jadi ya akan banyaknya fungsi tentang image processing.

Tanpa basa basi lanjut, berikut beberapa fungsi yang saya konversi :

**1. `find`**
  ```python
  def find(a, func, 
           amounts: int = 1, 
           position: str = "first") -> list:
    filtered = [i for i, val in enumerate(a) if func(val)]
    sorted_list = filtered[::-1] if position == "last" else filtered
    return sorted_list[0:amounts]
  ```
  Cara penggunaanya (Python) :
  ```python
  foo = find(bar, lambda x: x > 0)
  foo = find(bar, lambda x: x > 0, position="last")
  ```
  Ekuivalensi pada Matlab:
  ```matlab
  foo = find(bar > 0, 1, 'first');
  foo = find(bar > 0, 1, 'last');
  ```
  Seperti yang dilihat, pada `Matlab`, disitu ada angka `1` sebagai argumen kedua dari fungsi `find`, hal ini sudah saya buat default pada versi `Python` nya dan bisa diubah dengan cara memasukkan argumen `amounts` secara explisit pada pemanggilan fungsinya.

  Contoh :
  ```python
  foo = find(bar, lambda x: x > 0, amounts=2)
  foo = find(bar, lambda x: x > 0, amounts=2, position="last")
  ```
  Hal yang sama berlaku dengan argumen position juga.

**2. `imresize`**
  ```python
  def imresize(image: Image, 
               w: int = None, h: int = None):
    real_w, real_h = image.size

    image.thumbnail([w if w != None else real_w, 
                     h if h != None else real_h])

    return np.array(image)
  ```
  Cara penggunaanya (Python) :
  ```python
  from PIL import Image # install dengan `pip install pillow`
  image = imresize(Image.open(image_path), w=427)
  ```
  Ekuivalensi pada Matlab:
  ```matlab
  image = imresize(imread([image_path]), [427 NaN]);
  ```

**3. `imbinarize`**
  ```python
  def imbinarize(image: list(), multiplier: int = 1):
    from skimage.filters import threshold_otsu # install dengan `pip install scikit-image`

    thresh = threshold_otsu(image) * multiplier
    binary = image > thresh

    image_binarized = img_as_ubyte(binary)
    return image_binarized
  ```
  Cara penggunaanya (Python) :
  ```python
  image_binarized = imbinarize(img_gray, 0.7)
  ```
  Ekuivalensi pada Matlab:
  ```matlab
  image_binarized = im2bw(img_gray, (graythresh(img_gray) .* 0.7));
  ```

**4. `bwareaopen`**
  ```python
  def bwareaopen(image: list(), p, level: int = 100):
    from cv2 import cv2 # install dengan `pip install opencv-python`

    area = []

    # Find profile
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(image, contours, -1, (255, 255, 255), -1)
    len_contours = len(contours)

    for i in range(0, len_contours):
        area.append(cv2.contourArea(contours[i]))

    for i in range(0, len_contours):
        if area[i] < p:
            cv2.drawContours(image, contours, i, (0, 0, 0), -1)
        else:
            pass

    # Find profile
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (255, 255, 255), -1)

    # Returns the binarized image after removal of the target small area
    return image
  ```
  Cara penggunaanya (Python) :
  ```python
  image_clean = bwareaopen(image_binarized, 31337)
  ```
  Ekuivalensi pada Matlab:
  ```matlab
  image_clean = bwareaopen(image_binarized, 31337);
  ```

**5. `imfill`**
  ```python
  def imfill(image: list()):
    from cv2 import cv2 # install dengan `pip install opencv-python`

    # Copy the thresholded image.
    im_floodfill = image.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = image.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = image | im_floodfill_inv

    return im_out
  ```
  Cara penggunaanya (Python) :
  ```python
  image_filled = imfill(image_clean)
  ```
  Ekuivalensi pada Matlab:
  ```matlab
  image_filled = imfill(image_clean, 'holes');
  ```
  
### And another ~~one~~ many

Yang sudah saya tuliskan diatas hanya fungsi-fungsi saya konversi dari kode `Matlab`, akan tetapi sebenarnya ada banyak sekali kode yang saya konversi dalam bentuk pecahan pecahan kecil, jadi akan lebih baik jika dilihat sendiri dari beberapa referensi yang saya suguhkan berikut ini :

- http://mathesaurus.sourceforge.net/matlab-numpy.html (Matlab to NumPy cheatsheet)  
- https://www.mathworks.com/help/ (Matlab documentation itself)  
  Ini berguna untuk mengetahui algoritma dari tiap fungsi pada Matlab nya, agar bilapun kita tidak menemui *free real estate snippet* yang orang lain sudah buat, kita bisa implementasi sendiri berdasarkan algoritmanya.  
- https://scikit-image.org (Scikit Image documentation)  
  Disini biasanya sudah tertera banyak hal yang memang sudah kompatibel dengan fungsi yang ada pada Matlab, jadi bisa mempermudah untuk pengkonversian kode `Matlab` apapun itu.

  Anggap saja ini sebagai tambang emas yang menjadi harapan akhir saat otak pun sudah tidak mampu implementasi algo Matlabnya sendiri :(


Dan berikut ini adalah beberapa referensi yang saya gunakan untuk pembuatan fungsinya :

- https://stackoverflow.com/questions/5957470/matlab-style-find-function-in-python (find() Matlab in Python3)  
- https://www.learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/ (imfill holes in Python3)  
- https://programmersought.com/article/82182780880/ (bwareaopen in Python3)  
- https://note.nkmk.me/en/python-numpy-opencv-image-binarization/ (Python3 implementation of imbinarize and graythresh)  



### Last word

Semoga artikel nya mudah dipahami dan menyenangkan, jika memang dirasa bermanfaat silahkan sebarkan kepada yang lainnya agar ilmu nya tidak berhenti disini saja.

Terimakasih kepada Allah SWT dan juga para pembaca disini, semua yang buruk datangnya dari saya dan yang baik hanya datang dari-Nya, mohon maaf bila ada kesalahan 🙏.