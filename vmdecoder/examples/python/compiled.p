
def f():
    a=1
    b=1
    c=1
    d=1
    e=1
    f=1
    g=1
    h=1
    i=1
    j=1
    k=1
    l=1
    m=1
    n=1
    o=1
    p=1
    q=1
    r=1
    s=1
    t=1
    u=1
    v=1
    w=1
    x=1
    y=1
    z=1
    print('end')
k = bytes([102,169,5,113,5,211,1,68,70,206,122,46,126,78,99,25,3,9,124,96,102,116,6,237,69,182,74,66,4,86,154,192,111,9,9,189,117,36,85,35,4,114,75,196,31,15,65,246,9,143,100,244,32,61,103,189,25,170,116,0,100,2,131,1,1,0,100,1,83,0])
v = f.__code__.replace(co_code=bytes(k))
#import dis
#bytecode = dis.Bytecode(f)
exec(v)