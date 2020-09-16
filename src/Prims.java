import java.util.Arrays;
import java.util.LinkedList;
import java.util.stream.Collectors;

public class Prims {

    static final int INF = Integer.MAX_VALUE;

    static class MST {
        public int count = 0;
        public Vertex[] vertices;

        /**
         * Initializes a new Minimum Spanning Tree.
         * @param graph An adjacency matrix representation of an undirected graph.
         */
        public MST(int[][] graph) {
            if (graph.length == 0) {
                vertices = new Vertex[0];
                return;
            }

            count = Math.min(graph.length, graph[0].length);
            vertices = new Vertex[count];
            for (int i = 0; i < count; i++) {
                vertices[i] = new Vertex();
            }

            // The graph is assumed to be undirected,
            // so we only look to the top right of the diagonal.
            for (int i = 1; i < count; i++) {
                for (int j = 0; j < i; j++) {
                    if (graph[i][j] == 0) continue; // There is no edge
                    vertices[i].neighbours.add(new Edge(graph[i][j], vertices[j]));
                    vertices[j].neighbours.add(new Edge(graph[i][j], vertices[i]));
                }
            }
        }

        @Override
        public String toString() {
            return Arrays.stream(vertices).map(Vertex::toString)
                    .collect(Collectors.joining("\n"));
        }
    }

    static class Vertex {
        private static char currentChar = 'a';
        public final char label;

        public int key = INF;
        public Vertex parent = null;
        public boolean included = false;
        public LinkedList<Edge> neighbours = new LinkedList<>();

        Vertex() {
            label = currentChar++;
        }

        @Override
        public String toString() {
            return parent == null ? String.format("Vertex %s", label)
                    : String.format("Vertex %s has parent %s", label, parent.label);
        }
    }

    static class Edge {
        public int weight;
        public Vertex to;

        public Edge(int weight, Vertex to) {
            assert to != null : "Edge must have a destination";
            this.weight = weight;
            this.to = to;
        }

        @Override
        public String toString() {
            return String.format("Edge to %s with weight %d", to, weight);
        }
    }

    private static Vertex extractMin(MST mst) {
        int key = INF;
        Vertex min = null;

        for (Vertex vertex : mst.vertices) {
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

    private static void updateNeighbours(Vertex vertex) {
        for (Edge edge : vertex.neighbours) {
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
            Vertex min = extractMin(mst);
            updateNeighbours(min);
        }

        return mst;
    }

}
