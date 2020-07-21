digraph {
	graph [rankdir=LR]
	ini [shape=point]
	q1 [shape=doublecircle]
	q0
	ini -> q0
	q0 -> q1 [label=1]
	q1 -> q1 [label=1]
}
