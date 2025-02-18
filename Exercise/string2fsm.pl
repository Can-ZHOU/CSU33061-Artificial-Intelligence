% string2fsm(+String, ?TransitionSet, ?FinalStates)
string2fsm([], [], [q0]).
string2fsm([H|T], Trans, Last) :- 
    mkTL(T, [H], [[q0, H, [H]]], Trans, Last).

% mkTL(+More, +LastSoFar, +TransSoFar, ?Trans, ?Last)
mkTL([], Last, Trans, Trans, Last).
mkTL([H|T], LastSoFar, TransSoFar, Trans, Last) :-
    mkTL(T, [H|LastSoFar], [[LastSoFar, H, [H|LastSoFar]]|TransSoFar], Trans, Last).