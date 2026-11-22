import java.util.LinkedList;
import java.util.Queue;

public class App {
    
    public static void main(String[] args) {

        //3X3 puzzle
        String initialState = "7621 3458";
        String goalState = "12345678";
        SearchTree searchTree = new SearchTree(initialState, goalState);
        SearchTree.breadthFirstSearch(searchTree);
        System.out.println("Initial State: " + initialState);

    }

    public void printSolution(Node node) {
        Queue<Node> path = new LinkedList<>();
        queue.add(root);
        
    }
}
