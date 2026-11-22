package puzzle;

import java.util.ArrayList;
import java.util.List;

public class NodeUtils {

    public static String dibujarTablero(String estado) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < estado.length(); i++) {
            sb.append(estado.charAt(i)).append(" ");
            if (i % 3 == 2) {
                sb.append("\n");
            }
        }
        return sb.toString();
    }

    public static List<Node> obtenerSucesores(Node actual) {
        List<Node> sucesores = new ArrayList<>();
        String estado = actual.getTablero();
        int posVacio = estado.indexOf(' ');

        int fila = posVacio / 3;
        int col = posVacio % 3;

        int[][] direcciones = {
            {-1, 0}, // arriba
            {1, 0},  // abajo
            {0, -1}, // izquierda
            {0, 1}   // derecha
        };

        for (int[] dir : direcciones) {
            int nuevaFila = fila + dir[0];
            int nuevaCol = col + dir[1];

            if (nuevaFila >= 0 && nuevaFila < 3 && nuevaCol >= 0 && nuevaCol < 3) {
                int nuevaPos = nuevaFila * 3 + nuevaCol;
                String nuevoEstado = moverPieza(estado, posVacio, nuevaPos);
                sucesores.add(new Node(nuevoEstado, actual));
            }
        }

        return sucesores;
    }

    private static String moverPieza(String estado, int i, int j) {
        char[] arreglo = estado.toCharArray();
        char aux = arreglo[i];
        arreglo[i] = arreglo[j];
        arreglo[j] = aux;
        return new String(arreglo);
    }
}
