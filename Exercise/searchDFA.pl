search(Node) :- searchD([Node]).

searchD(NL) :- goalD(NL);
               (arcD(NL, NL2), searchD(NL, NL2)).

goalD(NodeList) :- member(Node, NodeList), goal(Node).

arcLN(NodeList,Next) :- member(Node,NodeList),arc(Node,Next).

arcD(NodeList,NextList) :-setof(Next, arcLN(NodeList,Next), NextList).

goal(1).