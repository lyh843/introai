%------------------------------------------------------------------------------
% Declaring dynamic methods

:- dynamic ([
        % TODO: Here you should add some predicates used in knowledge bases. 
	    agent_location/1,
	    gold_location/1,
	    pit_location/1,
	    time_taken/1,
	    score/1,
	    world_size/1,
	    wumpus_location/1
]).


%------------------------------------------------------------------------------
% To start the game

start :-
    format('Initializing started...~n', []),
    init,
    format('Let the game begin!~n', []),
    take_steps([[1,1]]).

%------------------------------------------------------------------------------
% Scheduling simulation:

step_pre(VisitedList) :-
    agent_location(AL),
    gold_location(GL),
    wumpus_location(WL),
    score(S),
    time_taken(T),

    ( AL=GL -> writeln('WON!'), format('Score: ~p,~n Time: ~p~n', [S,T]),
               format('Visited Cells: ~p', [VisitedList])
    ; AL=WL -> format('Lost: Wumpus eats you!~n', []),
               format('Score: ~p,~n Time: ~p', [S,T])
    ; pit_location(AL) -> format('Lost: Fell into a pit!~n', []),
                      format('Score: ~p, ~n Time: ~p', [S, T])
    ; T > 100 -> format('Lost: Time is up!~n', [])
    ; take_steps(VisitedList)
    ).

take_steps(VisitedList) :-
    make_percept_sentence(Perception),
    agent_location(AL),
    format('I\'m in ~p, seeing: ~p~n', [AL,Perception]),

    update_KB(Perception),
    ask_KB(VisitedList, Action), 
    format('I\'m going to: ~p~n', [Action]),
    update_agent_location(Action, VisitedList),

    update_time,
    update_score,

    agent_location(Aloc),
    VL = [Aloc|VisitedList],
    step_pre(VL).

%------------------------------------------------------------------------------
% Updating states

update_time :-
    % TODO
    retract(time_taken(PreT)),
    NewT is PreT + 1,
    assert(time_taken(NewT)).

update_score :-
    % TODO
    retract(score(PreS)),
    agent_location(AL),
    gold_location(GL),
    (
        AL = GL -> NewS is PreS + 50
        ; NewS is PreS - 1
    ),
    assert(score(NewS)).

update_agent_location(NewAL, VisitedList) :-
    % TODO
    retract(agent_location(PreAL)),
    assert(agent_location(NewAL)).

%------------------------------------------------------------------------------
% Perception

make_percept_sentence([Stench,Breeze,Glitter]) :-
	smelly(Stench),
	breezy(Breeze),
	glittering(Glitter).

%------------------------------------------------------------------------------
% Initializing

init :-
    init_game,
    init_land_fig72,
    init_agent,
    init_wumpus.

init_game :-
    % TODO: Add the initial knowledge base assertions
    retractall( time_taken(_) ),
    assert( time_taken(0) ),

    retractall( score(_) ),
    assert( score(0) ).

% To set the situation described in Russel-Norvig's book (2nd Ed.),
% according to Figure 7.2
init_land_fig72 :-
    retractall( world_size(_) ),
    assert( world_size(4) ),

    retractall( gold_location(_) ),
    assert( gold_location([3,2]) ),

    retractall( pit_location(_) ),
    assert( pit_location([4,4]) ),
    assert( pit_location([3,3]) ),
    assert( pit_location([1,3]) ).

init_agent :-
    retractall( agent_location(_) ),
    assert( agent_location([1,1]) ).

init_wumpus :-
    retractall( wumpus_location(_) ),
    assert( wumpus_location([3,1]) ).

%------------------------------------------------------------------------------
% Perceptors

adj(1,2).
adj(2,1).
adj(2,3).
adj(3,2).
adj(3,4).
adj(4,3).

adjacent( [X1, Y1], [X2, Y2] ) :-
    ( X1 = X2, adj( Y1, Y2 )
    ; Y1 = Y2, adj( X1, X2 )
    ).

isSmelly(L) :-
    % TODO
    wumpus_location(WL),
    adjacent(L, WL).

isBreezy(L) :-
    % TODO
    pit_location(PL),
    adjacent(L, PL).

isGlittering(L) :-
    % TODO
    gold_location(L).

breezy(yes) :-
    agent_location(AL),
    isBreezy(AL).
breezy(no) :-
    agent_location(AL),
    \+ isBreezy(AL).

smelly(yes) :-
    agent_location(AL),
    isSmelly(AL).
smelly(no) :-
    agent_location(AL),
    \+ isSmelly(AL).

glittering(yes) :-
    agent_location(AL),
    isGlittering(AL).
glittering(no) :-
    agent_location(AL),
    \+ isGlittering(AL).

%------------------------------------------------------------------------------
% Knowledge Base:

:- dynamic ([
    no_wumpus/1,
    no_gold/1,
    no_pit/1,
    maybe_wumpus/1,
    is_gold/1,
    maybe_pit/1
]).

update_KB( [Stench,Breeze,Glitter] ) :-
    add_wumpus_KB(Stench),
    add_pit_KB(Breeze),
    add_gold_KB(Glitter).


add_wumpus_KB(no) :-
    % TODO
    agent_location(AL), % 获取当前坐标
    (
        \+ no_wumpus(AL) -> % 如果之前没有添加过，那么就添加
            assert(no_wumpus(AL))
        ;true
    ),

    forall( % 遍历领居
        adjacent(AL, NeighbourL),
        (
            (
                \+ no_wumpus(NeighbourL) -> % 如果领居没有标注，则标注
                    assert(no_wumpus(NeighbourL))
                ;true
            ),
            (
                maybe_wumpus(NeighbourL) -> % 被误判则清除
                    retract(maybe_wumpus(NeighbourL))
                ;true
            )
        )
    ).
    
add_wumpus_KB(yes) :-
    % TODO
    agent_location(AL),
    forall(
        (
            adjacent(AL, NeighbourL), 
            \+ no_wumpus(NeighbourL)       
        ),
        (
            \+ maybe_wumpus(NeighbourL) ->
                assert(maybe_wumpus(NeighbourL))
            ;true
        )
    ).

add_pit_KB(no) :-
    % TODO
    agent_location(AL), % 获取当前坐标
    (
        \+ no_pit(AL) -> % 如果之前没有添加过，那么就添加
            assert(no_pit(AL))
        ;true
    ),

    forall( % 遍历领居
        adjacent(AL, NeighbourL),
        (
            (
                \+ no_pit(NeighbourL) -> % 如果领居没有标注，则标注
                    assert(no_pit(NeighbourL))
                ;true
            ),
            (
                maybe_pit(NeighbourL) -> % 被误判则清除
                    retract(maybe_pit(NeighbourL))
                ;true
            )
        )
    ).

add_pit_KB(yes) :-
    % TODO
    agent_location(AL),
    forall(
        (
            adjacent(AL, NeighbourL),        
            \+ no_pit(NeighbourL)
        ),
        (
            \+ maybe_pit(NeighbourL) ->
                assert(maybe_pit(NeighbourL))
            ;true
        )
    ).


add_gold_KB(no) :-
    % TODO
    agent_location(AL).

add_gold_KB(yes) :-
    % TODO
    agent_location(AL),
    is_gold(AL).

ask_KB(VisitedList, Action) :-
    % TODO
    agent_location(AL),
    (
        adjacent(AL, Action),
        \+ member(Action, VisitedList),
        \+ maybe_wumpus(Action),
        \+ maybe_pit(Action)
    -> true
    ; 
        adjacent(AL, Action),
        member(Action, VisitedList),
        \+ maybe_wumpus(Action),
        \+ maybe_pit(Action)
    ).
