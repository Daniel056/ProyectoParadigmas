%conexiones en ambas direcciones
c(A,B,C,V) :- c0(A,B,C,V).
c(A,B,C,V) :- c0(B,A,C,V).
%--------------------------------------------
vertices(V) :-
	findall(X,(c(X,_,_,_);c(_,X,_,_)),V).

ruta(A,B) :- ruta(A,B,_,_).
ruta(A,B,R,V) :- ruta(A,B,[],0,R,V).

ruta(Z,Z,R,V,R1,V) :- append(R,[Z],R1).

ruta(A,B,Ar,Av,R,V) :-
	A \= B, \+miembro(A,Ar),
	c(A,D,Cac,Vac),
	V1 is Av + Vac,
	append(Ar,[A],Br),
	ruta(D,B,Br,V1,R,V).

miembro(X,[X|_]).
miembro(X,[_|Xr]) :- miembro(X,Xr).


