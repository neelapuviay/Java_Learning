package leariningExamples;

public class Lamp {
    private boolean isOn;

    public void turnOn() {
        this.isOn = true;
        printStatus();
    }

    public void turnOff() {
        this.isOn = false;
        printStatus();
    }

    private void printStatus() {
        System.out.println("Light is turned " + (isOn ? "on" : "off"));
    }

    public static void main(String[] args) {
        var lamp = new Lamp();
        lamp.turnOn();
        lamp.turnOff();
    }
}