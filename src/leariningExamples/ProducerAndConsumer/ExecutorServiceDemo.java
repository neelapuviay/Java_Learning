package ProducerAndConsumer;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class ExecutorServiceDemo {

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(2);

        // Submitting a Callable returns a Future
        Future<Integer> future = executor.submit(() -> {
            Thread.sleep(10000);
            return 42;
        });

        // Check status without blocking
        System.out.println("Is done? " + future.isDone()); // false

        // future.get() BLOCKS the calling thread until 42 is returned
        Integer result = future.get();
        System.out.println("Result: " + result);

        executor.shutdown();
    }
}
