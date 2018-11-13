%conexiones en ambas direcciones
c(A,B,C,V) :- c0(A,B,C,V).
c(A,B,C,V) :- c0(B,A,C,V).
%--------------------------------------------
