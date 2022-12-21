from Crypto.Cipher import AES
from Crypto.Random import new as Random
from hashlib import sha256
from base64 import b64encode,b64decode
import asn1

iv = b'\x00' * AES.block_size

class AESCipher:
  def __init__(self, data, key):
    self.data = data
    self.block_size = AES.block_size
    self.key = sha256(key.encode()).digest()[:32]
    self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr (self.block_size - len(s) % self.block_size)
    self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

  def encrypt(self):
    # Tạo mật mã mới AES256- mode CBC 
    plain_text = self.pad(self.data)
    cipher = AES.new(self.key, AES.MODE_CBC, iv)
    # Mã hóa, pad - đệm của một khối chưa hoàn chỉnh
    encrypttext = b64encode(iv + cipher.encrypt(plain_text.encode())).decode()
    # Chuyển đổi sang định dạng asn.1
    asn1_text = asn_encoderAES(len(encrypttext), encrypttext)
    return asn1_text

  def decrypt(self):
    parameters = []
    text = self.data
    decoder = asn1.Decoder()
    # Bắt đầu giải mã
    decoder.start(text)
    asn_decoderAES(decoder, parameters)
    encrypttext = text[-parameters[-1]:]
    cipher_text = b64decode(encrypttext)
    
    # Tạo mật mã mới AES256- mode CBC  
    cipher = AES.new(self.key, AES.MODE_CBC, iv)
    # Giải mã văn bản mã, giải mã - loại bỏ phần đệm của một khối chưa hoàn chỉnh
    decrypted = self.unpad(cipher.decrypt(cipher_text[self.block_size:])).decode()

    return bytes(decrypted, 'utf-8')
    

def asn_encoderAES(lenth, encrypted):
    encoder = asn1.Encoder()
    # Bắt đầu mã hóa
    encoder.start()
    # Dãy chính
    encoder.enter(asn1.Numbers.Sequence)
    # Bộ phím 
    encoder.enter(asn1.Numbers.Set)
    
    # Trình tự là khóa đầu tiên
    encoder.enter(asn1.Numbers.Sequence)
    # ID AES
    encoder.write(b'0x1082', asn1.Numbers.OctetString)
    # Kết thúc
    encoder.leave()
    
    # Thoát khỏi chuỗi khóa
    encoder.leave() 
    
    # Chuỗi dữ liệu tin nhắn được mã hóa
    encoder.enter(asn1.Numbers.Sequence)
    # Độ dài văn bản mã
    encoder.write(lenth, asn1.Numbers.Integer)
    # Nhập bản mã
    encoder.write(encrypted, asn1.Numbers.OctetString)
    # Thoát khỏi chuỗi dữ liệu
    encoder.leave()
    
    # Thoát khỏi chuỗi chính
    encoder.leave()
    
    return encoder.output()

def asn_decoderAES(decoder, parameters):
    while not decoder.eof():
        try:
            tag = decoder.peek()
            if tag.nr == asn1.Numbers.Null:
                break
            if tag.typ == asn1.Types.Primitive:
                tag, value = decoder.read()
                # Nếu là kiểu số nguyên
                if tag.nr == asn1.Numbers.Integer: 
                    # Thêm giá trị vào mảng
                    parameters.append(value)
            else:
                decoder.enter()
                asn_decoderAES(decoder, parameters)
                decoder.leave()

        except asn1.Error:
            break