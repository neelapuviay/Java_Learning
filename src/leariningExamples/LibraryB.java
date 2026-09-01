package leariningExamples;

public class LibraryB {
    public static void main(String[] args) {
        System.out.println(LibraryA.MAX);
        LibraryA a = new LibraryA();
        System.out.println(a.getClass().getProtectionDomain().getCodeSource());
    }
}
