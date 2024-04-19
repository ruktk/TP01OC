andi x6, x6, 7
sub x6, x6, x5
or x0, x5, x6
srl x0, x1, x6
beq x0, x0, 8
8:
lh x1, 4(x2)
sh x1, 8(x2)