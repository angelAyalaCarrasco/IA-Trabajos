import java.util.LinkedList;
import java.util.Queue;
import org.w3c.dom.Node;


public class SearchTree {

    Node root;
    String initialState;
    String goalState;

    public SearchTree(String initialState, String goalState){
        this.initialState = initialState;
        this.goalState = goalState;
        this.root = new Node(initialState, null);
    }
}
