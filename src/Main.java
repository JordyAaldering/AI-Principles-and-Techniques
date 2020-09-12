public class Main {

    public static void main(String[] args) {
        int[][] graph = new int[][] {
                { 0, 2, 0, 5, 0 },
                { 2, 0, 3, 0, 2 },
                { 0, 3, 0, 3, 1 },
                { 5, 0, 3, 0, 0 },
                { 0, 2, 1, 0, 0 },
        };

        MST mst = Prims.run(graph);
        System.out.println("MST:\n" + mst);
    }

}
