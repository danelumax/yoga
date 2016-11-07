package DiamondTest;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DiamondTest {

	public static void main(String[] args) {
		System.out.println("\nTest List ...");
		List<String> books = new ArrayList<>();
		books.add("Crazy Java");
		books.add("Crazy Android");
		books.forEach(ele -> System.out.println(ele.length()));
		
		System.out.println("\nTest Map ...");
		Map<String, List<String>> schoolsInfo = new HashMap<>();
		List<String> schools = new ArrayList<>();
		schools.add("Three Stars");
		schools.add("West Way");
		schoolsInfo.put("Monkey", schools);
		schoolsInfo.forEach((key, value) -> System.out.println(key + "-->" + value));
	}

}
