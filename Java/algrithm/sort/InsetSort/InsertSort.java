import java.io.IOException;

public class InsertSort {

	public void insertSort(int[] array) 
		throws IOException {
		try {
			int temp = 0;
                        int j = 0;
    			for(int i=1; i<array.length; i++) {
        			temp = array[i];
				for(j=i-1; j>=0 && temp<array[j]; j--) {
	    				array[j+1] = array[j];
				}
				array[j+1] = temp;
    			}
    
    			for(int i=0; i<array.length; i++) {
    				System.out.println(array[i]);
    			}
		}
		catch(ArrayIndexOutOfBoundsException e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) 
		throws Exception {
		int[] array = new int[] {9,8,7,6,5,4,3,2,1};
		Class clazz = Class.forName("InsertSort");
		InsertSort obj = (InsertSort)clazz.newInstance();
		obj.insertSort(array);
	}
}
