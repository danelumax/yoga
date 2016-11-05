import java.io.IOException;

public class BubbleSort {
    
    public void bubbleSort(int[] array)
        throws IOException {
        try {
            int i = 0;
            int j = 0;
            int temp = 0;
            int flag = 0;
            for(i=0; i<array.length; i++) {
                for(j=array.length-1; j>i; j--) {
                    temp = array[j-1];
                    array[j-1] = array[j];
                    array[j] = temp;
                    flag = 1;
                }
                if (0 == flag) {
                    break;
                }
                else {
                    flag = 1;
                }
            }
        }
        catch(ArrayIndexOutOfBoundsException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args)
        throws Exception {
        int[] array = new int[] {9,8,7,6,5,4,3,2,1};
        Class clazz = Class.forName("BubbleSort");
        BubbleSort obj = (BubbleSort)clazz.newInstance();
        obj.bubbleSort(array);
        for(i=0; i<array.length; i++) {
            System.out.println(array[i]);
        }
    }
}
