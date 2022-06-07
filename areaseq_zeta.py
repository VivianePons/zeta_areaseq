from sage.combinat.dyck_word import DyckWords


def area_sequences(n):
    if n == 0:
        yield []
    elif n == 1:
        yield [0]
    else:
        for seq in area_sequences(n-1):
            for i in range(seq[-1]+2):
                yield seq + [i]

def insert(seq, pos):
    if pos == 0:
        return [0] + seq
    return seq[:pos] + [seq[pos-1] + 1] + seq[pos:]

def last_position(seq):
    amax = -1
    imax = -1
    inline = False

    #finding the last entry
    #it is one with maximal area
    #and on the left end of the right most group with this value
    for i in range(len(seq)-1,-1,-1):
        n = seq[i]
        if n == amax and inline:
            imax = i
        elif n > amax:
            amax = n
            imax = i
            inline = True
        else:
            inline = False

    return imax

def M_positions(seq):
    if len(seq) > 0:

        imax = last_position(seq)
        amax = seq[imax]

        # the inserts right after the max areas
        for i in range(len(seq)-1,-1,-1):
            n = seq[i]
            if n == amax:
                yield i+1

def Mprime_positions(seq):
    if len(seq) > 0:
        imax = last_position(seq)
        amax = seq[imax]

        # the inserts right after the max-1 areas on the right
        for i in range(len(seq)-1,imax,-1):
            n = seq[i]
            if n == amax-1:
                yield i+1

def admissible_insertion_positions(seq):

    if len(seq)==0:
        yield 0
        return

    imax = last_position(seq)
    amax = seq[imax]

    # the inserts right after the max areas
    for i in range(len(seq)-1,-1,-1):
        n = seq[i]
        if n == amax:
            yield i+1
    # the inserts right after the max-1 areas on the right
    for i in range(len(seq)-1,imax,-1):
        n = seq[i]
        if n == amax-1:
            yield i+1
    #the last insert, always at imax
    yield imax




def ungrow_area_seq(seq):

    imax = last_position(seq)
    amax = seq[imax]
    #counting the dinvs of the last entry
    dinv = -1
    for n in seq: # the one with equal areas
        if n == amax:
            dinv+=1
    for i in range(imax+1,len(seq)): # the ones on the right with area-1
        n = seq[i]
        if n == amax-1:
            dinv+=1

    newseq = seq[:imax] + seq[imax+1:]
    return newseq, dinv

def grow_area_seq(seq, dinv):
    for i,ci in enumerate(admissible_insertion_positions(seq)):
        if i == dinv:
            return insert(seq,ci)


def dinv_to_area(areaseq):
    dinvseq = []
    while(len(areaseq)>0):
        areaseq, d = ungrow_area_seq(areaseq)
        dinvseq.append(d)
    dinvseq.reverse()
    return dinvseq

def area_to_dinv(dinvseq):
    areaseq = []
    for d in dinvseq:
        areaseq = grow_area_seq(areaseq,d)
    return areaseq

def dw_dinv_to_area(dw):
    areaseq = dw.to_area_sequence()
    dinvseq = dinv_to_area(areaseq)
    return DyckWords().from_area_sequence(dinvseq)  # we interpret the dinvs as areas

def dw_area_to_dinv(dw):
    dinvseq = dw.to_area_sequence() # we take the area seq of dw and interpret it as dinvs
    areaseq = area_to_dinv(dinvseq)
    return DyckWords().from_area_sequence(areaseq)

def dinv(seq):
    return sum(sum(1 for w in seq[i+1:] if w == seq[i] or w == seq[i] - 1) for i in range(len(seq)-1))

def bounce_seq(seq):
    b = [0]
    for v in seq[1:]:
        if b[-1]+1 <= v:
            b.append(b[-1]+1)
        else:
            b.append(0)
    return b

def bounce(seq):
    bseq = bounce_seq(seq)
    n = len(bseq)
    b = 0
    for i in range(1,len(bseq)):
        if bseq[i] == 0:
            b+= n - (i+1) + 1
    return b
