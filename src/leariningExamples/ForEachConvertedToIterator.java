import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ForEachConvertedToIterator {

    public static void main(String[] args) {

        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> list = new ArrayList<>();
        // 1. foreach loop
        for (Integer number : numbers) {
            System.out.print(number + " ");
        }
    }
}