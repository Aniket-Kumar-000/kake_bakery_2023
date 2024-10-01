import java.util.ArrayList;
import java.util.Scanner;

class SleepSort {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Integer> arr = new ArrayList<>();
        
        System.out.print("Enter the number of elements: ");
        int n = sc.nextInt();
        
        System.out.println("Enter the elements:");
        for (int i = 0; i < n; i++) {
            arr.add(sc.nextInt());
        }

        sleepSort(arr);
    }

    public static void sleepSort(ArrayList<Integer> arr) {
        ArrayList<Thread> threads = new ArrayList<>();

        for (int num : arr) {
            Thread thread = new Thread(() -> {
                try {
                    Thread.sleep(num);
                    System.out.print(num + " ");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });

            threads.add(thread);
            thread.start();
        }

        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
