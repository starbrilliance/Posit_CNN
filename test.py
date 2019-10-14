from Matrix import convert, func
from Posit import posit, quire


a = [
    [1.3, 0.8, 2.0],
    [10, 5.0, 0],
    [0, 3.0, 1.0]
]

b = convert.float2posit(a, 3, 3)
c = convert.posit2float(b, 3, 3)

out = 0.0

for i in range(0, 3):
    for j in range(0, 3):
        tmp = a[i][j] * a[i][j]
        out += tmp

print(out)

posit_out = func.posit_dot_mul(b, b, 3, 3)
print(posit_out.value_string())
posit_out_quire = func.posit_dot_mul(b, b, 3, 3, True)
print(posit_out_quire.to_float())
q2p = posit_out_quire.to_posit8_1()
print(q2p.value_string())

p1 = posit.PositN8E1(-2)
p2 = posit.PositN8E1(-3)
p3 = posit.PositN8E1(-2)
x = p1.fma(p2, p3)
print(x.value_string())
y = p1.fam(p2, p3)
print(y.value_string())

q1 = quire.QuireN8E1C14()
q1 += p1
print(q1.to_float())

