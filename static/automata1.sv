digraph {
	graph [rankdir=LR]
	ini [shape=point]
	q0
	ini -> q0
	q1 [shape=doublecircle]
	q1 -> q1 [label=a]
	q1 -> q0 [label=b]
	q0 -> q1 [label=a]
	q0 -> q0 [label=b]
}
