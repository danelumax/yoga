package LambdaQs;

import LambdaQs.Eatable;
import LambdaQs.Flyable;
import LambdaQs.Addable;

public class LambdaQs {

	public void eat(Eatable e) {
		System.out.println(e);
		e.taste();
	}
	
	public void drive(Flyable f) {
		System.out.println("I am driving: " + f);
		f.fly("Sunning");
	}
	
	void test(Addable add) {
		System.out.println("Add 5 and 3: " + add.add(5, 3));
	}
	
	/* main */
	public static void main(String[] args) throws Exception {
		LambdaQs lq = new LambdaQs();
		System.out.println("\nTest Eatable ...");
		lq.eat(() -> System.out.println("Apple taste good!"));
		
		System.out.println("\nTest Flyable ...");
		lq.drive(weather1 -> 
		{
			System.out.println("Today's weather is :" + weather1);
			System.out.println("Airplane fly well!");
		});
		
		System.out.println("\nTest Addable ...");
		lq.test((a1, b1) -> a1 + b1);
	}

}


