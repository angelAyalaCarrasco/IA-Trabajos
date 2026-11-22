//AYALA CARRASCO ANGEL ROLDAN 23170086
package nodo;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class ArbolBinario<T> {

    protected NodoArbol<T> nodoRaiz;
    protected int cantidadNodos;

    public ArbolBinario() {
        this.nodoRaiz = null;
        this.cantidadNodos = 0;
    }

    public ArbolBinario(T elementoRaiz, ArbolBinario<T> subarbolIzq, ArbolBinario<T> subarbolDer) {
        if (elementoRaiz != null) {
            this.nodoRaiz = new NodoArbol<>(elementoRaiz);
            this.cantidadNodos = 1;

            if (subarbolIzq != null && !subarbolIzq.isEmpty()) {
                this.nodoRaiz.setIzquierdo(subarbolIzq.getRaiz());
                this.cantidadNodos += subarbolIzq.size();
            }

            if (subarbolDer != null && !subarbolDer.isEmpty()) {
                this.nodoRaiz.setDerecho(subarbolDer.getRaiz());
                this.cantidadNodos += subarbolDer.size();
            }
        } else {
            removeAllElements();
        }
    }

    public NodoArbol<T> getRaiz() {
        return nodoRaiz;
    }

    public void setRaiz(NodoArbol<T> nodoRaiz) {
        this.nodoRaiz = nodoRaiz;
    }

    public int size() {
        return cantidadNodos;
    }

    public boolean isEmpty() {
        return nodoRaiz == null;
    }

    public void removeLeftSubtree() {
        if (!isEmpty() && nodoRaiz.getIzquierdo() != null) {
            int nodosEliminados = nodoRaiz.getIzquierdo().numeroDeHijos() + 1;
            nodoRaiz.setIzquierdo(null);
            cantidadNodos -= nodosEliminados;
        }
    }

    public void removeRightSubtree() {
        if (!isEmpty() && nodoRaiz.getDerecho() != null) {
            int nodosEliminados = nodoRaiz.getDerecho().numeroDeHijos() + 1;
            nodoRaiz.setDerecho(null);
            cantidadNodos -= nodosEliminados;
        }
    }

    public void removeAllElements() {
        nodoRaiz = null;
        cantidadNodos = 0;
    }

    public boolean contains(T elemento) {
        if (elemento == null || isEmpty()) {
            return false;
        }
        return buscarElemento(nodoRaiz, elemento);
    }

    private boolean buscarElemento(NodoArbol<T> nodo, T objetivo) {
        if (nodo == null) {
            return false;
        }
        if (nodo.getElemento().equals(objetivo)) {
            return true;
        }
        return buscarElemento(nodo.getIzquierdo(), objetivo) || buscarElemento(nodo.getDerecho(), objetivo);
    }

    public Iterator<T> iteratorPreOrden() {
        List<T> listaElementos = new ArrayList<>();
        llenarPreOrden(nodoRaiz, listaElementos);
        return listaElementos.iterator();
    }

    private void llenarPreOrden(NodoArbol<T> nodo, List<T> lista) {
        if (nodo != null) {
            lista.add(nodo.getElemento());
            llenarPreOrden(nodo.getIzquierdo(), lista);
            llenarPreOrden(nodo.getDerecho(), lista);
        }
    }
}
