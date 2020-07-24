:- dynamic(kb/1).

makeKB(File):- open(File,read,Str),
               readK(Str,K), 
               reformat(K,KB), 
               asserta(kb(KB)), 
               close(Str).                  
   
readK(Stream,[]):- at_end_of_stream(Stream),!.
readK(Stream,[X|L]):- read(Stream,X),
                      readK(Stream,L).

reformat([],[]).
reformat([end_of_file],[]) :- !.
reformat([:-(H,B)|L],[[H|BL]|R]) :- !,  
                                    mkList(B,BL),
                                    reformat(L,R).
reformat([A|L],[[A]|R]) :- reformat(L,R).
    
mkList((X,T),[X|R]) :- !, mkList(T,R).
mkList(X,[X]).

initKB(File) :- retractall(kb(_)), makeKB(File).

%----------------------------------------------------------------------------------------

% astar
% Give the Node and KB, find its path to the goal node with min cost.
% 3 related functions: astar/3, astar/4, astar/5.

% astar/3
% astar(+Node, ?Path, ?Cost)
astar(Node, Path, Cost) :- kb(KB), astar(Node, Path, Cost, KB).

% astar/4
% astar(+Node, ?Path, ?Cost, +KB)
astar(Node, Path, Cost, KB) :- astar([Node, [Node], 0], Path, Cost, KB, []).

% astar/5
% astar(+[CurrentNode, NodePath, NodeCost], ?GoalPath, ?GoalCost, +KB, +Frontier)
astar([CurrentNode, NodePath, NodeCost], NodePath, NodeCost, _, _) :- goal(CurrentNode).
astar([CurrentNode, NodePath, NodeCost], GoalPath, GoalCost, KB, Frontier) :-
    % Find all the frontier nodes for CurrentNode and store as Children.
    findall(
        [ChildNode, [ChildNode|NodePath], ChildNodeCost], 
        (arc(CurrentNode, ChildNode, NewCost, KB), ChildNodeCost is NewCost + NodeCost), 
        Children
    ),
    % Add CurrentNode frontier to previous frontiers list then find the smallest node in frontier list and put it as head node in the list.
    add_to_frontier(Children, Frontier, SortedFrontier),
    % Separating new current node and new frontier list from SortedFrontier.
    SortedFrontier = [NewNode | NewFrontier],
    % Call astar recursively.
    astar(NewNode, GoalPath, GoalCost, KB, NewFrontier).

% Goal node.
goal([]).

% arc/4
% arc(+[H|T], ?Node, ?Cost, +KB)
arc([H|T], Node, Cost, KB) :- 
    member([H|B], KB), 
    append(B, T, Node),
    length(B, L), 
    Cost is L+1.

% add_to_frontier/3
% add_to_frontier(+Children, +Frontier, ?SortedFrontier)
add_to_frontier(Children, Frontier, SortedFrontier) :-
    append(Children, Frontier, UnsortFrontier),
    find_smallest_node(UnsortFrontier, SortedFrontier).

% find_smallest_node/2
% find_smallest_node(+[Head|Tail], ?ReturnFrontier)
find_smallest_node([Head|Tail], ReturnFrontier) :- sort(Head, Tail, [], ReturnFrontier).

% sort/4
% sort(+Head, +[UnSortedHead|UnSortedTail], +SortedList, ?ReturnFrontier)
sort(Head, [], SortedList, [Head|SortedList]).
sort(Head, [UnSortedHead|UnSortedTail], SortedList, ReturnFrontier) :-
    (less_than(Head, UnSortedHead) % if
     -> % then
        sort(Head, UnSortedTail, [UnSortedHead|SortedList], ReturnFrontier)
     ;  % else
        sort(UnSortedHead, UnSortedTail, [Head|SortedList], ReturnFrontier)
    ).

% less_than/2
% less_than(+[Node1, _, Cost1], +[Node2, _, Cost2])
less_than([Node1, _, Cost1], [Node2, _, Cost2]) :-
	heuristic(Node1,Hvalue1), 
    heuristic(Node2,Hvalue2),
    F1 is Cost1 + Hvalue1, 
    F2 is Cost2 + Hvalue2,
    F1 =< F2.

% heuristic/2
% heuristic(+Node, ?H)
heuristic(Node, H) :- length(Node, H).