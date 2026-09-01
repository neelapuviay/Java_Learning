package leariningExamples.locksOnStaticblockAndFiledsHowTheyWork;

public class A {

    public static int aVal = B.bVal + 1;

    public static void main(String[] args) {
        System.out.println("A.aVal = " + aVal);
        System.out.println("B.bVal = " + B.bVal);
    }

}
