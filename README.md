# LazyPixels

A basic script that allows you to "encrypt" and "decrypt" a segmented image.

## Requirements
- Python 3.X
- Python package manager (pip)

## Setup
1. Create a virtualenviroment. (Optional)
2. Install dependencies: ```pip install -r requirements.txt```
3. Change ```IMAGE``` path.

## How it works

First, the script will generate a key used to encrypt the image. The length of the key is defined by the number of segments you want to have in your image. Each segment length is
defined by the constant ```SEGMENT_SIZE``` which defines the number of rows per segment. Each key segment will have a total amount of 13 digits. The first digit defines
which segment will it target and the next 12 hexadecimal digits composes the key.

### Encryption
The ```crypt``` method will iterate over the key segments in order to determine which digits interacts with each pixel. As an example, if we define a ```SEGMENT_SIZE``` of 50 
the segment with the segment target of 0 will interact with the first 50 rows of the image, segment target 1 will interact from the 51 row to the 100 row, etc.
Each key digit interacts with BGR values (opencv uses BGR instead of RGB) in this way:
1. Convert integer value of, for example, B, into a string and makes sure that the string length is equal to 3 appending required 0 to the left.
```
value_str = str(value)
while len(value_str) != 3:
  value_str = '0' + value_str
```
2. Add 0s to the key digit converted to decimal based on the index of the previous string. For example, if the key digit is 2, it will add 2 zeros to the key digit.
If the key digit exceeds the length of the string it will loop over the string cycling from 0 to 2 to determine the number of 0s.
```
index = 0
  for x in range(digits[digit]):
    index += 1
    if index == len(value_str):
      index = 0

  new_digit = digits[digit]
  for x in range(index):
    new_digit = new_digit * 10
```
3. Sum BGR value plus the previously created integer. If the result exceeds 255 (max value of BGR value) it will get the excess and sum it to 0 until the result is between 0 and 255.
Math formula representation to avoid loops:
```
n = (int(value_str) + new_digit) // 256
new_value = value + new_digit - 256 * n
```
4. Repeat that step over all BGR values until we have 3 values collected. With them collected, substitute the old BGR with the new one.

### Decryption
The ```decrypt``` method works the same way that ```crypt``` but in reverse. Thanks to the way of how segments works you can just input 2 key segments and it will just decrypt
that segments.

## Acknowledgements
- Thanks to Vicky and Zuleikarg for the help on ```crypt``` method.