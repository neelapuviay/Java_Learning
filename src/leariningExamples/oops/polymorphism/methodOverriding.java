package leariningExamples.oops.polymorphism;

class Animal {
    void sound() {
        System.out.println("Some generic sound");
    }
}

class Dog extends Animal {
    @Override
    void sound() {
        System.out.println("Bark");
    }
}

class Cat extends Animal {
    @Override
    void sound() {
        System.out.println("Meow");
    }
}

public class methodOverriding {
    public static void main(String[] args) {
        Animal a = new Dog(); // reference type Animal, object type Dog
        a.sound(); // prints "Bark" — decided at RUNTIME, not by the reference type
    }
}
