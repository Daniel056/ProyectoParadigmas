%conexiones en ambas direcciones
c(A,B,C,V) :- c0(A,B,C,V).
c(A,B,C,V) :- c0(B,A,C,V).
%------------------------------------------------

% 1)
conexion(A,B) :- ruta(A,B,_,_,_).

% 2)
conexion(A,B,R):-ruta(A,B,R,_,_).

% 3)
velocidad_maxima(A,B,R,V):- ruta(A,B,R,_,V).

% 4)
velocidad_maxima(A,B,V) :- 
	findall(V1,ruta(A,B,_,_,V1),X),
	min(X,V).

% 5)
confiabilidad(A,B,R,C):-
	ruta(A,B,R,C,_).
%------------------------------------------------
%Métodos auxiliares
%------------------------------------------------

%Encuentra ruta entre A y B y su velocidad maxima
ruta(A,B,R,C,V) :- ruta(A,B,[],0,0,R,C,V).
ruta(Z,Z,R,C,V,R1,C,V) :- append(R,[Z],R1).

ruta(A,B,[],0,0,R,C,V):-
	A \= B,
	c(A,D,Cac,Vac),
	B == D,
	append([],[A],Br),
	ruta(D,B,Br,Cac,Vac,R,C,V).

ruta(A,B,[],0,0,R,C,V):-
	A \= B,
	c(A,D,Cac,Vac),
	B \= D,
	\+cliente(D),
	append([],[A],Br),
	ruta(D,B,Br,Cac,Vac,R,C,V).
	
ruta(A,B,Ar,Ac,Av,R,C,V) :-
	A \= B, \+miembro(A,Ar),
	c(A,D,Cac,Vac),
	B == D,
	>(Av,0),
	C1 is Ac * Cac,
	min(Av,Vac,V1),
	append(Ar,[A],Br),
	ruta(D,B,Br,C1,V1,R,C,V).
	
ruta(A,B,Ar,Ac,Av,R,C,V) :-
	A \= B, \+miembro(A,Ar),
	c(A,D,Cac,Vac),
	B \= D,
	\+cliente(D),
	>(Av,0),
	C1 is Ac * Cac,
	min(Av,Vac,V1),
	append(Ar,[A],Br),
	ruta(D,B,Br,C1,V1,R,C,V).
%------------------------------------------------

% Verifica si ya se revisó una ruta especifica
miembro(X,[X|_]).
miembro(X,[_|Xr]) :- miembro(X,Xr).
%------------------------------------------------

% Devuelve el menor de 2 números
min(X,Y,M):-
	>(X,Y),
	M is Y,!.
min(X,Y,M):-
	>(Y,X),
	M is X,!.
%------------------------------------------------

% Devuelve el menor de una lista
min([X|Xr],M):-
	list_min(X,Xr,M).

list_min(M,[],M):-!.
list_min(Y,[L|Lr],X):-
	L >= Y,
	!,
	list_min(Y,Lr,X).
list_min(Y,[L|Lr],X):-
	L =< Y,
	list_min(L,Lr,X).
%------------------------------------------------