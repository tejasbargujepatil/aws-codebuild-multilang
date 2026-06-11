public class Numbers {
    public static void main(String[] args) {
        int[] numbers = {45, 12, 78, 3, 56, 89, 23, 67, 34, 91,154,5,48,5,98};

        int highest = numbers[0];
        int lowest  = numbers[0];
        int sum     = 0;

        for (int n : numbers) {
            if (n > highest) highest = n;
            if (n < lowest)  lowest  = n;
            sum += n;
        }

        double average = (double) sum / numbers.length;

        System.out.println("========================================");
        System.out.println("         JAVA NUMBER ANALYSIS");
        System.out.println("========================================");
        System.out.print("Numbers : [");
        for (int i = 0; i < numbers.length; i++) {
            System.out.print(numbers[i]);
            if (i < numbers.length - 1) System.out.print(", ");
        }
        System.out.println("]");
        System.out.println("Highest : " + highest);
        System.out.println("Lowest  : " + lowest);
        System.out.printf("Average : %.2f%n", average);
        System.out.println("========================================");
    }
}
