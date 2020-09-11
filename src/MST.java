import java.util.Arrays;
import java.util.LinkedList;
import java.util.stream.Collectors;

public class MST {

    static final int INF = Integer.MAX_VALUE;

    public int count = 0;
    public Vertex[] vertices;
    public int root = 0;

    public MST(int[][] graph, int root) {
        if (graph.length == 0) {
            Debug.warn("Input graph is empty");
            vertices = new Vertex[0];
            return;
        }

        setVertices(graph);
        setRoot(root);
        setNeighbours(graph);
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
            Debug.warn("Root '" + root + "' is out of range");
            Debug.info("Clamping root between 0 and " + (count - 1));
            root = Math.max(0, Math.min(root, count - 1));
        }

        vertices[root].key = 0;
    }

    private void setNeighbours(int[][] graph) {
        for (int i = 0; i < count; i++) {
            // The graph is assumed to be undirected,
            // so we only look to the top right of the diagonal.
            for (int j = 0; j < i; j++) {
                int weight = graph[i][j];
                if (weight == 0) continue;

                vertices[i].neighbours.add(new Edge(weight, vertices[j]));
                vertices[j].neighbours.add(new Edge(weight, vertices[i]));
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

    @Override
    public String toString() {
        return Arrays.stream(vertices).map(Vertex::toString)
                .collect(Collectors.joining("\n"));
    }

}
