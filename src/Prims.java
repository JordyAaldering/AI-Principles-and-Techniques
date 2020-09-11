import java.util.Arrays;

public class Prims {

    private static MST.Vertex extractMin(MST mst) {
        int key = MST.INF;
        // Set min = root for first iteration
        MST.Vertex min = mst.vertices[mst.root];

        for (var vertex : mst.vertices) {
            if (!vertex.included // The vertex is not yet in the MST
                    && vertex.key < key) { // The new key is better
                key = vertex.key;
                min = vertex;
            }
        }

        min.included = true;
        return min;
    }

    private static void updateNeighbours(MST.Vertex vertex) {
        for (var edge : vertex.neighbours) {
            if (!edge.to.included // The vertex is not yet in the MST
                    && edge.weight != 0 // There is an edge to the vertex
                    && edge.weight < edge.to.key) { // The new key is better
                edge.to.key = edge.weight;
                edge.to.parent = vertex;
            }
        }
    }

    static MST run(int[][] graph, int root) {
        MST mst = new MST(graph, root);
        for (int i = 0; i < mst.count - 1; i++) {
            MST.Vertex min = extractMin(mst);
            updateNeighbours(min);
        }

        return mst;
    }

}
