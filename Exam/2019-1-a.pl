arc([H|T], Next, [[H_kb|T_kb]|Rest]) :-
    findall([[H_kb|T_kb]|Rest], H == H_kb, Next).
    