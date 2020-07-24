% accept(+Trans, +Final, +Q0, ?String)
accept(_, Final, Q, []) :- member(Q, Final).
accept(Trans, Final, Q, [H|T]) :- 
    member([Q, H, Qn], Trans), 
    accept(Trans, Final, Qn, T).

member(X, [X|_]).
member(X, [_|L]) :- member(X, L).

% string2fsm(+String, ?TransitionSet, ?FinalStates)
string2fsm([], [], [q0]).
string2fsm([H|T], Trans, [Last]) :- 
    mkTL(T, [H], [[q0, H, [H]]], Trans, Last).

% mkTL(+More, +LastSoFar, +TransSoFar, ?Trans, ?Last)
mkTL([], Last, Trans, Trans, Last).
mkTL([H|T], LastSoFar, TransSoFar, Trans, Last) :-
    mkTL(T, [H|LastSoFar], [[LastSoFar, H, [H|LastSoFar]]|TransSoFar], Trans, Last).

test(String) :-
    string2fsm(String, Trans, Final),
    accept(Trans, Final, q0, String).