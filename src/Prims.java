import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;

public class Prims {

    private static final int INF = Integer.MAX_VALUE;

    private int extractMin(int[] keys, boolean[] mst) {
        int min = INF, index = -1;
        for (int i = 0; i < keys.length; i++) {
            if (!mst[i] && keys[i] < min) {
                min = keys[i];
                index = i;
            }
        }

        mst[index] = true;
        return index;
    }

    private void run(int[][] graph) {
        int vertices = graph.length;
        int[] keys = new int[vertices];
        int[] parents = new int[vertices];
        boolean[] mst = new boolean[vertices];
        Arrays.fill(keys, INF);

        keys[0] = 0;
        parents[0] = -1;

        for (int i = 0; i < vertices - 1; i++) {
            int v = extractMin(keys, mst);
            for (int w = 0; w < vertices; w++) {
                if (!mst[w] && graph[v][w] != 0 && graph[v][w] < keys[w]) {
                    keys[w] = graph[v][w];
                    parents[w] = v;
                }
            }
        }
    }

    public static void main(String[] args) {
        (new Prims()).run(new int[][] {
                { 0, 2, 0, 5, 0 },
                { 2, 0, 3, 0, 0 },
                { 0, 3, 0, 3, 1 },
                { 5, 0, 3, 0, 0 },
                { 0, 0, 1, 0, 0 },
        });
    }

}
