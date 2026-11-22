//AYALA CARRASCO ANGEL ROLDAN 23170086
package nodo;

public class NodoArbol<T> {

    private T valor;
    private NodoArbol<T> izquierdo;
    private NodoArbol<T> derecho;

    public NodoArbol(T valor) {
        this.valor = valor;
        this.izquierdo = null;
        this.derecho = null;
    }

    public NodoArbol(T valor, NodoArbol<T> izquierdo, NodoArbol<T> derecho) {
        this.valor = valor;
        this.izquierdo = izquierdo;
        this.derecho = derecho;
    }

    public T getElemento() {
        return valor;
    }

    public void setElemento(T valor) {
        this.valor = valor;
    }

    public NodoArbol<T> getIzquierdo() {
        return izquierdo;
    }

    public void setIzquierdo(NodoArbol<T> izquierdo) {
        this.izquierdo = izquierdo;
    }

    public NodoArbol<T> getDerecho() {
        return derecho;
    }

    public void setDerecho(NodoArbol<T> derecho) {
        this.derecho = derecho;
    }

    public boolean esHoja() {
        return (izquierdo == null) && (derecho == null);
    }

    public int numeroDeHijos() {
        int hijosIzq = (izquierdo != null) ? 1 + izquierdo.numeroDeHijos() : 0;
        int hijosDer = (derecho != null) ? 1 + derecho.numeroDeHijos() : 0;
        return hijosIzq + hijosDer;
    }
}
