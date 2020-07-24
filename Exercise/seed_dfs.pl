arc(N, M, Seed) :- M is N*Seed.
arc(N, M, Seed) :- M is N*Seed + 1.

goal(N, Target) :- 0 is N mod Target.

depth1st(Start, Found, Seed, Target) :- 
    fsD([Start], Found, Seed, Target).

fsD([Node|_], Node, _, Target) :- goal(Node, Target).
fsD([Node|Rest], Found, Seed, Target) :-
    findall(Next, arc(Node, Next, Seed), Children),
    append(Children, Rest, NewFrontier),
    fsD(NewFrontier, Found, Seed, Target).