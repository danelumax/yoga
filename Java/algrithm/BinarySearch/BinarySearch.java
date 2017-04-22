import java.util.Arrays;
import java.io.IOException;

public class BinarySearch {
    
    public int binarySearch(int[] array, int key)
        throws IOException {
        try {
            int start = 0;
            int end = array.length-1;
            int middle = 0;
            Arrays.sort(array);
            while(start <= end) {
                middle = (start + end) / 2;
                if (key < array[middle]) {
                    end = middle - 1;
                } else if (key > array[middle]) {
                    start = middle + 1;
                } else {
                    return middle;
                }
            }
            return -1;
        }
        catch(ArrayIndexOutOfBoundsException e) {
            e.printStackTrace();
            return -1;
        }
    }

    public static void main(String[] args)
        throws Exception {
        int[] array = new int[] {9,8,7,5,6,3,4,1,2};
        int key = 5;
        Class clazz = Class.forName("BinarySearch");
        BinarySearch obj = (BinarySearch)clazz.newInstance();
        int index = obj.binarySearch(array, key);
        if (index != -1)
        {
            System.out.println(array[key] + " is on " + index);
        }
    }
}

                

