package leariningExamples.oops.polymorphism;

public class methodOverrideStaticMethod {
    public static void main(String[] args) {
        Parent p = new Child();
        p.greet(); // prints "Parent" — static dispatch uses reference type, NOT runtime type

    }
}

class Parent {
    static void greet() {
        System.out.println("Parent");
    }
}

class Child extends Parent {
    static void greet() {
        System.out.println("Child");
    }
}
