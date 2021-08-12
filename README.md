zbar-lite
----------

# This module is used to provide an easy to pack zbar python binding to wheel. And also provide some pythonic apis for users to use zbar easily. 

Only supports image related functions. 

For now , it is only designed for *Python*.


# How to build and install

## 1. get zbar
```
git clone https://github.com/mchehab/zbar.git
```
**It is recommended for you to run cmd below first to get the right config.h.**

```
cd zbar
autoreconf -vfi
./configure --without-java --without-gtk --without-qt  --without-imagemagick  --disable-video --without-python
```



## 2. copy the source file we need
```
sh preparation.sh
```
There are two template config.h in the `zbar_lite/config_template` . 

if you did not generate a config.h, we will copy one of them to `./src` according to your OS when setup.



*Before build, you should make sure that your gcc compiler is fit with your OS.*

you can install gcc build env from `https://sourceforge.net/projects/mingw-w64/files/` for windows

*Notice that mingw64 and mingw-w64 is not the same thing.*

It is recommended for you to install setuptools to install and build.

```
pip install setuptools wheel
```
### Windows
I select `x86_64-posix-seh-rev0` to build my wheel on Windows.

```
python setup.py build -c mingw32
```

to build whl
```
python setup.py build -c mingw32 bdist_wheel
```

to install
```
python setup.py build -c mingw32 install
```

### Linux

to build whl
```
CC="gcc -std=gnu99" python setup.py bdist_wheel
```

to install
```
CC="gcc -std=gnu99" python setup.py install
```

## Some errors you could meet:

### 1. Cannot find -lmsvcr140

if you build this whl in Windows with `python setup.py build_ext --compiler=mingw32`, 
you may meet an error that `cannot find -lmsvcr140`, as you can see in <https://stackoverflow.com/questions/43873604/where-is-msvcr140-dll-does-it-exist>.

*I fixed it in the setup.py*

### 2. Should be build by std99 or gnu99
```
CC="gcc -std=gnu99" python setup.py bdist_wheel
```
### 3. Do not support inverted Code
When the background is darker than the QR Code's foreground, it's called an inverted Code. 
These types of Codes typically have a dark background such as black, navy or dark grey. 
While a few scanners can read an inverted Code, some apps are not able to scan them including us.

### 4. Can not detect the barcode
You can do some preprocess before decoding it.  
It is recommended for you to try the ways below:
1. Turn it to gray
2. Split the color channel, such as use the ```b or g or r``` channel separately
# How to use
### *We provide several versions of whl right now. You can try to install via `pip install zbar-lite`.*

#### example1

```
import zbar
import cv2

img_path='./test.jpg'

# create a reader
scanner = zbar.ImageScanner()

# configure the reader
scanner.parse_config('enable')

# obtain image data
pil = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
height, width = pil.shape[:2]
raw = pil.tobytes()

# wrap image data
image = zbar.Image(width, height, 'Y800', raw)

# scan the image for barcodes
scanner.scan(image)

# extract results
for symbol in image:
    # do something useful with results
    print('decoded', symbol.type, 'text', '"%s"' % symbol.data)
    print('type {} text {} location {} quality {}'.format( symbol.type, symbol.data,symbol.location,symbol.quality))

# clean up
del(image)
```
#### example2
```
from zbar_helper.utils import decode, show_info
import cv2
image_path = "test.png"
img = cv2.imread(image_path)
print(decode(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)))
show_info(decode(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)), img)
```
# For more documents you can visit <https://github.com/mchehab/zbar/tree/master/python> 
