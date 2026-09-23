package ProducerAndConsumer;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class ProducerAndConsumer {
    public static void main(String[] args) {
        // Queue with fixed capacity of 5
        BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(5);

        // Producer thread
        Thread producer = new Thread(() -> {
            try {
                for (int i = 1; i <= 10; i++) {
                    queue.put(i); // Blocks if the queue reaches 5 items
                    Thread.sleep(1000);
                    System.out.println("Produced: " + i);

                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        // Consumer thread
        Thread consumer = new Thread(() -> {
            try {
                while (true) {
                    Integer item = queue.take(); // Blocks if the queue is empty
                    Thread.sleep(3000); // Slower consumer to show backpressure
                    System.out.println("Consumed: " + item);

                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        producer.start();
        consumer.start();
    }
}