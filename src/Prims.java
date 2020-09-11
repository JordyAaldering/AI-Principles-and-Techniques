import java.util.LinkedList;

public class Prims {

    private static final int INF = Integer.MAX_VALUE;

    private static class MST {
        public Vertex[] vertices;
        public int count;

        public MST(int[][] graph) {
            count = graph.length;
            vertices = new Vertex[count];

            // Initialize vertices
            for (int i = 0; i < count; i++) {
                vertices[i] = new Vertex();
            }

            // Set root
            vertices[0].key = 0;

            // Add neighbours
            for (int i = 0; i < graph.length; i++) {
                for (int j = 0; j < graph.length; j++) {
                    int weight = graph[i][j];
                    if (weight != 0) {
                        Edge edge = new Edge(weight, vertices[j]);
                        vertices[i].neighbours.add(edge);
                    }
                }
            }
        }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            for (Vertex v : vertices) {
                sb.append(v);
                sb.append('\n');
            }

            return sb.toString();
        }
    }

    private static class Vertex {
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

    private static class Edge {
        public int weight;
        public Vertex to;

        public Edge(int weight, Vertex to) {
            this.weight = weight;
            this.to = to;
        }
    }

    private static Vertex extractMin(MST mst) {
        int key = INF;
        // Set min to root for first iteration
        Vertex min = mst.vertices[0];

        for (Vertex n : mst.vertices) {
            if (!n.included && n.key < key) {
                key = n.key;
                min = n;
            }
        }

        min.included = true;
        return min;
    }

    private static MST generateMST(int[][] graph) {
        assert graph.length == graph[0].length
                : "Adjacency matrix must be square!";
        MST mst = new MST(graph);

        // Generate MST
        for (int i = 0; i < graph.length - 1; i++) {
            Vertex min = extractMin(mst);
            System.out.println("Add " + min.label);
            for (Edge edge : min.neighbours) {
                if (!edge.to.included && edge.weight != 0 && edge.weight < edge.to.key) {
                    edge.to.key = edge.weight;
                    edge.to.parent = min;
                }
            }
        }

        return mst;
    }

    public static void main(String[] args) {
        int[][] graph = new int[][] {
                { 0, 2, 0, 5, 0 },
                { 2, 0, 3, 0, 2 },
                { 0, 3, 0, 3, 1 },
                { 5, 0, 3, 0, 0 },
                { 0, 2, 1, 0, 0 },
        };
        MST mst = generateMST(graph);
        System.out.println(mst.toString());
    }

}
