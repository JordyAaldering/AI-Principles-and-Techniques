import java.util.logging.Level;
import java.util.logging.Logger;

public class Debug {

    private static boolean enabled = false;
    private static Logger logger = null;

    public static void enable() {
        enabled = true;
        Logger logger = Logger.getLogger("Debug");
        logger.info("Debugger enabled.");
        logger.setLevel(Level.WARNING);
    }

    public static void trace(String msg) {
        if (!enabled) return;
        System.out.println(msg);
    }

    public static void info(String msg) {
        if (!enabled) return;
        logger.info(msg);
    }

    public static void warn(String msg) {
        if (!enabled) return;
        logger.warning(msg);
    }

}
