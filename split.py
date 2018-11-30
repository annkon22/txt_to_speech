

def spl_inp(us_input):
    us_input = us_input.upper()
    us_split = []

    cons = 'BCDFGHJKLMPQRSTVWXYZ'
    vow = 'AEIOU'

    cur = 0
    nxt = 1
    
    while nxt <= len(us_input):
        for _ in us_input:
            if us_input[cur] in cons and us_input[nxt] in vow:
                syl = ''+ us_input[cur] + us_input[nxt] + 'n'
                cur = nxt + 1
            elif us_input[cur] in cons and us_input[nxt] in cons: 
                syl = '' + us_input[cur] + 'n'
                cur = nxt
            elif us_input[cur] in vow:
                syl = '' + us_input[cur] + 'n'
                cur = nxt
            elif us_input[cur] in cons and us_input[nxt] not in cons and us_input[nxt] not in vow:
                syl = '' + us_input[cur] + 'n'
                cur = nxt
            us_split.append(syl)
            nxt = cur + 1
    return(us_split)

my_input = input('Enter word or phrase: ')
print(spl_inp(my_input))
