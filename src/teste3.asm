beq x0, x0, 10
10:
lh x7, 1(x2)
sh x7, 1(x2)
andi x6, x5, 32
sub x6, x6, x5
or x0, x5, x5
srl x6, x7, x5


