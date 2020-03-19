package task_01;

public class Driver {
    public static void main(String[] args) {
        if (args.length < 2)
            System.out.println("error, no parameteres inputed");
        else {
            try {
                int t = Integer.parseInt(args[1]);// max seconds that program can work
                int b = Integer.parseInt(args[2]);// if b == 0 than minimalize function h else g
            } catch (Exception e) {
                System.out.println("These arguments are not integers!");
            }
        }
    }
}
