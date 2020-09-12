import java.util.Arrays;

public class Prims {

    private static MST.Vertex extractMin(MST mst) {
        int key = MST.INF;
        MST.Vertex min = null;

        for (var vertex : mst.vertices) {
            if (!vertex.included // The vertex is not yet in the MST
                    && vertex.key < key) { // The new key is better
                key = vertex.key;
                min = vertex;
            }
        }

        assert min != null : "No vertex was found";
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

    static MST run(int[][] graph) {
        MST mst = new MST(graph);
        mst.vertices[0].key = 0;

        for (int i = 0; i < mst.count - 1; i++) {
            MST.Vertex min = extractMin(mst);
            updateNeighbours(min);
        }

        return mst;
    }

}
