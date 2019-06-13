#glpsol -m modelo.mod -o modelo.sol --tmlim 4

set CIUDADES;
param COSTO{i in CIUDADES, j in CIUDADES : i<>j};
param n := 24;

var Y{i in CIUDADES, j in CIUDADES: i<>j} >= 0, binary;
var U{i in CIUDADES} >=0, integer;

minimize z: sum{i in CIUDADES, j in CIUDADES : i<>j} COSTO[i,j]*Y[i,j];

s.t. entrantes{j in CIUDADES}: 
		sum{i in CIUDADES: i<>j } Y[i,j] = 1;

s.t. salientes{i in CIUDADES}:
		sum{j in CIUDADES: i<>j} Y[i,j] = 1;

s.t. orden{i in CIUDADES, j in CIUDADES: i<>j and i<>'A' and j <> 'A'}:
		U[i] - U[j] + n*Y[i,j] <= n - 1;

s.t. NodoFinal:Y['K','A']=1;

#Descomentar para camino optimo en tiempo normal
#s.t. startRight:Y['A','B']=1;
#s.t. forcedNext:Y['B','C']=1;
#s.t. lastForcedStep:Y['C','D']=1;

solve;


printf "Optimal tour has length %d\n",
   sum{i in CIUDADES, j in CIUDADES : i<>j} COSTO[i,j]*Y[i,j];
printf("City Order \n");
printf{i in CIUDADES: i<>'A'} "%s %d\n",i,U[i];


data;

set CIUDADES:= A B C D E F G H I J K L M N O P Q R S T U V W X Y ;
param COSTO :  A B C D E F G H I J K L M N O P Q R S T U V W X Y :=
			
A . 1 2 3 4 5 1 4 5 6 2 3 4 5 3 4 5 6 6 5 6 8 7 7 6
B 1 . 1 2 3 4 2 5 4 5 3 4 5 4 4 5 6 5 5 6 5 7 6 7 7
C 2 1 . 1 2 3 3 4 3 4 4 5 6 3 5 6 5 4 4 7 4 6 5 6 7
D 3 2 1 . 1 2 4 3 2 3 5 4 7 2 6 5 4 3 3 7 3 5 4 5 6
E 4 3 2 1 . 1 5 2 1 2 4 3 6 1 5 4 3 2 2 6 2 4 3 4 5
F 5 4 3 2 1 . 6 3 2 1 5 4 6 2 6 5 4 3 3 5 1 3 2 3 4
G 1 2 3 4 5 6 . 3 4 7 1 2 3 6 2 3 4 5 7 4 7 8 7 6 5
H 4 5 4 3 2 3 3 . 1 4 2 1 4 3 3 4 5 4 4 5 4 6 5 6 6
I 5 4 3 2 1 2 4 1 . 3 3 2 5 2 4 5 4 3 3 6 3 5 4 5 6
J 6 5 4 3 2 1 7 4 3 . 6 5 6 1 5 4 3 2 2 6 2 4 3 4 5
K 2 3 4 5 4 5 1 2 3 6 . 1 2 5 1 2 3 4 6 3 6 7 6 5 4
L 3 4 5 4 3 4 2 1 2 5 1 . 3 4 2 3 4 5 5 4 5 7 6 6 5
M 4 5 6 7 6 6 3 4 5 6 2 3 . 5 1 2 3 4 5 1 5 5 4 3 2
N 5 4 3 2 1 2 6 3 2 1 5 4 5 . 4 3 2 1 1 5 3 3 2 3 4
O 3 4 5 6 5 6 2 3 4 5 1 2 1 4 . 1 2 3 5 2 6 6 5 4 3
P 4 5 6 5 4 5 3 4 5 4 2 3 2 3 1 . 1 2 4 3 6 6 5 5 4
Q 5 6 5 4 3 4 4 5 4 3 3 4 3 2 2 1 . 1 3 4 5 5 4 5 5
R 6 5 4 3 2 3 5 4 3 2 4 5 4 1 3 2 1 . 2 5 4 4 3 4 5
S 6 5 4 3 2 3 7 4 3 2 6 5 5 1 5 4 3 2 . 4 2 2 1 2 3
T 5 6 7 7 6 5 4 5 6 6 3 4 1 5 2 3 4 5 4 . 4 4 3 2 1
U 6 5 4 3 2 1 7 4 3 2 6 5 5 3 6 6 5 4 2 4 . 2 1 2 3
V 8 7 6 5 4 3 8 6 5 4 7 7 5 3 6 6 5 4 2 4 2 . 1 2 3
W 7 6 5 4 3 2 7 5 4 3 6 6 4 2 5 5 4 3 1 3 1 1 . 1 2
X 7 7 6 5 4 3 6 6 5 4 5 6 3 3 4 5 5 4 2 2 2 2 1 . 1
Y 6 7 7 6 5 4 5 6 6 5 4 5 2 4 3 4 5 5 3 1 3 3 2 1 .
;

end;