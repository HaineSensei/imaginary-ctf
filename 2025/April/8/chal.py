flag = 'ictf{REDACTED}'

allowed_characters = set([i for i in "1234567890a+-*&|^ ()<>"])

def main():
    try:
        expr_1 = str(input("enter your first expression): "))
        
        for i in expr_1:
            if i not in allowed_characters:
                print("Illegal character found")
                exit(1)
                
        expr_2 = str(input("enter your second expression): "))
        
        for i in expr_2:
            if i not in allowed_characters:
                print("Illegal character found")
                exit(1)
        
        for initial in range(16):
            a = initial
            encoded = eval(expr_1) & 127
            
            for error in range(8):
                a = (encoded ^ (1 << error)) & 127
                decoded = eval(expr_2)
                if (decoded != initial):
                    print("thats not correct")
                    exit(1)
        print(flag)
    except:
        print("Don't try and break me >:V")
        exit(1)
        
        
if __name__ == "__main__":
    main()
