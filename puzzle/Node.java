public class Node {
    //PONER TODO PRIVATE
    String state;
    Node parent;
    int depth;

    public Node(String state, Node parent){
        this.state = state;
        this.parent = parent;
    }
}