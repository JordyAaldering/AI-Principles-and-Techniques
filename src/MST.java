import java.util.Arrays;
import java.util.LinkedList;
import java.util.stream.Collectors;

public class MST {

    static final int INF = Integer.MAX_VALUE;

    public int count;
    public Vertex[] vertices;
    public int root;

    public MST(int[][] graph, int root) {
        if (graph.length == 0) {
            Debug.warn("Input graph is empty.");
            count = 0;
            vertices = new Vertex[0];
            root = 0;
            return;
        }

        setVertices(graph);
        setRoot(root);
        setNeighbours(graph);

        Debug.trace("Initial graph:");
        Debug.trace(toString());
    }

    private void setVertices(int[][] graph) {
        count = Math.min(graph.length, graph[0].length);
        vertices = new Vertex[count];
        for (int i = 0; i < count; i++) {
            vertices[i] = new Vertex();
        }
    }

    private void setRoot(int root) {
        if (root >= count) {
            Debug.warn("Root '" + root + "' is out of range.");
            Debug.info("Clamping root between 0 and " + (count - 1));
            root = Math.max(0, Math.min(root, count - 1));
        }

        vertices[root].key = 0;
    }

    private void setNeighbours(int[][] graph) {
        int weight;
        Edge edge;

        for (int i = 0; i < count; i++) {
            // The graph is assumed to be undirected,
            // so we only look to the top right of the diagonal.
            for (int j = 0; j < i; j++) {
                weight = graph[i][j];
                if (weight == 0) continue;

                // Add an edge from i to j.
                edge = new Edge(graph[i][j], vertices[j]);
                vertices[i].neighbours.add(edge);

                // Add an edge from j to i.
                edge = new Edge(graph[i][j], vertices[i]);
                vertices[j].neighbours.add(edge);
            }
        }
    }

    static class Vertex {
        private static char currentLabel = 'a';
        public final char label;

        public int key = INF;
        public Vertex parent = null;
        public boolean included = false;
        public LinkedList<Edge> neighbours = new LinkedList<>();

        Vertex() {
            label = currentLabel++;
        }

        @Override
        public String toString() {
            return parent == null ? "Root is " + label
                    : "Edge from " + parent.label + " to " + label;
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
            return "Edge with weight " + weight + " to " + to;
        }
    }

    @Override
    public String toString() {
        return Arrays.stream(vertices)
                .map(v -> String.valueOf(v) + '\n')
                .collect(Collectors.joining());
    }

}
