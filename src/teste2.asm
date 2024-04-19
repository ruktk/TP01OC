
andi x6, x5, 15
sub x6, x6, x5
or x0, x5, x5
srl x0, x1, x5
beq x0, x0, 6
6:
lh x1, 1(x2)
sh x1, 1(x2)
