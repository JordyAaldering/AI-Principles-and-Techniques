public class Prims {

    private static MST.Vertex extractMin(MST mst) {
        int key = MST.INF;
        // Set min to root for first iteration
        MST.Vertex min = mst.vertices[mst.root];

        for (MST.Vertex n : mst.vertices) {
            if (!n.included && n.key < key) {
                key = n.key;
                min = n;
            }
        }

        min.included = true;
        return min;
    }

    private static MST generateMST(int[][] graph) {
        MST mst = new MST(graph, 0);

        // Generate MST
        for (int i = 0; i < graph.length - 1; i++) {
            MST.Vertex min = extractMin(mst);
            for (MST.Edge edge : min.neighbours) {
                if (!edge.to.included && edge.weight != 0 && edge.weight < edge.to.key) {
                    edge.to.key = edge.weight;
                    edge.to.parent = min;
                }
            }
        }

        return mst;
    }

    public static void main(String[] args) {
        Debug.enable();

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
