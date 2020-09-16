import java.util.Random;

public class Main {

    private final static Random rand = new Random();

    /**
     * @param size The number of vertices in the matrix.
     * @param density The chance of an edge appearing.
     * @return A random undirected adjacency matrix.
     */
    private static int[][] generateUAM(int size, float density) {
        int[][] graph = new int[size][size];
        for (int i = 1; i < size; i++) {
            for (int j = 0; j < i; j++) {
                if (rand.nextFloat() <= density) continue;
                int weight = (int)(rand.nextFloat() * size);
                graph[i][j] = weight;
                graph[j][i] = weight;
            }
        }

        return graph;
    }

    public static void main(String[] args) {
        var graph = generateUAM(10, 0.5f);
        var mst = Prims.calculateMST(graph);

        System.out.println("Graph:");
        for (var v : mst.vertices) {
            System.out.print("Vertex " + v.label + ":");
            for (var e : v.neighbours) {
                System.out.print(" -" + e.weight + "> " + e.to.label + ",");
            }
            System.out.println();
        }

        System.out.println("MST:");
        System.out.println(mst);
    }

}
