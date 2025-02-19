from time import sleep
text = input("Who do you want erased?")
text += " "
i = len(text)
while not all(text[i]==" " for i in range(len(text))):
    text = text[:i-1]+" "+text[i:]
    print(f"\r  {text}",end = "")
    sleep(1)
    i -= 1
print()
    