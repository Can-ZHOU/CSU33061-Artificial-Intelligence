arc(N, M, Seed) :- M is N*Seed.
arc(N, M, Seed) :- M is N*Seed + 1.

goal(N, Target) :- 0 is N mod Target.

% breadth1st(+Start, ?Found, +Seed, +Target)
breadth1st(Start, Found, Seed, Target) :- fsB([Start], Found, Seed, Target).

fsB([Node|_], Node, _, Target) :- goal(Node, Target).
fsB([Node|Rest], Found, Seed, Target) :-
    findall(Next, arc(Node, Next, Seed), Children),
    append(Rest, Children, NewFrontier),
    fsB(NewFrontier, Found, Seed, Target).