import base64,zlib,os
from lxml import etree

"""
If you don't know much about GD saves and where they are stored, here's your explanation:
Xor (the first function) takes the binary bits of the data in the file and does a Exclusive-OR logic comparison for every bit and then returns the output.
    Exclusive-OR is a gate that returns 0 if both bits are 0 (in this case 1 bit each of the file and the key) and 1 ONLY if ONE of the bits is on.
For example, XOR(1,1) would return 0 because both bits are on, and XOR(1,0) would return 1 because ONLY ONE bit is on (or equal to one).
Using this data, we can form a truth table, or every possible combination and output graphed onto a grid.
2^2 (2 combinations^2 combinations) is how many combinations we will get.
So,
XOR(0,0) = 0
XOR(1,0) = 1
XOR(0,1) = 1
XOR(1,1) = 0

That's all the XOR function does.

Next, the Decrypt(data) function.
This function converts the encoded base-64 to a decrypted, more readable but not perfect XML format. It first decompresses the weird .dat file and converts it into
base-62 with "-" and "=" (aka what I call YouTube Base-64 because it's the format for youtube's video URLs) which is then converted to regular Base-62 with "+" and
"/", aka regular base-64.

This base-64 can then be converted to the UTF-8 format by the base64.b64decode function.

The function local_levels() gets the local levels via Xor(path,key) and Decrypt(data) and retrieves a .txt version.

The function prettify(xmlfile) takes a XML (eXtensible Markup Language) file and makes it look nicer via the LXML library (libxml).

Finally, the function pretty_local_levels(filename) takes local_levels and converts it into a nicer-looking version and outputs it to the filename.

If you read all of this, WOW you're a nerd.
Just kidding, thank you.
"""

saves = ['CCGameManager.dat','CCLocalLevels.dat']
 
def Xor(path,key):
    with open(path,'rb') as fr:
        data = fr.read()
   
    res = []
    [res.append(i^key) for i in data]
    
    return bytearray(res).decode()
 
def Decrypt(data):
    return zlib.decompress(base64.b64decode(data.replace('-','+').replace('_','/').encode())[10:],-zlib.MAX_WBITS)
 
def local_levels():
    for x in range(2):
        fPath = os.getenv('localappdata')+'\\GeometryDash\\'
        res = Xor(fPath+saves[x],11)
        fin = Decrypt(res)
     
        with open(saves[x]+'.txt','wb') as fw:
            fw.write(fin)

def prettify(xmlfile):
    return etree.tostring(etree.parse(xmlfile), encoding="unicode", pretty_print=True)

def pretty_local_levels(filename):
    local_levels()
    with open(filename, "w") as file:
        file.write(prettify("CCLocalLevels.dat.txt"))
