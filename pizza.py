key = "gdscisawayoflifenotjustanotherclub"
msg_raw = b"\x1a\x03\x17\x10\n\x082\x1f\x14?)\n\t62\r]07Z\x11@\x07"

for m, k in zip(msg_raw, key):
    print(chr(m ^ ord(k)), end="")
print()
