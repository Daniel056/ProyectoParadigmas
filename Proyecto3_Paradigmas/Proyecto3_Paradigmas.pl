%conexiones en ambas direcciones
c(A,B,C,V) :- c0(A,B,C,V).
c(A,B,C,V) :- c0(B,A,C,V).
%--------------------------------------------
% 1)
conexion(A,B) :- ruta(A,B,_,_).

% 2)
conexion(A,B,R):-ruta(A,B,R,_).

% 3)
velocidad_maxima(A,B,R,V):- ruta(A,B,R,V).

% 4)
velocidad_maxima(A,B,V) :- 
	findall(V1,ruta(A,B,_,V1),X),
	min(X,V).
%------------------------------------------------
%Métodos auxiliares
%------------------------------------------------

%Encuentra ruta entre A y B y su velocidad maxima
ruta(A,B,R,V) :- ruta(A,B,[],0,R,V).
ruta(Z,Z,R,V,R1,V) :- append(R,[Z],R1).

ruta(A,B,[],0,R,V):-
	A \= B,
	c(A,D,_,Vac),
	append([],[A],Br),
	ruta(D,B,Br,Vac,R,V).
	
ruta(A,B,Ar,Av,R,V) :-
	A \= B, \+miembro(A,Ar),
	c(A,D,_,Vac),
	>(Av,0),
	min(Av,Vac,V1),
	append(Ar,[A],Br),
	ruta(D,B,Br,V1,R,V).
%------------------------------------------------

% Verifica si ya se reviso una ruta especifica
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