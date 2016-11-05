import java.io.IOException;

public class FastSort {

    private int division(int[] array, int left, int right)
        throws IOException {
        try {
            int base = array[left];
            while(left < right) {
                while(left<right && array[right]>=base) {
                    right--;
                }
                array[left] = array[right];
                while(left<right && array[left]<=base) {
                    left++;
                }
                array[right] = array[left];
            }
            array[left] = base;
            return left;
        }
        catch(ArrayIndexOutOfBoundsException e) {
            e.printStackTrace();
            return -1;
        }
    }

    public void fastSort(int[] array, int left, int right)
        throws IOException {
        try {
            int i = 0;
            if (left < right) {
                i = division(array, left, right);
                fastSort(array, left, i-1);
                fastSort(array, i+1, right);
            }
        }
        catch(ArrayIndexOutOfBoundsException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) 
        throws Exception {
        int[] array = new int[] {9,8,7,6,5,4,3,2,1};
        Class clazz = Class.forName("FastSort");
        FastSort obj = (FastSort)clazz.newInstance();
        obj.fastSort(array, 0, array.length-1);
        for(int i=0; i<array.length; i++) {
            System.out.println(array[i]);
        }
    }
}

    
