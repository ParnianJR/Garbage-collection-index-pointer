# Garbage-collection-using-index-pointer

garbage collection is the process of collecting all unused nodes and returning them to available space.
This process is carried out in essentially two phases. In the first phase, known as the marking phase, all nodes in use are marked.
In the second phase all unmarked nodes are returned to the available space list.

This project satisfies 5 commands:
1) Li = exp : creates Li list corresponding to total parenthesis expression exp.(and this proccess is done by recursion).
2) Make Li child of Lj at node_expr : created list Li becomes the child of node_expr in list Lj.
3) Delete Li from node_expr : down pointer of node_expr will be none.
4) Print Li :)
5) Garbage Collection: adds all unreachable elements to avail list.
